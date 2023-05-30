import sys
import os
from pathlib import Path
from environs import Env
from dataclasses import dataclass

@dataclass
class Bots:
    bot_token: str
    admin_id: int
    media_store: str
    manager_id: int
    user_accessed_list: str
    error_log: str



@dataclass
class Settings:
    bots: Bots



def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str('TOKEN'),
            admin_id=env.int('ADMIN_ID'),
            media_store=os.path.join(Path(__file__).parent.parent, "data", env.str("MEDIA_STORE")),
            manager_id=env.int("MANAGER_ID"),
            user_accessed_list=os.path.join(Path(__file__).parent.parent, "data", env.str("USERS_LIST")),
            error_log=os.path.join(Path(__file__).parent.parent, "logs", env.str("ERROR_LOG"))
        )
    )

settings = get_settings(sys.argv[1])