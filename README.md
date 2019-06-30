# image_optimize_helpers


## Notes for myself

Most of the time, I'll want:
```shell
python enumFiles.py | concurrent -
```

* `enumFiles.py`:

  Enumerate files in a directory (and subdirectories).

  * `recurisve = True`: list files in subdirectories.

  * `ext = None`: list all files.

    `ext = "png"`: list only PNG files.

* `transcode.py`

  All the hard work of manipulating files safely & handling unicode filenames are done here.

  * Choose 1 helper function from the below list:

    | Helper | Notes |
    | ------ | ----- |
    | `runDeflopt()` | Optimize PNG files via [Deflopt](https://web.archive.org/web/20140209022101/http://www.walbeehm.com/download/) |
    | `runOptipng()` | Optimize PNG files via [OptiPNG](http://optipng.sourceforge.net/). |
    | `runPngout()` | Optimize PNG files via [PNGOUT](http://advsys.net/ken/utils.htm). |
    | `optimizePNG()` | A sequence of actions (that I often use) to compress PNG files. |
    | `runJpegoptim()` | Optimize JPG files via [jpegoptim](https://github.com/tjko/jpegoptim). |
    | `runCwebp()` | Run [WebP](https://developers.google.com/speed/webp/). |

* [`concurrent`](https://github.com/Chocobo1/concurrent)

  A tool to utilize multicore CPU.
