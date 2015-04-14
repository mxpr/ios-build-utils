
import shutil
import tempfile

class TempDirectory:
    """
    Temporary directory helper which can be used within the With Context Manager.

    When used with a `with` statement, cleanup of the directory is done automatically.

    Example:

        file1 = "/path/to/file1"
        file2 = "/path/to/file2"
        with TempDirectory() as tempdir:
            temp_file = os.path.join(tempdir, "_file1")
            shutil.move(file1, temp_file)
            shutil.move(file2, file1)
            shutil.move(file1, temp_file)
    """
    def __init__(self):
        self.path = tempfile.mkdtemp()

    def __cleanup(self):
        shutil.rmtree(self.path, ignore_errors=True)

    def __enter__(self):
        return self.path

    def __exit__(self, exc, value, tb):
        self.__cleanup()
