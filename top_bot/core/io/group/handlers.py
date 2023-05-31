from typing import Any
from aiogram import Router, F, Bot
from aiogram.handlers import MessageHandler, CallbackQueryHandler
from aiogram.fsm.context import FSMContext
from top_bot.utils.callbacks import *
from top_bot.core.service import *
from top_bot.utils.keyboards import *
from top_bot.utils.states import *
from aiogram.types import Message, CallbackQuery



def dispatch() -> Router:
    groups = Router(name="groups")
    groups.callback_query.register(ListGroups, GroupCallback.filter(F.action=="list"))
    groups.callback_query.register(CreateGroup, GroupCallback.filter(F.action=="add"))
    groups.message.register(SetGroupTitle, AddGroupState.GET_TITLE)
    groups.message.register(SetSubjects, AddGroupState.GET_SUBJECTS)
    groups.message.register(ResultCreateGroup, AddGroupState.GET_RESULT)
    return groups

class ListGroups(CallbackQueryHandler):
        async def handle(self):
                cb = GroupCallback.unpack(self.callback_data)
                groups = Groups.list_groups() 
                if len(groups) > 0:
                        return await self.bot.send_message(cb.user, "Выберите следующее действие: ", reply_markup=ManagerInline().groups(user=cb.user, groups=groups))
                else:
                        return await self.bot.send_message(cb.user,"Групп не найдено", reply_markup=ManagerInline().start(user=cb.user))
 
async def CreateGroup(cb: CallbackQuery, bot: Bot, state: FSMContext):
                cb = GroupCallback.unpack(cb.data)
                await bot.send_message(cb.user, 'Введите название группы!')
                await state.update_data(user=cb.user)
                
                return await state.set_state(AddGroupState.GET_TITLE)
        

async def SetGroupTitle( message: Message, bot: Bot, state: FSMContext):
                title = message.text
                await bot.send_message(message.from_user.id, 
                                        'Введите название дисциплин разделяя их через Enter.\n'
                                        'Пример:\n'
                                        'PythonJun\n'
                                        'PythonMid\n'
                                        'И так далее')
                await state.update_data(title=title)
                return await state.set_state(AddGroupState.GET_SUBJECTS)


async def SetSubjects( message: Message, bot: Bot, state: FSMContext):
        await state.update_data(subjects=message.text)
        context = await state.get_data()
        await message.answer(
            "Если данные указаны верно отправьте сообщение: Да\n"
            "Если вы допустили ошибку то отправьте сообщение: Нет\n"
            "Данные новой группы:\n"
            f"Название: {context['title']}\n"
            "Дисциплины:\n"
            f"{context['subjects']}"
            )
        return await state.set_state(AddGroupState.GET_RESULT) 


async def ResultCreateGroup(message: Message, bot: Bot, state: FSMContext):
        context =  await state.get_data()
        if 'да' in message.text.lower():
            Groups.create_group(title=context['title'])
            subjects = context['subjects'].split('\n')
            for subject in subjects:
                Subjects.create_subject(group=context['title'], title=subject)
            return await bot.send_message(message.from_user.id, 'Создание группы прошло успешно!\n'
                                               'Выберите действие над группой', reply_markup=ManagerInline().subjects(user=context['user'],group=context['title'],subjects=subjects))
        else:
            return await bot.send_message(message.from_user.id, 
                                               'Отменяю создание группы\n'
                                               'Выберите действие:',
                                               reply_markup=ManagerInline().start(user=context['user']) if (context['user'] == 'manager') or (context['user'] == 'admin')
                                               else ManagerInline().start(user=context['user']))