from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

class DefaultInline(InlineKeyboardBuilder):
    def markup(self) -> InlineKeyboardMarkup:
        """alias for as_markup function"""
        return self.as_markup()

class StartInline(DefaultInline):
    def start():
        pass

class AdminInline(DefaultInline):
    def apply(self):
        pass
    
    def groups(self):
        pass

    def subjects(self):
        pass

    def media(self):
        pass

class TeacherInline(DefaultInline):
    def groups():
        pass

    def subjects():
        pass

    def media():
        pass