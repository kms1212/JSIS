from fileapi.models import File
from django.core.files.storage import default_storage
import uuid
import magic

def get_data_from_file(file):
    """
    Get the binary data from a file.

    Parameters / Return Values
    --------------------------

    :param file: File object to get the data from.
    :returns: Binary data from the file.

    Description
    -----------

    This function gets filename from the file object and opens it with the default storage.
    Then, it reads the file and returns the data.
    
    Revision History
    ----------------
    * 2023-02-??: Created by @kms1212.
    * 2023-02-09: Documented by @kms1212.
    """
    with default_storage.open(file.data.name, 'rb') as file:
        return file.read()

def get_size_from_file(file):
    """
    Get the file size from a file.

    Parameters / Return Values
    --------------------------

    :param file: File object to get the size from.
    :returns: File size.

    Description
    -----------

    This function gets filename from the file object and opens it with the default storage.
    Then, it reads the file and returns the file size.
    
    Revision History
    ----------------
    * 2023-02-??: Created by @kms1212.
    * 2023-02-09: Documented by @kms1212.
    """
    with default_storage.open(file.data.name, 'rb') as file:
        return file.size

def register_file(filename, file, uploader):
    """
    Register a file.

    Parameters / Return Values
    --------------------------

    :param filename: File name
    :param file: File data
    :param uploader: Uploader
    :returns: File object.

    Description
    -----------

    This function saves the file with the default storage and creates a File object.
    
    Revision History
    ----------------
    * 2023-02-??: Created by @kms1212.
    * 2023-02-09: Documented by @kms1212.
    """
    filename_saved = default_storage.save(uuid.uuid4(), file)
    file_saved = default_storage.open(filename_saved, 'r')
    file = File.objects.create(filename=filename, data=filename_saved, uploader=uploader, mimetype=magic.from_buffer(file_saved.read(2048), mime=True))
    file_saved.close()
    file.save()

    return file


