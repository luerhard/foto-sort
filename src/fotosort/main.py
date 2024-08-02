#!python3
import logging
from pathlib import Path

import click

from .fotosort import FotoSort

@click.command()
@click.option(
    "-i",
    "--input",
    multiple=True,
    help="Input folder. Multiple parameters are allowed.",
)
@click.option("-o", "--to", required=True, help="Location of output folder.")
def main(input, to):
    """Sort fotos by date and location of file metadata."""
    logger = logging.getLogger(__name__)

    for i in input:
        logger.info("Importing folder: %s", i)
        fotosort = FotoSort(Path(i), Path(to))
        fotosort.run()


if __name__ == "__main__":
    main()
