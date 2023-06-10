from typing import Any
from aiogram.filters.callback_data import CallbackData


    #agree = 0
    #decline = 1
    #apply = 2
class StartCallback(CallbackData, prefix="request"):
    action: int
    user: str
    #add = "add"
    #list = "list"
class DefaultCallback(CallbackData, prefix='default'):
    action: str

class GroupCallback(DefaultCallback, prefix="group"):
    group: str

class SubjectCallback(GroupCallback, prefix="subject"):
    subject: str

class MediaCallback(SubjectCallback, prefix="media"):
    path: str
    offset: str