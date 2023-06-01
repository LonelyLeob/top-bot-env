from top_bot.core.settings import settings
import os

class Groups():
    def create_group(title: str):
        return os.mkdir(os.path.join(settings.bots.media_store, title))

    def list_groups():
        return os.listdir(settings.bots.media_store)

class Subjects():
    def create_subject(group: str, title: str):
        return os.mkdir(os.path.join(settings.bots.media_store, group, title))
    
    def list_subjects(group: str):
        return os.listdir(os.path.join(settings.bots.media_store, group))
    
class Media():
    def create_media_path(group: str, subject: str, date: str) -> bool:
        try:
            os.mkdir(os.path.join(settings.bots.media_store, group, subject, date))
        except FileExistsError:
            return True
        except Exception:
            return False
        return True
    
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
    
    def offset_generator(offset: str):
        if '+' in offset:
            offset = offset.split('+')
            offset = int(offset[0]) + int(offset[1])
            sign = '+'
            return int(offset), sign
        elif '-' in offset:
            offset = offset.split('-')
            offset = int(offset[0]) - int(offset[1])
            sign = '-'
            return int(offset), sign
        else:
            return '0', '+'