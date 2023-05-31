from aiogram.handlers import MessageHandler, CallbackQueryHandler
from aiogram import Router, F, Bot
from top_bot.core.io import base
from top_bot.utils.callbacks import SubjectCallback, GroupCallback
from top_bot.utils.keyboards import *
from top_bot.core.service import Subjects
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from top_bot.utils.states import *

def dispatch() -> Router:
    subjects = Router(name="subjects")
    subjects.callback_query.register(ListSubjects, GroupCallback.filter(F.action=='retrieve'))
    subjects.callback_query.register(RetrieveSubject, SubjectCallback.filter(F.action=='retrieve'))
    subjects.callback_query.register(CreateSubjects, SubjectCallback.filter(F.action=='add'))
    subjects.message.register(SetSubjectName, AddSubjectState.GET_NAME)
    return subjects

class ListSubjects(CallbackQueryHandler):
    async def handle(self):
        cb = GroupCallback.unpack(self.callback_data)
        subjects = Subjects.list_subjects(cb.group)
        await self.bot.send_message(self.from_user.id, 
                                    f'Вы выбрали группу: {cb.group}\n'
                                    'Список дисциплин:',
                                    reply_markup=ManagerInline().subjects(user=cb.user, group=cb.group, subjects=subjects))
    
class RetrieveSubject(CallbackQueryHandler):
    async def handle(self):
        cb = SubjectCallback.unpack(self.callback_data)
        await self.bot.send_message(self.from_user.id,
                                    f'Вы выбрали дисциплину: {cb.subject}\n'
                                    'Выберите действие:',
                                    reply_markup=ManagerInline().media(user=cb.user, group=cb.group, subject=cb.subject))
    

async def CreateSubjects(cb: CallbackQuery, bot: Bot, state: FSMContext):
        cb_data = SubjectCallback.unpack(cb.data)
        await bot.send_message(cb.from_user.id, 
                               'Введите название дисциплины, если их несколько то вводите через Enter\n'
                               'Пример:\n'
                               'PythonJun\n'
                               'PythonMid\n'
                               'И т.д.')
        await state.update_data(user=cb_data.user, group=cb_data.group)
        return await state.set_state(AddSubjectState.GET_NAME)


async def SetSubjectName(message: Message, bot: Bot, state: FSMContext):
    context = await state.get_data()
    subjects = message.text.split('\n')
    k = 0
    for subject in subjects:
        try:
            Subjects.create_subject(context['group'], subject)
        except Exception:
            k += 1
    if k == len(subjects):
        await bot.send_message(message.from_user.id, 'Данные дисциплины уже существуют, введите название ещё раз или веберите действие',
                               reply_markup=ManagerInline().add_subject_result(user=context['user'], group=context['group'], subject='subjects'))
        
    elif k == 0 and (len(subjects) == 1 or len(subjects) >= 1):
        await bot.send_message(message.from_user.id, 'Добавление дисциплины прошло успешно',
                               reply_markup=ManagerInline().add_subject_result(user=context['user'], group=context['group'], subject='subjects'))
    
    else:
        await bot.send_message(message.from_user.id, f'{str(k)} из перечислинных дисциплин уже существует, остальные были созданы успешно',
                               reply_markup=ManagerInline().add_subject_result(user=context['user'], group=context['group'], subject='subjects'))
        
    