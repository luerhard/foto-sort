# foto-sort
Sort fotos by date and location of file metadata

# Installation
## Requirements
This package requires ExifTool to be install beforehand.
It is avalailabe for Windows, MacOS and Unix Platforms.

Installation instructions can be found [here](https://exiftool.org/install.html).

## Ubuntu
`sudo apt install exiftool`

## Arch
`sudo pacman -S perl-image-exiftool`


# Usage
Install fotosort will make the command `fotoingest` available on the commandline.

```
Usage: fotoingest [OPTIONS]

  Sort fotos by date and location of file metadata

Options:
  -i, --input TEXT  Input folder. Multiple parameters are allowed.
  -o, --to TEXT     Location of output folder.  [required]
  --help            Show this message and exit.
```
