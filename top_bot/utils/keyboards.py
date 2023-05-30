from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
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
    
    def menu(self, user: str):
        self.button(text='Создать группу', callback_data=DefaultCallback(user=user, action='add'))
        self.button(text='Все группы', callback_data=DefaultCallback(user=user, action='list'))
        self.adjust(1)
        return self.as_markup()

    def groups(self, user: str, groups: list[str]):
        for group in groups:
            self.button(text=f'{group}', callback_data=GroupCallback(user=user, action='retrieve', group=group))
        self.button(text='Назад к меню', callback_data='') #???
        self.adjust(1)
        return self.as_markup()

    def subjects(self, user: str, group: str, subjects: list[str]):
        for subject in subjects:
            self.button(text=f'{subject}', callback_data=SubjectCallback(user=user, action='retrieve', group=group, subject=subject))
        self.button(text='Назад к группам', callback_data=DefaultCallback(user=user, action='list'))
        self.adjust(1)
        return self.as_markup()

    def media(self, user: str, group: str, subject: str):
        self.button(text='Добавить медиа', callback_data=MediaCallback(user=user, action='add', group=group, subject=subject))
        self.button(text='Просмотреть медиа', callback_data=MediaCallback(user=user, action='retrieve', group=group, subject=subject))
        self.adjust(2)
        return self.as_markup()
    
    def result_add_media(self, user: str, group: str, subject: str):
        self.button(text='Добавить ещё', callback_data='') #???
        self.button(text='Просмотреть медиа', callback_data='') #???
        self.button(text='Назад к дисциплинам', callback_data=GroupCallback(user=user, action='retrieve', group=group))
        self.adjust(2)
        return self.as_markup()

    def list_media(self, user: str, group: str, subject: str):
        self.button(text='Предыдущие', callback_data='') #???
        self.button(text='Следующие', callback_data='') #???
        self.button(text='Добавить медиа', callback_data='') #???
        self.button(text='Назад к дисциплинам', callback_data=GroupCallback(user=user, action='retrieve', group=group))
        self.adjust(2,1,1)
        return self.as_markup()

class TeacherInline(DefaultInline):
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