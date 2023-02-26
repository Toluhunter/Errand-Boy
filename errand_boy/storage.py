import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage

class OverWriteStorage(FileSystemStorage):

    def get_available_name(self, name, *args, **kwargs):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name