from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from top_bot.utils.callbacks import *
from top_bot.core.models import AbstractUser

class DefaultInline(InlineKeyboardBuilder):
    def markup(self) -> InlineKeyboardMarkup:
        """alias for as_markup function"""
        return self.as_markup()

class StartInline(DefaultInline):
    def start(self, user: int):
            self.button(text="Подать заявку", callback_data=StartCallback(action=2, user=user,))
            self.adjust(1)
            return self.markup()
    
class ManagerInline(DefaultInline):
    def apply(self, user: int):
        self.button(text="Подтвердить", callback_data=StartCallback(action=0, user=user,))
        self.button(text="Отклонить", callback_data=StartCallback(action=1, user=user,))
        return self.markup()
    
    def start(self):
        print()
        self.button(text='Создать группу', callback_data=GroupCallback(action='add', group='group'))
        self.button(text='Все группы', callback_data=GroupCallback(action='list', group='groups'))
        self.adjust(1)
        return self.markup()

    def groups(self, groups: list[str]):
        for group in groups:
            self.button(text=f'{group}', callback_data=GroupCallback(action='retrieve', group=group))
        self.button(text='Добавить группу', callback_data=GroupCallback(action='add', group='group'))
        self.adjust(1)
        return self.markup()
    
    def confirmation_destroy_group(self, group: str):
        self.button(text='Да', callback_data=GroupCallback(action='confirm_destroy', group=group))
        self.button(text='Нет', callback_data=GroupCallback(action='retrieve', group=group))
        self.adjust(2)
        return self.markup()

    def subjects(self, group: str, subjects: list[str]):
        for subject in subjects:
            self.button(text=f'{subject}', callback_data=SubjectCallback(action='retrieve', group=group, subject=subject))
        self.button(text='Добавить дисциплину', callback_data=SubjectCallback(action='add', group=group, subject=subject))
        self.button(text='Удалить группу', callback_data=GroupCallback(action='destroy', group=group))
        self.button(text='Назад к группам', callback_data=GroupCallback(action='list', group='groups'))
        self.adjust(1)
        return self.markup()
    
    def confirmation_destroy_group(self, group: str):
        self.button(text='Да', callback_data=GroupCallback(action='confirm_destroy', group=group))
        self.button(text='Нет', callback_data=GroupCallback(action='retrieve', group=group))
        self.adjust(2)
        return self.markup()

    
    def add_subject_result(self, group: str, subject: str):
        self.button(text='Продолжить добавление', callback_data=SubjectCallback(action='add', group=group, subject=subject))
        self.button(text='Просмотреть дисциплины', callback_data=GroupCallback(action='retrieve', group=group))
        self.button(text='Назад к группам', callback_data=GroupCallback(action='list', group='groups'))
        self.adjust(2)
        return self.markup()

    def confirmation_destroy_subject(self, group: str, subject: str):
        self.button(text='Да', callback_data=SubjectCallback(action='confirm_destroy', group=group, subject=subject))
        self.button(text='Нет', callback_data=SubjectCallback(action='retrieve', group=group, subject=subject))
        self.adjust(2)
        return self.markup()

    def media(self, group: str, subject: str):
        self.button(text='Добавить медиа', callback_data=MediaCallback(action='add', group=group, subject=subject, path='', offset=''))
        self.button(text='Просмотреть медиа', callback_data=MediaCallback(action='list', group=group, subject=subject, path='', offset=''))
        self.button(text='Назад к дисциплинам', callback_data=GroupCallback(action='retrieve', group=group))
        self.button(text='Удалить дисциплину', callback_data=SubjectCallback(action='destroy', group=group, subject=subject))
        self.button(text='Назад к группам', callback_data=GroupCallback(action='list', group='groups'))
        self.adjust(2,1,1,1)
        return self.markup()
    
    def for_empty_group(self, group: str):
        self.button(text='Добавить дисциплину', callback_data=SubjectCallback(action='add', group=group, subject=''))
        self.button(text='Удалить группу', callback_data=GroupCallback(action='destroy', group=group))
        self.button(text='Назад к группам', callback_data=GroupCallback(action='list', group='groups'))
        self.adjust(1)
        return self.markup()

    def result_add_media(self, group: str, subject: str, offset: str, path: str):
        self.button(text='Добавить ещё', callback_data=MediaCallback(action='add', group=group, subject=subject, path=path, offset=offset))
        self.button(text='Просмотреть медиа', callback_data=MediaCallback(action='list', group=group, subject=subject, path=path, offset=offset))
        self.button(text='Назад к дисциплинам', callback_data=GroupCallback(action='retrieve', group=group))
        self.adjust(2)
        return self.markup()
    
    def cancel_save_media(self, group: str):
        self.button(text='Отменить отправку', callback_data=GroupCallback(action='retrieve', group=group))
        self.adjust(1)
        return self.markup()
    
    def list_media_paths(self, group: str, subject: str, media_paths: list[str], offset: str):
        for path in media_paths:
            self.button(text=f'{path}', callback_data=MediaCallback(subject=subject, action='retrieve', group=group, path=path, offset='0'))
        self.button(text='Назад к медиа', callback_data=SubjectCallback(action='retrieve', group=group, subject=subject))
        self.adjust(1)
        return self.markup()

    def list_media_files(self, group: str, subject: str, offset: str, path: str):
        offsetpl=offset+'+5'
        offsetmn=offset+'-5'
        self.button(text='Предыдущие', callback_data=MediaCallback(action='retrieve', group=group, subject=subject, path=path, offset=offsetmn)) 
        self.button(text='Следующие', callback_data=MediaCallback(action='retrieve', group=group, subject=subject, path=path, offset=offsetpl)) 
        self.button(text='Добавить медиа', callback_data=MediaCallback(action='add', group=group, subject=subject, path=path, offset=''))
        self.button(text='Назад к дисциплинам', callback_data=GroupCallback(action='retrieve', group=group))
        self.adjust(2,1,1)
        return self.markup()

