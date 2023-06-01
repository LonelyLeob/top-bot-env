from aiogram import Router, F
from aiogram.handlers import MessageHandler, CallbackQueryHandler
from datetime import datetime as dt
from aiogram.types import Message, InputMediaPhoto, InputMediaVideo, FSInputFile
from aiogram.fsm.context import FSMContext
from top_bot.core.service import Media
from top_bot.utils.callbacks import MediaCallback
from top_bot.utils.states import AddMediaState, ListMediaFiles
from top_bot.utils.keyboards import *
from .middleware import *

def dispatch():
    media = Router(name="media")
    media.message.middleware(AlbumMiddleware())
    media.callback_query.register(SetMedia, MediaCallback.filter(F.action=='add'))
    media.message.register(AddAlbum, AddMediaState.GET_MEDIA)
    media.callback_query.register(ListMedia, MediaCallback.filter(F.action=='list'))
    media.callback_query.register(SendMedia, MediaCallback.filter(F.action=='retrieve'))
    return media

class ListMedia(CallbackQueryHandler):
    async def handle(self):
        cb = MediaCallback.unpack(self.callback_data)
        media_paths = Media.list_media_paths(cb.group, cb.subject)
        return await self.bot.send_message(self.from_user.id, 'Дата указана в формате: ГГ.ММ.ДД\n'
                           'Выберите дату сохранения:',
                            reply_markup=ManagerInline().list_media_paths(group=cb.group, subject=cb.subject, media_paths=media_paths, user=cb.user, offset=0))

    
class SetMedia(CallbackQueryHandler):
    async def handle(self):
        cb = MediaCallback.unpack(self.callback_data)
        date = dt.now().strftime("%d.%m.%Y")
        state: FSMContext = self.data["state"]
        if cb.path != "":
            date = cb.path
            await state.update_data(group=cb.group, subject=cb.subject, date=date, user=cb.user)
            await self.message.answer('Папка уже была создана ранее. Отправьте медиа файл')
            return await state.set_state(AddMediaState.GET_MEDIA)
        elif Media.create_media_path(cb.group, cb.subject, date):
            await state.update_data(group=cb.group, subject=cb.subject, date=date, user=cb.user)
            await self.message.answer('Папка на текущую дату создана. Отправьте медиа файл')
            return await state.set_state(AddMediaState.GET_MEDIA)
        return await self.message.answer("Произошла ошибка, обратитесь к системному администратору!")

class AddAlbum(MessageHandler):
    async def handle(self):
        state: FSMContext = self.data["state"]
        album: list[Message] = self.data["album"]
        context = await state.get_data()
        for msg in album:
            if msg.photo:
                file_id = msg.photo[-1].file_id
            elif msg.video:
                file_id = msg.video.file_id
            elif msg.document:
                file_id = msg.document.file_id
            file = await self.bot.get_file(file_id)
            pathname = file.file_path.split("/")
            path = Media.save_media_path(group=context['group'], subject=context['subject'], filename=pathname[1], date=context["date"] if 'date' in context.keys() else dt.now().strftime("%d.%m.%Y"))
            await self.bot.download_file(file.file_path, path)
        return await self.bot.send_message(self.from_user.id, f'Ваш файл успешно сохранен в директорию', 
                                            reply_markup=ManagerInline().result_add_media(group=context["group"], subject=context["subject"], user=context["user"], offset='0', path=dt.now().strftime("%d.%m.%Y")))

class SendMedia(CallbackQueryHandler):
    async def handle(self):
        state: FSMContext = self.data["state"]
        cb = MediaCallback.unpack(self.callback_data)
        user = cb.user
        date = cb.path
        group = cb.group
        subject = cb.subject
        offset = cb.offset
        path = Media.get_media_path(group,subject,date)
        media_objects = Media.list_media_files(group, subject, date)
        media = []
        photos = ['jpg', 'png', 'jpeg']
        offset = Media.offset_generator(offset)
        if len(media_objects) == 0:
            await self.bot.send_message(self.from_user.id, 
                                'На данную дату не сохранено ни одного медиа файла.\n'
                                'Выберите действие',
                                reply_markup=ManagerInline().list_media_files(group=group, subject=subject, offset=str(offset), user=user, path=date))
        elif int(offset) < 0:
            await self.bot.send_message(self.from_user.id, 'Вам отправлены первые фото')
            offset = 0
        elif len(media_objects) - int(offset) <= 0:
            await self.bot.send_message(self.from_user.id, 'Вам отправленны последние фото')
        else:
            if len(media_objects) - int(offset) < 5 and len(media_objects) - int(offset) != 0:
                last_files = len(media_objects) % 5
                media_objects = media_objects[int(offset):int(offset)+last_files]
            else:
                media_objects = media_objects[int(offset):int(offset)+5]
            for object in media_objects:
                if object.split('.')[-1] in photos:
                    file = InputMediaPhoto(type='photo', media=FSInputFile(Media.get_media_file(group,subject,date,object)))
                    media.append(file)
                else:
                    file = InputMediaVideo(type='video', media=FSInputFile(Media.get_media_file(group,subject,date,object)))
                    media.append(file)
            await self.bot.send_media_group(self.from_user.id, media)
            await self.bot.send_message(self.from_user.id, 'Выберите действие:',
                                reply_markup=ManagerInline().list_media_files(group=group, subject=subject, offset=str(offset), user=user, path=date))
            await state.update_data(path=path, group=group, subject=subject, me=user)
            await state.set_state(ListMediaFiles.CHOICE_ACTION)