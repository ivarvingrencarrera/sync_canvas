
from models.database.mssql import Database
from models.converters import adjustStringCase
from decouple import config
import pyodbc


class SalEad(Database):

    def __init__(self) -> None:
        super().__init__(self.__get_connection())
        self.__course_origin = None
        self.__institute_name = None
        self.__institute_id = None
        self.__course_name = None
        self.__course_id = None
        self.__course_type = None
        self.__discipline_name = None
        self.__discipline_id = None
        self.__discipline_index = None
        self.__offer_id = None
        self.__offer_num = None
        self.__offer_year = None

    def __get_connection(self) -> pyodbc.Connection:
        DRIVER = '{ODBC Driver 17 for SQL Server}'
        SERVER = config('SAL_EAD_SERVER') 
        DATABASE = config('SAL_EAD_DATABASE')
        DB_UID = config('SAL_EAD_UID')
        PWD = config('SAL_EAD_PWD')
        MARS_CONNECTION = 'yes'
        string_connection = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};UID={DB_UID};PWD={PWD};MARS_CONNECTION={MARS_CONNECTION}'
        connection = pyodbc.connect(string_connection)
        return connection

    def get_courses_unsync(self, year) -> list[dict]:
        query = f"""
        WITH COURSES
        AS	(
            SELECT DISTINCT
                    'SAL_EAD' AS course_origin,
                    CASE
                        WHEN o.cod_instituto = 53252 THEN 'IPUC - INSTITUTO POLITÉCNICO'
                        WHEN o.cod_instituto = 53253 THEN 'ICBS - INSTITUTO DE CIÊNCIAS BIOLÓGICAS E DA SAÚDE'
                        WHEN o.cod_instituto = 53254 THEN 'ICH - INSTITUTO DE CIÊNCIAS HUMANAS'
                        WHEN o.cod_instituto = 53255 THEN 'ICEI - INSTITUTO DE CIÊNCIAS EXATAS E INFORMÁTICA'
                        WHEN o.cod_instituto = 53256 THEN 'FAPSI - FACULDADE DE PSICOLOGIA'
                        WHEN o.cod_instituto = 53258 THEN 'FMD - FACULDADE MINEIRA DE DIREITO'
                        WHEN o.cod_instituto = 53259 THEN 'ICEG - INSTITUTO DE CIÊNCIAS ECONÔMICAS E GERENCIAIS'
                        WHEN o.cod_instituto = 53260 THEN 'IFTDJ - INSTITUTO DE FILOSOFIA E TEOLOGIA DOM JOÃO RESENDE COSTA'
                        WHEN o.cod_instituto = 53926 THEN 'FCA - FACULDADE DE COMUNICAÇÃO E ARTES'
                        WHEN o.cod_instituto = 61286 THEN 'ICS - INSTITUTO DE CIÊNCIAS SOCIAIS'
                        ELSE CONVERT(char, o.cod_instituto)
                    END AS institute_name,
                    o.cod_instituto AS institute_id,
                    TRIM(UPPER(o.nom_curso)) AS course_name,
                    cod_curso AS course_id,
                    o.cod_tipo_curso AS course_type,
                    TRIM(UPPER(co.nom_disciplina)) AS discipline_name,
                    co.seq_curriculo_oferta AS discipline_id,		
                    ROW_NUMBER() OVER	(
                        PARTITION BY	o.seq_oferta
                            ORDER BY	co.seq_curriculo_oferta
                    ) AS discipline_index,
                    CASE
                        WHEN co.ind_excluido = 1 THEN 'INACTIVE'
                        WHEN co.ind_excluido = 0 THEN 'ACTIVE'			
                    END AS discipline_state,
                    o.seq_oferta AS offer_id,
                    num_oferta AS offer_num,
                    YEAR(o.dat_inicio) AS offer_year
            FROM	SAL_EAD..oferta AS o
                    INNER JOIN SAL_EAD..curriculo_oferta AS co
                        ON o.seq_oferta = co.seq_oferta
                        AND o.origem = co.origem 
            WHERE	o.origem = 'EAD'
                    AND (o.ind_atualizado_EAD = 0 or co.ind_atualizado_EAD = 0)
                    AND YEAR(o.dat_inicio) = {year}
                    AND o.cod_tipo_curso in (1, 5, 7, 8)
                    --AND o.cod_curso = 825
            )
        SELECT	*
        FROM	COURSES
        ORDER	BY course_type, offer_id, discipline_index
        """
        itens = self.fetch(query)
        courses = []
        for item in itens:
            self.__course_origin = item['course_origin']
            self.__institute_name = item['institute_name']
            self.__institute_id = item['institute_id']
            self.__course_name = item['course_name'].strip()
            self.__course_id = item['course_id']
            self.__course_type = item['course_type']
            self.__discipline_name = item['discipline_name'].strip()
            self.__discipline_id = item['discipline_id']
            self.__discipline_index = item['discipline_index']
            self.__discipline_state = item['discipline_state']
            self.__offer_num = item['offer_num']
            self.__offer_year = item['offer_year']
            self.__offer_id = item['offer_id']
            
            if self.__institute_id == 0 and self.__course_type != 8:
                pass #enviar email para o setor informando o erro
            else:
                course = {
                    'name': self.__get_discipline_name(),
                    'course_code': self.__get_discipline_course_code(),
                    'sis_course_id': self.__get_discipline_sis_course_id(),
                    'sis_term_id': self.__get_discipline_sis_term_id(),
                    'workflow_state': self.__get_discipline_workflow_state(),
                    'section': {
                        'name': self.__get_section_name(),
                        'sis_section_id': self.__get_section_sis_section_id(),
                        'start_at': self.__get_section_start_at(),
                        'end_at': self.__get_section_end_at(),
                    },                    
                    'accounts': {
                        'first_level': {
                            'name': self.__get_first_account_level_name(),
                            'sis_account_id': self.__get_first_account_level_sis_account_id()
                            },
                        'second_level': {
                            'name': self.__get_second_account_level_name(),
                            'sis_account_id': self.__get_second_account_level_sis_account_id()
                        },
                        'third_level': {
                            'name': self.__get_third_account_level_name(),
                            'sis_account_id': self.__get_third_account_level_sis_account_id()
                        },
                        'fourth_level': {
                            'name': self.__get_fourth_account_level_name(),
                            'sis_account_id': self.__get_fourth_account_level_sis_account_id()
                        }
                    },
                    'origin': self.__course_origin,
                    'course_type': self.__course_type,
                    'offer_id': self.__offer_id,
                    'discipline_id': self.__discipline_id
                }
                courses.append(course)
        return courses

    def set_course_unsync(self, offer_id, lms_account_id, sis_account_id, discipline_id, 
        lms_course_id, sis_course_id) -> None:
        query_offer = f"""
        UPDATE  oferta
        SET     lms_account_id = {lms_account_id}, 
                cod_curso_EAD = '{sis_account_id}', 
                ind_atualizado_ead = 1, 
                ind_atualizado_sal = 0, 
                dat_atualizacao_sal = NULL, 
                dat_atualizacao_ead = GETDATE()
        WHERE   seq_oferta = {offer_id}
                AND origem = 'EAD'
        """
        self.update(query_offer)

        query_discipline = f"""
        UPDATE  curriculo_oferta
        SET     lms_course_id = {lms_course_id},
                cod_disciplina_ead = '{sis_course_id}', 
                ind_atualizado_ead = 1, 
                dat_atualizacao_ead = GETDATE()
        WHERE   seq_oferta = {offer_id}
                AND seq_curriculo_oferta = {discipline_id}
                AND origem = 'EAD'
        """
        self.update(query_discipline)        

    def __get_fourth_account_level_name(self) -> str:
        match (self.__course_type):
            case 1:
                account_name = 'Lato Sensu - EAD'
            case 5:
                account_name = 'Lato Sensu - EAD'
            case 7:
                account_name = 'Curta Duração'
            case 8:
                account_name = 'Lato Sensu - EAD'
        return account_name

    def __get_fourth_account_level_sis_account_id(self) -> str:
        if self.__course_type == 8  :
            account_sis_account_id = 'SALEAD_1'
        else:
            account_sis_account_id = f'SALEAD_{self.__course_type}'
        return account_sis_account_id

    def __get_third_account_level_name(self) -> str:
        if self.__course_type == 8:
            account_name = 'Curso/Disciplina'
        else:
            account_name = self.__institute_name
        return adjustStringCase(account_name)

    def __get_third_account_level_sis_account_id(self) -> str:
        if self.__course_type == 8:
            account_sis_account_id = 'SALEAD_8'
        else:
            account_sis_account_id = f'SALEAD_{self.__course_type}_{self.__institute_id}'
        return account_sis_account_id

    def __get_second_account_level_name(self) -> str:
        if self.__course_type == 8:
            account_name = f"{self.__course_name.replace(' - CD', '')}"
        else:
            account_name = self.__course_name
        return adjustStringCase(account_name)

    def __get_second_account_level_sis_account_id(self) -> str:
        if self.__course_type == 8:
            account_sis_account_id = f'SALEAD_{self.__course_type}_{self.__course_id}'
        else:
            account_sis_account_id = f'SALEAD_{self.__course_type}_{self.__institute_id}_{self.__course_id}'
        return account_sis_account_id

    def __get_first_account_level_name(self) -> str:
        if self.__course_type == 1:
            account_name = f'{self.__course_name} - {self.__offer_year}'
        elif self.__course_type == 8:
            account_name = f"{self.__course_name.replace(' - CD', '')} - Oferta {str(self.__offer_num).zfill(2)}"
        else:
            account_name = f"{self.__course_name} - Oferta {str(self.__offer_num).zfill(2)}"
        return adjustStringCase(account_name)            

    def __get_first_account_level_sis_account_id(self) -> str:
        if self.__course_type == 8:
            account_sis_account_id = f'SALEAD_{self.__course_type}_{self.__course_id}_{self.__offer_num}'
        else:
            account_sis_account_id = f'SALEAD_{self.__course_type}_{self.__institute_id}_{self.__course_id}_{self.__offer_num}'
        return account_sis_account_id

    def __get_discipline_name(self) -> str:
        if self.__course_type == 1:
            discipline_name = f'{str(self.__discipline_index).zfill(2)} - {self.__discipline_name} ({self.__offer_year})'
        elif self.__course_type == 8:
            discipline_name = f"{self.__discipline_name.replace(' - CD', '')} - Oferta {str(self.__offer_num).zfill(2)}"            
        else:
            discipline_name = f"{self.__discipline_name} - Oferta {str(self.__offer_num).zfill(2)}"
        return adjustStringCase(discipline_name)            

    def __get_discipline_course_code(self) -> str:
        if self.__course_type == 1:
            discipline_course_code = f'{str(self.__discipline_index).zfill(2)} - {self.__discipline_name} ({self.__offer_year})'
        elif self.__course_type == 8:
            discipline_course_code = f"{self.__discipline_name.replace(' - CD', '')} - Oferta {str(self.__offer_num).zfill(2)}"
        else:
            discipline_course_code = f"{self.__discipline_name} - Oferta {str(self.__offer_num).zfill(2)}"
        return adjustStringCase(discipline_course_code)
            
    def __get_discipline_sis_course_id(self) -> str:
        if self.__course_type == 8:
            discipline_sis_course_id = f'SALEAD_{self.__course_id}_{self.__offer_num}_{self.__discipline_id}'
        else:
            discipline_sis_course_id = f'SALEAD_{self.__institute_id}_{self.__course_id}_{self.__offer_num}_{self.__discipline_id}'
        return discipline_sis_course_id

    def __get_discipline_sis_term_id(self) -> str:
        match (self.__course_type):
            case 1:
                discipline_sis_term_id = f'term_pos_{self.__offer_year}'
            case 5:
                discipline_sis_term_id = f'term_aperfeicoamento_{self.__offer_year}'
            case 7:
                discipline_sis_term_id = 'term_curta_duracao'
            case 8:
                discipline_sis_term_id = f'term_curso_disciplina_{self.__offer_year}'
        return discipline_sis_term_id

    def __get_discipline_workflow_state(self) -> str:
        return 'unpublished' if self.__discipline_state == 'ACTIVE' else 'completed'

    def __get_section_name(self) -> str:
        if self.__course_type == 1:
            discipline_name = f'{self.__discipline_name} ({self.__offer_year})'
        elif self.__course_type == 8:
            discipline_name = f"{self.__discipline_name.replace(' - CD', '')} - Oferta {str(self.__offer_num).zfill(2)}"            
        else:
            discipline_name = f"{self.__discipline_name} - Oferta {str(self.__offer_num).zfill(2)}"
        return adjustStringCase(discipline_name)

    def __get_section_sis_section_id(self) -> str:
        if self.__course_type == 8:
            sis_section_id = f'SALEAD_{self.__course_id}_{self.__offer_num}_{self.__discipline_id}_section'
        else:
            sis_section_id = f'SALEAD_{self.__institute_id}_{self.__course_id}_{self.__offer_num}_{self.__discipline_id}_section'
        return sis_section_id

    def __get_section_start_at(self) -> str:
        start_at = None
        return start_at

    def __get_section_end_at(self) -> str:
        end_at = None
        return end_at