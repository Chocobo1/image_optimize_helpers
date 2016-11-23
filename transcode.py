#!/bin/python2

def processFile(file, newExt, cmdLine, quiet = False):
    """
    file: Input, the file to be processed
    newExt: Input, the file extension after processing. If `None`, then it will be the same as file
    cmdLine: Input, the command line to be invoked, will replace "%input%" & "%ouput%" fields
    """

    # start
    import os
    import shutil
    import subprocess
    import sys
    import tempfile

    if sys.platform == "win32":
        file = file.encode('utf-8')
    print "\n processing: %s \n" % file

    fsplit = file.rsplit(".", 1)
    origFileName = fsplit[0]
    origFileExt = fsplit[1]
    if not newExt:
        newExt = origFileExt

    # copy file to a temp file, workaround unicode file name issues
    tmpDir = os.getcwd()
    subDir = origFileName.rsplit(os.sep, 1)
    if len(subDir) > 1:  # have subdirectories
        tmpDir += os.sep + subDir[0]

    tmpFile = tempfile.NamedTemporaryFile(dir = tmpDir, suffix = "." + origFileExt, delete = False)
    tmpFile.close()
    shutil.copyfile(file.decode('utf-8'), tmpFile.name)

    # process command
    tmpInputName = tmpFile.name
    tmpOutputName = tmpFile.name.rsplit(".", 1)[0] + "." + newExt
    cmdLine2 = cmdLine.replace("%input%", '"' + tmpInputName + '"').replace("%output%", '"' + tmpOutputName + '"')

    # without shell, linux cannot find bin in $PATH
    shellArg = True
    if sys.platform == "win32":
        shellArg = False

    # redirect stdout & stderr to /dev/null
    quietArg = None
    if quiet:
        quietArg = open(os.devnull, 'w')

    runProg = subprocess.Popen(cmdLine2, shell = shellArg, stdout = quietArg, stderr = subprocess.STDOUT)
    runProg.wait()

    if quiet:
        quietArg.close()

    # cleanup
    shutil.move(tmpOutputName, origFileName.decode('utf-8') + "." + newExt)
    try:
        os.remove(tmpInputName)
    except OSError:
        pass


def runDeflopt(file):
    processFile(file, newExt = None, cmdLine = "deflopt %input%", quiet = True)


def runOptipng(file):
    processFile(file, newExt = "png", cmdLine = "optipng -o7 %input%", quiet = True)


def runPngout(file):
    processFile(file, newExt = "png", cmdLine = "pngout %input%", quiet = True)


def runZopflipng(file):
    processFile(file, newExt = "png", cmdLine = "zopflipng -m -y %input% %output%", quiet = True)


def optimizePNG(file):
    import os

    newSize = os.stat(file).st_size
    fileSize = newSize + 1
    while newSize < fileSize:
        fileSize = newSize
        runPngout(file)
        runOptipng(file)
        newSize = os.stat(file).st_size

    runDeflopt(file)


def runJpegoptim(file):
    processFile(file, newExt = None, cmdLine = "jpegoptim -s %input%", quiet = True)


def runCwebp(file):
    processFile(file, newExt = "webp", cmdLine = "cwebp -v -lossless -q 100 -m 6 %input% -o %output%", quiet = True)


if __name__ == "__main__":
    import sys
    import win32_unicode_argv

    arg1 = sys.argv[1]
    runCwebp(arg1)
