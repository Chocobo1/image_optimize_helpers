#!/bin/python3

def enumFilesFilter(dir, ext = None, recurisve = False):
    """
    dir: Input, the target directory
    ext: Input, only files ends with this field will be listed. If `None`, then no filtering will be done
    recursive: Input, whether go into subdirectories
    return a list of names of files (could contain relative path)
    """

    import os

    ret = []
    walker = os.walk(str(dir))
    for path, _, filenames in walker:
        relPath = path[(len(dir) + 1):]
        if relPath:
            fileFullPaths = [relPath + os.sep + x for x in filenames]
        else:
            fileFullPaths = filenames

        ret += fileFullPaths

        if not recurisve:
            break

    if ext:
        ret = [f for f in ret if f.endswith(ext)]
    return ret


def generateCmds(fileList, cmdLine):
    """
    fileList, Input list, the list of files to be processed
    cmdLine, Input, the command line string, the string "%listEntry%" will be replaced by entries in `fileList`
    """

    ret = [cmdLine.replace("%listEntry%", f) for f in fileList]
    return ret


def printList(cmdList):
    for c in cmdList:
        print(c)


if __name__ == "__main__":
    import os

    currentDir = os.getcwd()
    filesList = enumFilesFilter(currentDir, ext = "png", recurisve = False)
    if filesList:
        cmdsList = ["### Threads: 3 ###"]
        cmdsList += generateCmds(filesList, cmdLine = "python transcode.py \"%listEntry%\"")
        printList(cmdsList)
