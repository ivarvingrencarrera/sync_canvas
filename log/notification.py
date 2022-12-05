from email.message import EmailMessage
from smtplib import SMTP
from decouple import config

class Notification():
    
    def __init__(self) -> None:
        self.__SMTP_SERVER = None
        self.__SMTP_PORT = None
        self.__SMTP_USER = None
        self.__SMTP_PASSWORD = None
        self.mail_subject = None
        self.mail_to = None
        self.mail_body = None
        self.email_message = None

    def __set_smtp_office_365(self):
        self.__SMTP_SERVER = config('OFFICE_SMTP_SERVER')
        self.__SMTP_PORT = config('OFFICE_SMTP_PORT')
        self.__SMTP_USER = config('OFFICE_SMTP_USER')
        self.__SMTP_PASSWORD = config('OFFICE_SMTP_PASSWORD')

    def term_id_not_found(self, sis_term_id) -> None:
        self.__set_smtp_office_365()
        message = f"O período '{sis_term_id}' não está cadastrado no Canvas. É necessário cadastrá-lo para criação dos ambientes no Canvas."
        self.mail_subject = 'Período não cadastrado no Canvas'
        self.mail_to = 'ead.ti@pucminas.br'
        self.mail_body = self.__get_mail_body(message, 'amigos')
        self.email_message = self.__get_email_message()
        self.__send_message()

    def account_parent_account_different(self, account, parent_account) -> None:
        self.__set_smtp_office_365()
        message = f"A conta '{account}' está com a vinculação incorreta. A mesma deve ser vinculada à conta '{parent_account}'. \
            \nGentileza verificar se a vinculação foi corrigida no processo automático e caso contrário, é necessário realizar a alteração manualmente."
        self.mail_subject = 'Conta incorreta'
        self.mail_to = 'ead.ti@pucminas.br'
        self.mail_body = self.__get_mail_body(message, 'amigos')
        self.email_message = self.__get_email_message()
        self.__send_message()
         
    def __send_message(self):
        status = True
        while status:
            try:
                with SMTP(self.__SMTP_SERVER, self.__SMTP_PORT) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.login(self.__SMTP_USER, self.__SMTP_PASSWORD)
                    smtp.send_message(self.email_message)
                    status = False
            except:
                status = True

    def __get_email_message(self):
        email_message = EmailMessage()
        email_message ['Subject'] = self.mail_subject
        email_message ['From'] = self.__SMTP_USER
        email_message ['To'] = self.mail_to
        email_message.set_content(self.mail_body)
        return email_message		
  
    def __get_mail_body(self, message, person_name):
        mail_body = f"""Olá, {person_name}!\n\n{message}\n\nAtenciosamente,\n\nCoordenação de Tecnologia da Informação
        """
        return mail_body