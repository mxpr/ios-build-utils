

import os
import unittest
import zipfile

# Allow running tests in sublime using `cmd+b`
# otherwise command line `python -m test.test__packager`

if __package__ is None:
    import sys
    sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )

from utils.packager import Packager
from utils.tempdirectory import TempDirectory


class PackagerTest(unittest.TestCase):

    def __makeFile(self, directory, name, content = ""):

        path = os.path.join(directory, name)

        with open(path,'w') as temp_file:
            temp_file.write(content)

        return path

    def __makeDirectory(self, directory, name):

        path = os.path.join(directory, name)

        os.makedirs(path)

        return path

    def __packageContents(self, path_to_package):

        z = zipfile.ZipFile(path_to_package)
        return z.namelist()


    def test_adding_single_file(self):

        with TempDirectory() as tempdir:
            package_file = os.path.join(tempdir, "package.zip")

            p = Packager(package_file)

            self.assertFalse(os.path.exists(package_file))

            p.add(self.__makeFile(tempdir,"file1"))
            p.package()  

            self.assertTrue(os.path.exists(package_file))
            self.assertIn("file1", self.__packageContents(package_file))


    def test_adding_multiple_file(self):

        with TempDirectory() as tempdir:
            package_file = os.path.join(tempdir, "package.zip")

            p = Packager(package_file)

            self.assertFalse(os.path.exists(package_file))

            p.add(self.__makeFile(tempdir,"file1"))
            p.add(self.__makeFile(tempdir,"file2"))
            p.add(self.__makeFile(tempdir,"file3"))
            p.package()  

            self.assertTrue(os.path.exists(package_file))
            
            package_contents = self.__packageContents(package_file)

            self.assertEqual(3, len(package_contents))
            self.assertIn("file1", package_contents)
            self.assertIn("file2", package_contents)
            self.assertIn("file3", package_contents)


    def test_defining_custom_structure(self):

        with TempDirectory() as tempdir:
            package_file = os.path.join(tempdir, "package.zip")

            p = Packager(package_file)

            self.assertFalse(os.path.exists(package_file))

            item = self.__makeFile(tempdir,"file1")
            p.add(item)
            p.add(item, "directory1/file1")
            p.add(item, "directory2/file1")
            p.add(item, "directory2/subdir1/file1")
            p.package()

            self.assertTrue(os.path.exists(package_file))
            
            package_contents = self.__packageContents(package_file)

            self.assertEqual(4, len(package_contents))
            self.assertIn("directory1/file1", package_contents)
            self.assertIn("directory2/file1", package_contents)
            self.assertIn("directory2/subdir1/file1", package_contents)

    def test_adding_directories(self):

        with TempDirectory() as tempdir:
            package_file = os.path.join(tempdir, "package.zip")

            p = Packager(package_file)

            self.assertFalse(os.path.exists(package_file))

            directory = self.__makeDirectory(tempdir,"dir1")
            self.__makeFile(directory,"file1")
            p.add(directory)
            p.package()
            
            self.assertTrue(os.path.exists(package_file))
            
            package_contents = self.__packageContents(package_file)
            
            self.assertEqual(1, len(package_contents))
            self.assertIn("dir1/file1", package_contents)



if __name__ == '__main__':
    print __file__
    unittest.main()

