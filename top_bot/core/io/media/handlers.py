from aiogram import Router, Bot, F
from aiogram.handlers import MessageHandler, CallbackQueryHandler
from datetime import date as dt
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputMediaVideo, FSInputFile
from aiogram.fsm.context import FSMContext
from top_bot.core.service import Media
from top_bot.utils.callbacks import MediaCallback
from top_bot.utils.states import AddMediaState, ListMediaFiles
from top_bot.utils.keyboards import *
from .middleware import *

def dispatch():
    media = Router(name="media")
    media.message.middleware(AlbumMiddleware())
    media.callback_query.register(AddMedia, MediaCallback.filter(F.action=='add'))
    media.message.register(handle_albums, AddMediaState.GET_MEDIA)
    media.callback_query.register(ListMedia, MediaCallback.filter(F.action=='list_media'))
    media.callback_query.register(SendMedia, MediaCallback.filter(F.action=='retrieve'))
    return media

class ListMedia(CallbackQueryHandler):
    async def handle(self):
        cb = MediaCallback.unpack(self.callback_data)
        media_paths = Media.list_media_paths(cb.group, cb.subject)
        return await self.bot.send_message(self.from_user.id, 'Дата указана в формате: ГГ.ММ.ДД\n'
                           'Выберите дату сохранения:',
                            reply_markup=ManagerInline().list_media_paths(group=cb.group, subject=cb.subject, media_paths=media_paths, user=cb.user, offset='0'))

    
async def AddMedia(cb: CallbackQuery, state: FSMContext):
    cb_data = MediaCallback.unpack(cb.data)
    date = dt.today().__str__()
    if Media.create_media_path(cb_data.group, cb_data.subject, date):
        await state.update_data(group=cb_data.group, subject=cb_data.subject, date=date, user=cb_data.user)
        await cb.message.answer('Отправьте медиа файл')
        await state.set_state(AddMediaState.GET_MEDIA)
        return
    await cb.message.answer("Произошла ошибка, обратитесь к системному администратору!")

async def handle_albums(message: Message, state:FSMContext, bot: Bot, album: dict[str, list[Message]]):
    context = await state.get_data()
    for obj in album:
        if obj.photo:
            file_id = obj.photo[-1].file_id
        elif obj.video:
            file_id = obj.video.file_id
        else:
            file_id = obj.document.file_id

        try:
            file = await bot.get_file(file_id)
            pathname = file.file_path.split("/")
            await bot.download_file(file.file_path, 
                                    Media.save_media_path(context['group'], context['subject'], pathname[1], context["path"] if 'path' in context.keys() else dt.today().__str__()))
            
        except ValueError:
            return await message.answer("Произошла ошибка, обратитесь к системному администратору")
        offset = '0'
    await bot.send_message(message.from_user.id, f'Ваш файл успешно сохранен в директорию', 
                                         reply_markup=ManagerInline().result_add_media(group=context["group"], subject=context["subject"], user=context["user"], offset=offset, path=dt.today().__str__()))



async def SendMedia(callback: CallbackQuery, bot: Bot, state: FSMContext):
    cb = MediaCallback.unpack(callback.data)
    user = cb.user
    date = cb.path
    group = cb.group
    subject = cb.subject
    offset = cb.offset
    path = Media.get_media_path(group,subject,date)
    media_objects = Media.list_media_files(group, subject, date)
    media = []
    photos = ['jpg', 'png', 'jpeg']
    offset, sign = Media.offset_generator(offset)
    if int(offset) < 0:
        await bot.send_message(callback.from_user.id, 'Вам отправлены первые фото')
        offset = 0
    elif len(media_objects) - int(offset) <= 0:
        await bot.send_message(callback.from_user.id, 'Вам отправленны последние фото')
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
        await bot.send_media_group(callback.from_user.id, media)
        await bot.send_message(callback.from_user.id, 'Выберите действие:',
                            reply_markup=ManagerInline().list_media_files(group,subject,str(offset),user,date))
        await state.update_data(path=path, group=group, subject=subject, me=user)
        await state.set_state(ListMediaFiles.CHOICE_ACTION)