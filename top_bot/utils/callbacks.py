from aiogram.filters.callback_data import CallbackData
from enum import Enum

class Action(str, Enum):
    add = "add"
    list = "list"
    retrieve = "retrieve"

class DefaultCallback(CallbackData):
    user: str
    action: Action

class GroupCallback(DefaultCallback, prefix="group"):
    group: str

class SubjectCallback(GroupCallback, prefix="subject"):
    subject: str

class MediaCallback(SubjectCallback, prefix="media"):
    action: str