class TeacherInline(DefaultInline):
    def start(self):
        self.button(text="Все группы", callback_data=GroupCallback(action="list", group=""))
        return self.markup()

    def groups(self, groups: list[str]):
        for group in groups:
            self.button(text=f'{group}', callback_data=GroupCallback(action='retrieve', group=group))
        self.adjust(1)
        return self.markup()
    
    def subjects(self, group: str, subjects: list[str]):
        for subject in subjects:
            self.button(text=f'{subject}', callback_data=SubjectCallback(action='retrieve', group=group, subject=subject))
        self.button(text='Назад к группам', callback_data=GroupCallback(action='list', group='groups'))
        self.adjust(1)
        return self.as_markup()

    def media(self, group: str, subject: str):
        self.button(text='Добавить медиа', callback_data=MediaCallback(action='add', group=group, subject=subject, path='', offset=''))
        self.button(text='Просмотреть медиа', callback_data=MediaCallback(action='list', group=group, subject=subject, path='', offset=''))
        self.button(text='Назад к дисциплинам', callback_data=GroupCallback(action='retrieve', group=group))
        self.button(text='Назад к группам', callback_data=GroupCallback(action='list', group='groups'))
        self.adjust(2,1,1)
        return self.markup()

class StaffInline(InlineKeyboardBuilder):
    def start(self, user: AbstractUser):
        self.button(text="Отправить тикет", )
        if user.is_staff():
            self.button(text="Все группы", callback_data=GroupCallback( action="list", group=""))
        if user.is_manager() or user.is_superuser():
            self.button(text="Добавить группу", callback_data=GroupCallback(action="add", group=""))

    def groups(self, user: str, groups: list[str]):
        for group in groups:
            self.button(text=f'{group}', callback_data=GroupCallback(action='retrieve', group=group))
        self.adjust(1)
        return self.as_markup()