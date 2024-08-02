#!python3
import logging
from pathlib import Path

import click

from .config_manager import ConfigManager
from .fotosort import FotoSort

@click.command()
@click.option(
    "-i",
    "--input",
    multiple=True,
    help="Input folder. Multiple parameters are allowed.",
)
@click.option("-o", "--to", required=False, help="Location of output folder.")
@click.option(
    "-d",
    "--set_defaults",
    is_flag=True,
    help="""
        Set inputs and output as new defaults.
        On subsequent runs, these will be used of not parameters are set.
    """,
)
@click.option(
    "--remove_defaults",
    is_flag=True,
    help="Remove current defaults. This end the script immediately after removal.",
)
def main(input, to, set_defaults, remove_defaults):
    """Sort fotos by date and location of file metadata."""
    logger = logging.getLogger(__name__)

    config = ConfigManager()

    if remove_defaults:
        logger.info("removing defaults. ignoring all other parameters")
        config.delete()
        return

    if set_defaults:
        logger.info("setting defaults. run again to use them.")
        if to:
            to = Path(to)
            config.set_out_path(to)
        if input:
            input = [Path(inp) for inp in input]
            config.set_in_paths(input)
        return
    
    if not to:
        to = config.get_out_path()
        if not to:
            logger.error("Error: no output path given or set as default.")
            return
    if not input:
        input = config.get_in_paths()
        if not input:
            logger.error("Error: No input path(s) given or set as default.")
        return

    for i in input:
        logger.info("Importing folder: %s", i)
        fotosort = FotoSort(Path(i), Path(to))
        fotosort.run()


if __name__ == "__main__":
    main()
