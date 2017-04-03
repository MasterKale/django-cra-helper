import os

from django.core.files.storage import FileSystemStorage
from django.core.checks import Error


class SingleFileStorage(FileSystemStorage):
    '''
    This class allows for a reference to an individual file to be held while the staticfiles
    module attempts to collect static files for deployment.

    To use it, just pass an absolute path to the desired file as `location`
    '''
    def __init__(self, location=None, base_url=None, file_permissions_mode=None,
                 directory_permissions_mode=None):
        self._file_path = ''
        self._file_name = ''

        if os.path.isfile(location):
            # Separate the path from the filename
            self._file_path, self._file_name = os.path.split(location)
        else:
            # This class won't work if `location` doesn't point to an actual file
            raise IOError('Path should point to an existing file')

        # Pass in the folder so this acts like a typical FileSystemStorage that needs a path
        super().__init__(
            self._file_path,
            base_url,
            file_permissions_mode,
            directory_permissions_mode
        )

    def listdir(self, path):
        '''
        Return the file name as the sole file that needs to be collected from the specified path
        '''
        return [], [self._file_name]
