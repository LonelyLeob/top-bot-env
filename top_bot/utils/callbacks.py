from typing import Any
from aiogram.filters.callback_data import CallbackData


    #agree = 0
    #decline = 1
    #apply = 2
class StartCallback(CallbackData, prefix="request"):
    user: int
    action: int
    #add = "add"
    #list = "list"
class DefaultCallback(CallbackData, prefix='default'):
    user: str
    action: str

class GroupCallback(DefaultCallback, prefix="group"):
    group: str

class SubjectCallback(GroupCallback, prefix="subject"):
    subject: str

class MediaCallback(SubjectCallback, prefix="media"):
    action: str