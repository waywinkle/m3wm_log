from os import listdir, remove
from os.path import isfile, join
from process_log import process_file
import json
from datetime import datetime
import logging
from properties import get_property


LOGGER = logging.getLogger(__name__)
TEST_DIRECTORY = 'H:\M3WMServerLog'


def process_dir(directory):
    json_files = [f[0:-5] for f in listdir(join(directory, 'json'))]

    for f in listdir(directory):
        full_file = join(directory, f)
        if isfile(full_file) and f[0:4] == 'M3WM':
            name = f[0:-4]
            date_string = name[-8:]
            file_date = datetime.strptime(date_string, '%Y%m%d')
            if file_date.date() != datetime.now().date() and name not in json_files:
                LOGGER.info('processing file : {file}'.format(file=name))
                processed = json.dumps(process_file(full_file, date_string))
                with open(join(join(directory, 'json'), name + '.json'), 'w') as outfile:
                    json.dump(processed, outfile)
            else:
                LOGGER.info('skipping file : {file}'.format(file=name))


def clean_dir(directory):
    json_dir = join(directory, 'json')
    keep_days = get_property('keep_log_days')
    for f in listdir(json_dir):
        full_file = join(json_dir, f)
        name = f[0:-5]
        file_date = datetime.strptime(name[-8:], '%Y%m%d')
        delta = abs((datetime.now() - file_date).days)

        if delta > keep_days:
            LOGGER.info('removing file as over {days} old : {file}'.format(days=delta, file=name))
            remove(full_file)


if __name__ == "__main__":
    process_dir(TEST_DIRECTORY)
