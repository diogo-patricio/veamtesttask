import sys
import os
from pathlib import Path
import shutil
import filecmp
import logging
import time
import argparse

def main():
    args = parseArguments()

    logging.basicConfig(
        level=logging.INFO,
        format = '%(asctime)s:%(levelname)s:%(message)s',
        handlers=[logging.FileHandler(args.logfile), logging.StreamHandler(sys.stdout)],
    )

    logging.info('Starting process: source "%s", replica "%s", period "%s", logfile "%s"', 
                args.source,
                args.replica,
                args.period,
                args.logfile)
    try:
        while True:
            logging.info("Starting sync")
            dirSync(args.source, args.replica)
            logging.info("Sync ended")
            time.sleep(args.period)
    except KeyboardInterrupt:
        logging.info('Stopping process due to keyboard interrupt')

    #copytree(source, target, dirs_exist_ok=True)

def parseArguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Periodicaly synchronizes folders from a source folder to a replica folder'
    )
    parser.add_argument('source',
                        type=Path,
                        help='the path to the folder to be synchronized'
                        )
    parser.add_argument('replica',
                        type=Path,
                        help='the path where to replicate the source folder'
                        )
    parser.add_argument('period',
                        type=int,
                        help='the synchronization interval'
                        )
    parser.add_argument('logfile',
                        type=Path,
                        help='the path to the logfile (defaults to working directory)',
                        default='.'
                        )
    return parser.parse_args()

def dirSync(source : Path, target : Path) -> None:
    (newFiles, newDirs, updateFiles, updateDirs, removedFiles, removedDir) = dirCmp(source, target)

    for file in newFiles:
        copyFile(source / file, target / file)
    
    for file in removedFiles:
        removeFile(target / file)

    for file in updateFiles: 
        updateFile(source / file, target / file)

    for dir in newDirs:
        createDir(target / dir)
        dirSync(source / dir, target / dir)

    for dir in removedDir:
        removeDir(target / dir)

    for dir in updateDirs:
        dirSync(source / dir, target / dir)

def dirCmp(dir1 : Path, dir2 : Path) -> tuple[set[Path], set[Path], set[Path], set[Path], set[Path], set[Path]]:
    files1 = { file.relative_to(dir1) for file in dir1.iterdir() if file.is_file() }
    files2 = { file.relative_to(dir2) for file in dir2.iterdir() if file.is_file() }
    subdirs1 = { dir.relative_to(dir1) for dir in dir1.iterdir() if dir.is_dir() }
    subdirs2 = { dir.relative_to(dir2) for dir in dir2.iterdir() if dir.is_dir() }

    newFiles = files1.difference(files2)
    removedFiles = files2.difference(files1)
    updateFiles = { file for file in files1
                   if file in files2 and not fileCmp(dir1 / file, dir2 / file) }

    newDirs = subdirs1.difference(subdirs2)
    removedDir = subdirs2.difference(subdirs1)
    updateDirs = subdirs1.intersection(subdirs2)

    return (newFiles, newDirs, updateFiles, updateDirs, removedFiles, removedDir)

def fileCmp(file1 : Path, file2 : Path) -> bool:
    #TODO rewrite
    return filecmp.cmp(file1, file2)
    
def copyFile(source : Path, target : Path) -> None:
    try:
        shutil.copy2(source, target, follow_symlinks = False)
        logging.info('New file created: "%s"', target)
    except:
        e = sys.exc_info()[0]
        logging.error('Error creating file: "%s"', e)

def updateFile(source : Path, target : Path) -> None:
    try:
        os.remove(target)
        shutil.copy2(source, target)
        logging.info('File updated: "%s"', target)
    except:
        e = sys.exc_info()[0]
        logging.error('Error updating file: "%s"', e)


def removeFile(target : Path) -> None:
    try:
        os.remove(target)
        logging.info('File removed: "%s"', target)
    except:
        e = sys.exc_info()[0]
        logging.error('Error removing file: "%s"', e)

def removeDir(dir : Path) -> None:
    try:
        shutil.rmtree(dir)
        logging.info('Directory removed: "%s"', dir)
    except:
        e = sys.exc_info()[0]
        logging.error('Error removing directory: "%s"', e)

def createDir(dir : Path) -> None:
    try:
        os.mkdir(dir)
        logging.info('Directory created: "%s"', dir )
    except:
        e = sys.exc_info()[0]
        logging.error('Error creating directory: "%s"', e)


if __name__ == "__main__":
    main()