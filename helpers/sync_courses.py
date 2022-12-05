from models import *
from concurrent.futures import ThreadPoolExecutor


class SyncCourse():

    def __init__(self) -> None:
        self.course_sync = True
        self.year = 2023
        self.semester = 1
        self.salead = SalEad()

    def start_sync_course(self):
        self.sync_course_sal_ead()

    def sync_course_sal_ead(self):
        courses = self.salead.get_courses_unsync(self.year)
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for course in courses:
                futures.append(executor.submit(self.__sync_course, course))            

    def __sync_course(self, course):
        # Account validations
        if course['workflow_state'] != 'completed':
            fourth_level = course['accounts']['fourth_level']
            third_level = course['accounts']['third_level']
            second_level = course['accounts']['second_level']
            first_level = course['accounts']['first_level']

            validate = ValidateAccount(third_level['name'],
                third_level['sis_account_id'], fourth_level['sis_account_id']
            )
            validate.validate_account()
            
            validate = ValidateAccount(second_level['name'],
                second_level['sis_account_id'], third_level['sis_account_id']
            )
            validate.validate_account()
            
            validate = ValidateAccount(first_level['name'],
                first_level['sis_account_id'], second_level['sis_account_id']
            )
            validate.validate_account()
            account_canvas = validate.account_canvas

        # Course validations
        name = course['name']
        course_code = course['course_code']
        sis_course_id = course['sis_course_id']
        workflow_state = course['workflow_state']
        course_type = course['course_type']
        sis_account_id = course['accounts']['first_level']['sis_account_id']
        sis_term_id = course['sis_term_id']

        validate = ValidateCourse(name, course_code, sis_course_id, workflow_state, 
            course_type, sis_account_id, sis_term_id
        )
        validate.validate_course()
        course_canvas = validate.course_canvas

        # Section Validations
        name = course['section']['name']
        sis_section_id = course['section']['sis_section_id']
        start_at = course['section']['start_at']
        end_at = course['section']['end_at']
        
        validate = ValidateSection(name, sis_section_id, start_at, end_at, sis_course_id)
        validate.validate_section()

        # Database update
        if course_canvas != None:
            if course['origin'] == 'SAL_EAD':
                self.salead.set_course_unsync(course['offer_id'], account_canvas.id, sis_account_id,
                course['discipline_id'], course_canvas.id, sis_course_id
            )
            elif course['origin'] == 'SGA_PRESENCIAL':
                pass