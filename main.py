import logging
from log_setup import setup_logging
from process_files import process_dir, clean_dir
from properties import get_property


PROP = 'properties'


def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    log_to_process = get_property('log_location')

    logger.info('processing directory : {dir}'.format(dir=log_to_process))
    process_dir(log_to_process)
    clean_dir(log_to_process)


if __name__ == '__main__':
    main()
