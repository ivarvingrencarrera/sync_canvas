from .canvas.model import CanvasLms
from log.notification import Notification

class ValidateAccount(CanvasLms):

    def __init__(self, name, sis_account_id, sis_parent_account_id) -> None:
        super().__init__()
        self.name = name
        self.sis_account_id = sis_account_id
        self.sis_parent_account_id = sis_parent_account_id

    def validate_account(self):
        if not self.__is_account_created_canvas():
            self.create_account(self.name, self.sis_account_id, self.sis_parent_account_id)
        if self.__is_account_parent_account_different() or self.__is_account_name_different():
            self.set_account_settings(self.name)  

    def __is_account_created_canvas(self) -> bool:
        try:
            self.account_canvas = self.get_account(self.sis_account_id)
            status = True
        except:
            status = False
        return status

    def __is_account_name_different(self) -> bool:
        if self.account_canvas.name != self.name:
            status = True
        else:
            status = False
        return status

    def __is_account_parent_account_different(self) -> bool:
        self.parent_account_canvas = self.get_parent_account(self.sis_parent_account_id)
        if self.parent_account_canvas.id != self.account_canvas.parent_account_id:
            status = True
            Notification.account_parent_account_different(Notification(), self.account_canvas, 
                self.parent_account_canvas)
        else:
            status = False
        return status


class ValidateCourse(CanvasLms):
    
    def __init__(self, name, course_code, sis_course_id, workflow_state, course_type, 
        sis_account_id, sis_term_id
        ) -> None:
        super().__init__()
        self.name: str = name
        self.course_code: str = course_code
        self.sis_course_id: str = sis_course_id
        self.workflow_state: str = workflow_state
        self.course_type: str = str(course_type)
        self.sis_account_id: str = sis_account_id
        self.sis_term_id: str = sis_term_id
 
    def validate_course(self):
        if self.workflow_state == 'completed':
            if self.__is_course_created_canvas() and self.__is_course_state_different(): 
                pass
                #self.update_canvas_course_state()
        else:
            if self.__is_course_created_canvas():
                if self.__is_course_account_different() or self.__is_course_name_different() or \
                    self.__is_course_term_different(): 
                    self.set_course_settings(self.name, self.course_code, self.sis_account_id, self.sis_term_id)
                # if self.__is_course_state_different(): 
                #     self.update_canvas_course_state()
            else:
                self.create_course(self.name, self.course_code, self.sis_course_id, 
                    self.workflow_state, self.sis_account_id, self.sis_term_id
                )


    def __is_course_created_canvas(self) -> bool:
        try:
            self.course_canvas = self.get_course(self.sis_course_id)
            status = True
        except:
            status = False
        return status
    
    def __is_course_name_different(self) -> bool:
        if self.course_type == '1':
            if self.course_canvas.name[5:] != self.name[5:] or \
                self.course_canvas.course_code[5:] != self.course_code[5:]:
                index = self.course_canvas.name[:5]
                self.name = index + self.name[5:]
                self.course_code = index + self.course_code[5:]        
                status = True
            else: 
                status = False
        else:
            if self.course_canvas.name != self.name or self.course_canvas.course_code != self.course_code:
                status = True
            else:
                status = False
        return status

    def __is_course_account_different(self) -> bool:
        self.account_canvas = self.get_account(self.sis_account_id)
        return True if self.account_canvas.id != self.course_canvas.account_id else False
    
    def __is_course_term_different(self) -> bool:
        self.enrollment_term_canvas = self.get_enrollment_term(self.sis_term_id)
        return True if self.course_canvas.enrollment_term_id != self.enrollment_term_canvas ['id'] else False

    def __is_course_state_different(self) -> bool:
        if self.course_canvas.workflow_state.upper() == 'AVAILABLE': workflow_state = 'ACTIVE'  
        else: workflow_state = self.course_canvas.workflow_state.upper()
        return True if self.course_state != workflow_state else False


class ValidateSection(CanvasLms):
    
    def __init__(self, name, sis_section_id, start_at, end_at, sis_course_id) -> None:
        super().__init__()
        self.name: str = name
        self.sis_section_id: str = sis_section_id
        self.start_at: str = start_at
        self.end_at: str = end_at
        self.sis_course_id = sis_course_id
 
    def validate_section(self):
        if self.__is_section_created_canvas():
            if self.__is_section_name_different() or self.__is_section_start_at_different() or \
                self.__is_section_end_at_different(): 
                self.set_section_settings(self.name, self.start_at, self.end_at)
        else:
            self.create_section(self.name, self.sis_section_id, self.start_at, self.end_at, self.sis_course_id)

    def __is_section_created_canvas(self) -> bool:
        try:
            self.section_canvas = self.get_section(self.sis_section_id)
            status = True
        except:
            status = False
        return status
    
    def __is_section_name_different(self) -> bool:
        if self.section_canvas.name != self.name:
            status = True
        else:
            status = False
        return status

    def __is_section_start_at_different(self) -> bool:
        return True if self.section_canvas.start_at != self.start_at else False
    
    def __is_section_end_at_different(self) -> bool:
        return True if self.section_canvas.end_at != self.end_at else False