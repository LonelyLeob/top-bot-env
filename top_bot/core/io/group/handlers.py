from typing import Any
from aiogram import Router, F, Bot
from aiogram.handlers import MessageHandler, CallbackQueryHandler
from aiogram.fsm.context import FSMContext
from top_bot.utils.callbacks import *
from top_bot.core.service import *
from top_bot.utils.keyboards import *
from top_bot.utils.states import *


def dispatch() -> Router:
    groups = Router(name="groups")
    groups.callback_query.register(ListGroups, GroupCallback.filter(F.action=="list"))
    groups.callback_query.register(CreateGroup, GroupCallback.filter(F.action=="add"))
    groups.callback_query.register(ConfirmationDestroyGroup, GroupCallback.filter(F.action=='destroy'))
    groups.callback_query.register(DestroyGroup, GroupCallback.filter(F.action=='confirm_destroy'))
    groups.message.register(SetGroupTitle, AddGroupState.GET_TITLE)
    groups.message.register(SetSubjects, AddGroupState.GET_SUBJECTS)
    groups.message.register(ResultCreateGroup, AddGroupState.GET_RESULT)
    return groups

class ListGroups(CallbackQueryHandler):
        async def handle(self):
                await self.message.delete()
                groups = Groups.list_groups() 
                if len(groups) > 0:
                        if Auth.is_manager(self.from_user.id):
                            return await self.bot.send_message(self.from_user.id, "Выберите следующее действие: ", reply_markup=ManagerInline().groups(groups=groups))
                        elif Auth.is_teacher(self.from_user.id):
                            return await self.bot.send_message(self.from_user.id, "Выберите следующее действие: ", reply_markup=TeacherInline().groups(groups=groups))
                        else:
                            return await self.bot.send_message(self.from_user.id, 'Вы не прошли регистрацию. Подайте заявку', reply_markup=StartInline().start(user=self.from_user.id))             
                else:
                        return await self.bot.send_message(self.from_user.id, "Групп не найдено", reply_markup=ManagerInline().start())
 
class CreateGroup(CallbackQueryHandler):
    async def handle(self):
                    self.message.delete()
                    state: FSMContext = self.data["state"]
                    await self.bot.send_message(self.from_user.id, 'Введите название группы!')
                
                    return await state.set_state(AddGroupState.GET_TITLE)
        
class SetGroupTitle(MessageHandler):
    async def handle(self):
                    list_groups = Groups.list_groups()
                    state: FSMContext = self.data["state"]
                    title = self.event.text
                    if title in list_groups:
                        await state.clear()
                        return await self.bot.send_message(self.from_user.id, 'Группа с таким названием уже существует! Выеберите действие:', reply_markup=ManagerInline().start())
                    else:
                        await self.bot.send_message(self.from_user.id, 
                                                'Введите название дисциплин разделяя их через Enter.\n'
                                                'Пример:\n'
                                                'PythonJun\n'
                                                'PythonMid\n'
                                                'И так далее')
                        await state.update_data(title=title)
                        return await state.set_state(AddGroupState.GET_SUBJECTS)

class SetSubjects(MessageHandler):
    async def handle(self):
            state: FSMContext = self.data["state"]
            await state.update_data(subjects=self.event.text)
            context = await state.get_data()
            if Subjects.validation_subjects(subjects=self.event.text.split('\n')):
                await self.bot.send_message(self.from_user.id,
                    "Если данные указаны верно отправьте сообщение: Да\n"
                    "Если вы допустили ошибку то отправьте сообщение: Нет\n"
                    "Данные новой группы:\n"
                    f"Название: {context['title']}\n"
                    "Дисциплины:\n"
                    f"{context['subjects']}"
                    )
                return await state.set_state(AddGroupState.GET_RESULT) 
            else:
                return await self.bot.send_message(self.from_user.id, 'В перечисленных дисциплинах найдены дубликаты, пожалуйста перечислите дисциплины снова')
                

class ResultCreateGroup(MessageHandler):
    async def handle(self):
            state: FSMContext = self.data["state"]
            context =  await state.get_data()
            if 'да' in self.event.text.lower():
                Groups.create_group(title=context['title'])
                subjects = context['subjects'].split('\n')
                for subject in subjects:
                    Subjects.create_subject(group=context['title'], title=subject)
                await state.clear()
                return await self.bot.send_message(self.from_user.id, 'Создание группы прошло успешно!\n'
                                                    'Выберите действие над группой', reply_markup=ManagerInline().subjects(group=context['title'],subjects=subjects))
                
            else:
                await state.clear()
                return await self.bot.send_message(self.from_user.id, 
                                                'Отменяю создание группы\n'
                                                'Выберите действие:',
                                                reply_markup=ManagerInline().start())
            
class ConfirmationDestroyGroup(CallbackQueryHandler):
      async def handle(self):
            self.message.delete()
            cb = GroupCallback.unpack(self.callback_data)
            return await self.bot.send_message(self.from_user.id,f'Вы уверенны, что хотите удалить группу {cb.group}?',
                                               reply_markup=ManagerInline().confirmation_destroy_group(group=cb.group))

class DestroyGroup(CallbackQueryHandler):
      async def handle(self):
            self.message.delete()
            cb = GroupCallback.unpack(self.callback_data)
            if Groups.destroy_group(cb.group):
                groups = Groups.list_groups()
                return await self.bot.send_message(self.from_user.id, 'Удаление группы прошло успешно, список существующих групп:',
                                                reply_markup=ManagerInline().groups(groups=groups))
            else:
                groups = Groups.list_groups()
                return await self.bot.send_message(self.from_user.id, 
                                                   'При удалении группы произошла непредвиденная ошибка, обратитесь к ситстемному администратору\n'
                                                   'Вы можете прейти к работе с другой группой',
                                                   reply_markup=ManagerInline().groups(groups=groups))