from typing import Any
from aiogram.handlers import MessageHandler, CallbackQueryHandler
from aiogram import Router, F, Bot
from top_bot.core.io import base
from top_bot.utils.callbacks import SubjectCallback, GroupCallback
from top_bot.utils.keyboards import *
from top_bot.core.service import Subjects, Auth
from aiogram.fsm.context import FSMContext
from top_bot.utils.states import *
from top_bot.core.settings import settings

def dispatch() -> Router:
    subjects = Router(name="subjects")
    subjects.callback_query.register(ListSubjects, GroupCallback.filter(F.action=='retrieve'))
    subjects.callback_query.register(RetrieveSubject, SubjectCallback.filter(F.action=='retrieve'))
    subjects.callback_query.register(CreateSubjects, SubjectCallback.filter(F.action=='add'))
    subjects.callback_query.register(ConfirmationDestroySubject, SubjectCallback.filter(F.action=='destroy'))
    subjects.callback_query.register(DestroySubject, SubjectCallback.filter(F.action=='confirm_destroy'))
    subjects.message.register(SetSubjectName, AddSubjectState.GET_NAME)
    return subjects

class ListSubjects(CallbackQueryHandler):
    async def handle(self):
        await self.message.delete()
        cb = GroupCallback.unpack(self.callback_data)
        subjects = Subjects.list_subjects(cb.group)
        user_id = int(self.from_user.id)
        if Auth.is_manager(user_id):
            return await self.bot.send_message(chat_id=user_id, 
                                            text=f'Вы выбрали группу: {cb.group}\n'
                                            'Список дисциплин:',
                                            reply_markup=ManagerInline().subjects(group=cb.group, subjects=subjects))
        elif Auth.is_teacher(str(user_id)):
            return await self.bot.send_message(chat_id=user_id,
                                                text=f"Вы выбрали группу: {cb.group}\n"
                                                'Cписок дисциплин:', 
                                                reply_markup=TeacherInline().subjects(group=cb.group, subjects=subjects))
        return await self.bot.send_message(chat_id=user_id,
                                               text='Вы не прошли авторизацию, пожалуйста подайте заявку', 
                                                reply_markup=StartInline().start(user=self.from_user.id))
    
class RetrieveSubject(CallbackQueryHandler):
    async def handle(self):
        await self.message.delete()
        cb = SubjectCallback.unpack(self.callback_data)
        if Auth.is_manager(self.from_user.id):
            return await self.bot.send_message(self.from_user.id,
                                        f'Вы выбрали дисциплину: {cb.subject}\n'
                                        'Выберите действие:',
                                        reply_markup=ManagerInline().media(group=cb.group, subject=cb.subject))
        else:
             return await self.bot.send_message(self.from_user.id,
                                        f'Вы выбрали дисциплину: {cb.subject}\n'
                                        'Выберите действие:',
                                        reply_markup=TeacherInline().media(group=cb.group, subject=cb.subject))
    
class CreateSubjects(CallbackQueryHandler):
    async def handle(self):
            await self.message.delete()
            state: FSMContext = self.data["state"]
            cb = SubjectCallback.unpack(self.callback_data)
            await self.bot.send_message(self.from_user.id, 
                                'Введите название дисциплины, если их несколько то вводите через Enter\n'
                                'Пример:\n'
                                'PythonJun\n'
                                'PythonMid\n'
                                'И т.д.')
            await state.update_data(group=cb.group)
            return await state.set_state(AddSubjectState.GET_NAME)


class SetSubjectName(MessageHandler):
    async def handle(self):
        state: FSMContext = self.data["state"]
        context = await state.get_data()
        subjects = self.event.text.split('\n')
        k = 0
        for subject in subjects:
            if not (Subjects.create_subject(context['group'], subject)):
                k += 1
        if k == len(subjects):
            await self.bot.send_message(self.from_user.id, 'Данные дисциплины уже существуют, введите название ещё раз или веберите действие',
                                reply_markup=ManagerInline().add_subject_result(group=context['group'], subject='subjects'))
            
        elif k == 0 and (len(subjects) == 1 or len(subjects) >= 1):
            await self.bot.send_message(self.from_user.id, 'Добавление дисциплины прошло успешно',
                                reply_markup=ManagerInline().add_subject_result(group=context['group'], subject='subjects'))
        
        else:
            await self.bot.send_message(self.from_user.id, f'{str(k)} из перечислинных дисциплин уже существует, остальные были созданы успешно',
                                reply_markup=ManagerInline().add_subject_result(group=context['group'], subject='subjects'))

class ConfirmationDestroySubject(CallbackQueryHandler):
      async def handle(self):
            self.message.delete()
            cb = SubjectCallback.unpack(self.callback_data)
            return await self.bot.send_message(self.from_user.id,f'Вы уверенны, что хотите удалить дисциплину {cb.subject}?',
                                               reply_markup=ManagerInline().confirmation_destroy_subject(group=cb.group, subject=cb.subject))

class DestroySubject(CallbackQueryHandler):
      async def handle(self):
            self.message.delete()
            cb = SubjectCallback.unpack(self.callback_data)
            if Subjects.destroy_subject(group=cb.group,subject=cb.subject):
                subjects = Subjects.list_subjects(cb.group)
                return await self.bot.send_message(self.from_user.id, 'Удаление дисциплины прошло успешно, список существующих дисциплин:',
                                                reply_markup=ManagerInline().subjects(group=cb.group, subjects=subjects))
            else:
                subjects = Subjects.list_subjects(cb.group)
                return await self.bot.send_message(self.from_user.id, 
                                                   'При удалении дисциплины произошла непредвиденная ошибка, обратитесь к ситстемному администратору\n'
                                                   'Вы можете прейти к работе с другой дисциплиной',
                                                   reply_markup=ManagerInline().subjects(group=cb.group, subjects=subjects))
    
