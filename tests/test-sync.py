from pathlib import Path
import unittest
from sync.sync import *

class TestSync(unittest.TestCase):

    def setUp(self) -> None:
        self.sourcePath = Path('tests/test_files/source')
        self.targetPath = Path('tests/test_files/replica')
        self.restorePath = Path('tests/test_files/restore')
    
    def tearDown(self) -> None:
        dirSync(self.restorePath, self.targetPath)

    def test_copy_file (self):
        file = Path('new_file')
        sourceFile = self.sourcePath / file
        targetFile = self.targetPath / file
        copyFile(sourceFile, targetFile)
        self.assertTrue(targetFile.is_file())
        self.assertTrue(fileCmp(sourceFile, targetFile))

    def test_remove_file(self):
        file = Path('removed_file')
        targetFile = self.targetPath / file
        removeFile(targetFile)
        self.assertFalse(targetFile.is_file())

    def test_update_file(self):
        file = Path('altered_file')
        sourceFile = self.sourcePath / file
        targetFile = self.targetPath / file
        updateFile(sourceFile, targetFile)
        self.assertTrue(targetFile.is_file())
        self.assertTrue(fileCmp(sourceFile, targetFile))

    def test_create_dir(self):
        dir = Path('new_test_dir')
        targetDir = self.targetPath / dir
        createDir(targetDir)
        self.assertTrue(targetDir.is_dir())
    
    def test_remove_dir(self):
        dir = Path('removed_dir')
        targetDir = self.targetPath / dir
        removeDir(targetDir)
        self.assertFalse(targetDir.is_dir())
    
if __name__ == '__main__':
    unittest.main()