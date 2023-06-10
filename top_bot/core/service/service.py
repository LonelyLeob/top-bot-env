from top_bot.core.settings import settings
import os

class Auth:
    def is_teacher(user_id: int) -> bool:
        with open(settings.bots.users_list, 'r') as users_list:   
            for user in users_list:
                        if str(user_id) in str(user):
                            return True
            return False
        
    def is_manager(user_id: int) -> bool:
        if user_id == settings.bots.manager_id:
            return True
        return False
    
    def create_user(user_id: str) -> bool:
        try:
            with open(settings.bots.users_list, 'a') as user_list:
                    user_list.write(user_id +',')
                    return True
        except Exception:
            return False

class Groups:
    def create_group(title: str):
        return os.mkdir(os.path.join(settings.bots.media_store, title))

    def list_groups():
        return os.listdir(settings.bots.media_store)

class Subjects:
    def create_subject(group: str, title: str) -> bool:
        try:
            os.mkdir(os.path.join(settings.bots.media_store, group, title))
            return True
        except Exception:
            return False


    def list_subjects(group: str):
        return os.listdir(os.path.join(settings.bots.media_store, group))
    
class Media():
    def create_media_path(group: str, subject: str, date: str) -> bool:
        try:
            os.mkdir(os.path.join(settings.bots.media_store, group, subject, date))
            return True
        except FileExistsError:
            return True
        except Exception:
            return False
    
    def save_media_path(group: str, subject: str, filename: str, date: str):
        return os.path.join(settings.bots.media_store, group, subject, date, filename)

    def list_media_paths(group: str, subject: str):
        return os.listdir(os.path.join(settings.bots.media_store ,group, subject))
    
    def list_media_files(group: str, subject: str, date: str):
        return os.listdir(os.path.join(settings.bots.media_store,group, subject, date))
    
    def get_media_path(group: str, subject: str, date: str):
        return os.path.join(settings.bots.media_store, group, subject, date)
    
    def get_media_file(group: str, subject: str, date: str, file: str):
        return os.path.join(settings.bots.media_store, group, subject, date, file)
    
    def offset_generator(offset: str) -> int:
        if '+' in offset:
            offset = offset.split('+')
            offset = int(offset[0]) + int(offset[1])
            return int(offset)
        elif '-' in offset:
            offset = offset.split('-')
            offset = int(offset[0]) - int(offset[1])
            return int(offset)
        else:
            return 0