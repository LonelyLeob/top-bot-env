from top_bot.core.models import *
from top_bot.core.settings import settings

def get_user(user_id: int):
    if user_id == settings.bots.admin_id:
        return Admin()
    
    elif user_id == settings.bots.manager_id:
        return Manager()

    return Anonymous()