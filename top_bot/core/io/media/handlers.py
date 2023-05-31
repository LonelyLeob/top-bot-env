from aiogram import Router, Bot, F
from aiogram.handlers import MessageHandler, CallbackQueryHandler
from datetime import date as dt
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from top_bot.core.service import Media
from top_bot.utils.callbacks import MediaCallback
from top_bot.utils.states import AddMediaState, ListMedia

def dispatch():
    media = Router(name="media")
    media.callback_query.register(AddMedia, MediaCallback.filter(F.action=='add'))
    return media

class ListMedia(CallbackQueryHandler):
    async def handle(self):
        return await super().handle()
    
async def AddMedia(cb: CallbackQuery, state: FSMContext):
    cb_data = MediaCallback.unpack(cb.data)
    date = dt.today().__str__()
    if Media.create_media_path(cb_data.group, cb_data.subject, date):
        await state.update_data(group=cb_data.group, subject=cb_data.subject, date=date, user=cb_data.user)
        await cb.message.answer('Отправьте медиа файл')
        await state.set_state(AddMediaState.GET_MEDIA)
        return
    await cb.message.answer("Произошла ошибка, обратитесь к системному администратору!")

# async def handle_albums(message: Message, state:FSMContext, bot: Bot, album: dict[str, list[Message]]):
#     context = await state.get_data()
#     for obj in album:
#         if obj.photo:
#             file_id = obj.photo[-1].file_id
#         elif obj.video:
#             file_id = obj.video.file_id
#         else:
#             file_id = obj.document.file_id

#         try:
#             file = await bot.get_file(file_id)
#             pathname = file.file_path.split("/")
#             await bot.download_file(file.file_path, media_path(context['group'], context['subject'], pathname[1], context["path"] if 'path' in context.keys() else dt.today().__str__()))
            
#         except ValueError:
#             return await message.answer("Произошла ошибка, обратитесь к системному администратору")
#     offset = 0
#     await bot.send_message(message.from_user.id, f'Ваш файл успешно сохранен в директорию', 
#                                         reply_markup=keyboards.save_media_result(context["group"], context["subject"], context["me"], offset, dt.today().__str__()))
    