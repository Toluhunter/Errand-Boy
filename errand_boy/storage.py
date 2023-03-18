import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class OverWriteStorage(FileSystemStorage):
    '''
        Subclass of filesystem storage, designed to overwrite existing file
        '''

    def get_available_name(self, name, *args, **kwargs):
        '''
        if file already exists delete exisitng file and return back the name of the file to be written again
        '''

        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name
