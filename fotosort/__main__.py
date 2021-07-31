#!python3

from pathlib import Path
import logging
import click

from .fotosort import FotoSort


@click.command()
@click.option("-i", "--input", multiple=True)
@click.option("-o", "--to", required=True)
def main(input, to):

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger(__name__)

    for i in input:
        logger.info("Importing folder: %s", i)
        fotosort = FotoSort(Path(i), Path(to))
        fotosort.run()


if __name__ == "__main__":
    main()
