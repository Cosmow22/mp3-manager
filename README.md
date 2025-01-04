# mp3-manager

A simple cli to manage mp3 songs.

```Powershell
pip install mp3-manager
```

```Powershell
mp3 -h

usage: mp3 [-h] [-p PATH] {scan,edit,equalize} ...

A CLI to manage mp3.

positional arguments:
  {scan,edit,equalize}
    scan                Scan the folder and create a csv file.
    edit                Parse csv file and edit musics metadata.
    equalize            Equalize the volume of all musics.

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  The path to mp3
```

The csv file contains songs metadatas. Change them easily in your spreadsheet software.
