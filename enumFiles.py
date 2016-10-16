#!/bin/python2

def enumFilesFilter(dir, ext = None, recurisve = False):
    """
    dir: Input, the target directory
    ext: Input, only files ends with this field will be listed. If `None`, then no filtering will be done
    recursive: Input, whether go into subdirectories
    return a list of names of files (could contain relative path)
    """

    import os

    ret = []
    walker = os.walk(unicode(dir))
    for path, _, filenames in walker:
        relPath = path[(len(dir) + 1):]
        if relPath:
            fileFullPaths = map(lambda x: relPath + os.sep + x, filenames)
        else:
            fileFullPaths = filenames

        ret += fileFullPaths

        if not recurisve:
            break

    if ext:
        ret = filter(lambda f: f.endswith(ext), ret)
    return ret


def generateCmds(fileList, cmdLine):
    """
    fileList, Input list, the list of files to be processed
    cmdLine, Input, the command line string, the string "%listEntry%" will be replaced by entries in `fileList`
    """

    ret = map(lambda f: cmdLine.replace("%listEntry%", f), fileList)
    return ret


def printList(cmdList):
    for c in cmdList:
        print c.encode('utf-8')  # comment when printing to windows console


if __name__ == "__main__":
    import os

    currentDir = os.getcwd()
    filesList = enumFilesFilter(currentDir, ext = "png", recurisve = False)
    if filesList:
        cmdsList = ["### Threads: 3 ###"]
        cmdsList += generateCmds(filesList, cmdLine = "python2 transcode.py \"%listEntry%\"")
        printList(cmdsList)
