
import os
import shutil
import subprocess

from tempdirectory import TempDirectory


class Packager:
    """
    Packager utility

        output: the path to create the final package in

    Usage:

        Define the package structure by adding files or directories
        using `add(path)` and then create the package using `package()`

    Example:

        p = Packager("package.zip")
        p.add("/path/to/file")
        p.add("/path/to/another/file","another/file")
        p.package()

        # Produces a zip file with
        #   package.zip
        #       - file
        #       - another/file

    """
    def __init__(self, output): 
        self.output = output
        self.items  = []

    def add(self, path, path_in_package = None):
        """
        Add files or directories definition to the package.

            path:               path of item to include in package

            path_in_package:    the path the item will end up having in the package
                                will default to the directory or file name of the item
                                if not specified

        """
        self.items.append((path, path_in_package))

    def package(self):
        """
        Create the package in the `output` path specified during initialization.
        """
        # Make a temp directory
        with TempDirectory() as tempdir:

            # Copy all Items
            for item in self.items:

                (path, path_in_package) = item
                if not path_in_package:
                    path_in_package = os.path.basename(path)

                destination = os.path.join(tempdir, path_in_package)
                self.__copy(path, destination)

            # Zip temp directory
            self.__zipdir(tempdir, self.output)


    def __copy(self, src, dest):

        if os.path.isdir(src):

            shutil.copytree(src, dest)

        elif os.path.isfile(src):

            dest_dir = os.path.dirname(dest)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            shutil.copy(src,dest)

        elif os.path.islink(src):

            path = os.readlink(src)
            self.__copy(path, dest)


    def __zipdir(self, path, zip_path):
        command = ["zip","-qr", zip_path, "."]
        subprocess.check_call(command, cwd=path)

