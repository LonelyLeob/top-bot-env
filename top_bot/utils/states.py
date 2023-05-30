from aiogram.fsm.state import StatesGroup, State

class AddGroupState(StatesGroup):
    GET_TITLE = State()
    GET_SUBJECTS = State()
    GET_RESULT = State()


class AddMediaState(StatesGroup):
    GET_MEDIA = State()
    GET_RESULT = State()
    
class ListMedia(StatesGroup):
    CHOICE_ACTION = State()
    ADD_MEDIA = State()

class AddSubjectState(StatesGroup):
    GET_NAME = State()