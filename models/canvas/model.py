from canvasapi import Canvas
import requests, json
from log.notification import Notification
from decouple import config


class CanvasLms():

    def __init__(self) -> None:
        self.__API_KEY = None
        self.__API_URL = None
        self.__canvas = self.__get_connection()
        self.parent_account_canvas = None
        self.account_canvas = None
        self.course_canvas = None
        self.section_canvas = None
        self.enrollment_term_canvas = None

    def __get_connection(self):
        self.__API_KEY = config('CANVAS_API_KEY')
        self.__API_URL = config('CANVAS_API_URL')
        connection = Canvas(self.__API_URL, self.__API_KEY)
        return connection

    def get_parent_account(self, sis_parent_account_id):
        parent_account = self.__canvas.get_account(sis_parent_account_id, 'sis_account_id')
        self.parent_account_canvas
        return parent_account

    def get_account(self, sis_account_id):
        account = self.__canvas.get_account(sis_account_id, 'sis_account_id')
        self.account_canvas = account
        return account     

    def get_course(self, sis_course_id):
        course = self.__canvas.get_course(sis_course_id, 'sis_course_id')
        self.course_canvas = course
        return course
        
    def create_account(self, name, sis_account_id, sis_parent_account_id) -> None:
        self.parent_account_canvas = self.get_parent_account(sis_parent_account_id)
        self.parent_account_canvas.create_subaccount(account={'name': name, 'sis_account_id': sis_account_id})
        self.account_canvas = self.get_account(sis_account_id)
        print(f"New Account: {self.account_canvas.name} ({self.account_canvas.sis_account_id}) - {self.parent_account_canvas.name}")
    
    def create_course(self, name, course_code, sis_course_id, workflow_state, sis_account_id, sis_term_id):
        self.enrollment_term_canvas = self.get_enrollment_term(sis_term_id)
        if self.enrollment_term_canvas == None:
            Notification.term_id_not_found(Notification(), sis_term_id)
        else:
            account = self.get_account(sis_account_id)
            account.create_course(course = {'name': name, 'course_code': course_code, 
                'sis_course_id': sis_course_id, 'term_id': self.enrollment_term_canvas['id'],
                'workflow_state': workflow_state}, enable_sis_reactivation=True
            )
            self.course_canvas = self.get_course(sis_course_id)
            print(f"New Course: {self.course_canvas.name} ({self.course_canvas.sis_course_id}) - {account.name}")

    def set_account_settings(self, name) -> None:
        self.account_canvas.update(account={'parent_account_id': self.parent_account_canvas.id, 'name': name})
        print(f"Update Account: {self.account_canvas.name} ({self.account_canvas.sis_account_id})")

    def set_course_settings(self, name, course_code, sis_account_id, sis_term_id):
        enrollment_term = self.get_enrollment_term(sis_term_id)
        account = self.get_account(sis_account_id)
        self.course_canvas.update(course = {'name': name, 'course_code': course_code,
            'account_id': account.id, 'term_id': enrollment_term['id']})
        print(f"Update Course: {self.course_canvas.name} ({self.course_canvas.sis_course_id})")

    def get_enrollment_term(self, sis_term_id):
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.__API_KEY}
        url = f'{self.__API_URL}api/v1/accounts/1/terms/sis_term_id:{sis_term_id}'
        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            enrollment_term = None
            self.enrollment_term_canvas = enrollment_term
        else:
            enrollment_term = json.loads(response.content.decode('utf-8'))
            self.enrollment_term_canvas = enrollment_term
        return enrollment_term

    def get_section(self, sis_section_id):
        section = self.__canvas.get_section(sis_section_id, 'sis_section_id')
        self.section_canvas = section
        return section

    def create_section(self, name, sis_section_id, start_at, end_at, sis_course_id):
        self.get_course(sis_course_id)
        self.course_canvas.create_course_section(course_section = {'name': name, 
            'sis_section_id': sis_section_id, 'start_at': start_at, 'end_at': end_at,
            'restrict_enrollments_to_section_dates': True}
            )
        self.section_canvas = self.get_section(sis_section_id)
        print(f"New Section: {self.section_canvas.name} ({self.section_canvas.sis_section_id}) - {self.course_canvas.name}")
    
    def set_section_settings(self, name, start_at, end_at):
        self.section_canvas.edit(course_section={'name': name, 'start_at': start_at, 'end_at': end_at})
        print(f"Update Section: {self.section_canvas.name} ({self.section_canvas.sis_section_id})")