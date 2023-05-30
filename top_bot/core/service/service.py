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
    def create_media_path(group: str, subject: str, title: str):
        return os.mkdir(os.path.join(settings.bots.media_store, group, subject, title))
    
    def list_media_paths(group: str, subject: str):
        return os.listdir(os.path.join(group, subject))
    
    def list_media_files(group: str, subject: str, title: str):
        return os.listdir(os.path.join(group, subject, title))