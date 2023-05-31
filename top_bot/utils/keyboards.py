from aiogram.types import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder
from top_bot.utils.callbacks import *
from top_bot.core.models import AbstractUser

class DefaultInline(InlineKeyboardBuilder):
    def markup(self) -> InlineKeyboardMarkup:
        """alias for as_markup function"""
        return self.as_markup()

class StartInline(DefaultInline):
    def start(self, user_id: int):
            self.button(text="Подать заявку", callback_data=StartCallback(action=2, user=user_id))
            self.adjust(1)
            return self.markup()
    
class ManagerInline(DefaultInline):
    def apply(self, user_id: int):
        self.button(text="Подтвердить", callback_data=StartCallback(action=0, user=user_id))
        self.button(text="Отклонить", callback_data=StartCallback(action=1, user=user_id))
        return self.markup()
    
    def start(self, user: str):
        self.button(text='Создать группу', callback_data=GroupCallback(user=user, action='add', group='group'))
        self.button(text='Все группы', callback_data=GroupCallback(user=user, action='list', group='groups'))
        self.adjust(1)
        return self.markup()

    def groups(self, user: str, groups: list[str]):
        for group in groups:
            self.button(text=f'{group}', callback_data=GroupCallback(user=user, action='retrieve', group=group))
        self.button(text='Добавить группу', callback_data=GroupCallback(user=user, action='add', group='group'))
        self.adjust(1)
        return self.markup()

    def subjects(self, user: str, group: str, subjects: list[str]):
        for subject in subjects:
            self.button(text=f'{subject}', callback_data=SubjectCallback(user=user, action='retrieve', group=group, subject=subject))
        self.button(text='Добавить дисциплину', callback_data=SubjectCallback(user=user, action='add', group=group, subject=subject))
        self.button(text='Назад к группам', callback_data=GroupCallback(user=user, action='list', group='groups'))
        self.adjust(1)
        return self.markup()
    
    def add_subject_result(self, user: str, group: str, subject: str):
        self.button(text='Продолжить добавление', callback_data=SubjectCallback(user=user, action='add', group=group, subject=subject))
        self.button(text='Просмотреть дисциплины', callback_data=GroupCallback(user=user, action='retrieve', group=group))
        self.button(text='Назад к группам', callback_data=GroupCallback(user=user, action='list', group='groups'))
        self.adjust(2)
        return self.markup()

    def media(self, user: str, group: str, subject: str):
        self.button(text='Добавить медиа', callback_data=MediaCallback(user=user, action='add', group=group, subject=subject))
        self.button(text='Просмотреть медиа', callback_data=MediaCallback(user=user, action='retrieve', group=group, subject=subject))
        self.button(text='Назад к дисциплинам', callback_data=GroupCallback(user=user, action='retrieve', group=group))
        self.button(text='Назад к группам', callback_data=GroupCallback(user=user, action='list', group='groups'))
        self.adjust(2,1,1)
        return self.markup()
    
    def result_add_media(self, user: str, group: str, subject: str):
        self.button(text='Добавить ещё', callback_data=MediaCallback(user=user, action='add', group=group, subject=subject))
        self.button(text='Просмотреть медиа', callback_data=MediaCallback(user=user, action='list', group=group, subject=subject))
        self.button(text='Назад к дисциплинам', callback_data=GroupCallback(user=user, action='retrieve', group=group))
        self.adjust(2)
        return self.markup()

    def list_media(self, user: str, group: str, subject: str):
        self.button(text='Предыдущие', callback_data='') #???
        self.button(text='Следующие', callback_data='') #???
        self.button(text='Добавить медиа', callback_data='') #???
        self.button(text='Назад к дисциплинам', callback_data=GroupCallback(user=user, action='list', group=group))
        self.adjust(2,1,1)
        return self.markup()

class TeacherInline(DefaultInline):
    def start(self, user:str):
        self.button(text="Все группы", callback_data=GroupCallback(user=user, action="list", group=""))
        return self.markup()

    def groups(self, user: str, groups: list[str]):
        for group in groups:
            self.button(text=f'{group}', callback_data=GroupCallback(user=user, action='retrieve', group=group))
        self.adjust(1)
        return self.as_markup()

    def subjects(self, user: str, group: str, subjects: list[str]):
        for subject in subjects:
            self.button(text=f'{subject}', callback_data=SubjectCallback(user=user, action='retrieve', group=group, subject=subject))
        self.button(text='Назад к группам', callback_data='') #???
        self.adjust(1)
        return self.as_markup()

    def media():
        pass

class StaffInline(InlineKeyboardBuilder):
    def start(self, user: AbstractUser):
        self.button(text="Отправить тикет", )
        if user.is_staff():
            self.button(text="Все группы", callback_data=GroupCallback(user=user.role(), action="list", group=""))
        if user.is_manager() or user.is_superuser():
            self.button(text="Добавить группу", callback_data=GroupCallback(user=user.role(), action="add", group=""))

    def groups(self, user: str, groups: list[str]):
        for group in groups:
            self.button(text=f'{group}', callback_data=GroupCallback(user=user, action='retrieve', group=group))
        self.adjust(1)
        return self.as_markup()