import os
import re
import time
import pprint
import logging

LOGGER = logging.getLogger(__name__)

TEST_FILE = 'test_data/M3WMServerLog20170406.txt'


def process_file(file, date_string):
    file_dict = dict()
    records = list()
    for line in open(get_file_location(file)):
        split_line = line.split(' ', 3)
        if line != '\n' and split_line[1] not in ['Server', 'Server->']:
            line_dict = clean_line(split_line)
            line_dict['data']['time'] = get_time(date_string, line_dict['data']['time'])
            if line_dict['source'] == 'Client':
                record = dict(client=line_dict['data']['fields'])
                record['ip'] = line_dict['data']['ip']
                record['time'] = line_dict['data']['time']
                record['username'] = line_dict['data']['fields'][0][0:-17]
            else:
                record['server'] = line_dict['data']['fields']
                records.append(record)

    file_dict['records'] = records
    return file_dict


def get_file_location(file_name):
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    return os.path.join(__location__, file_name)


def clean_line(line):
    line_dict = {'data': dict()}
    for i, value in enumerate(line):
        if i == 0:
            line_dict['data']['ip'] = value
        elif i == 1:
            line_dict['data']['time'] = value[1:-2]
        elif i == 2:
            line_dict['source'] = value[0:-2]
        elif i == 3:
            cleaned_data = clean_api_call(value)
            line_dict['data']['fields'] = cleaned_data

    return line_dict


def clean_api_call(call):
    pattern = r'"([A-Za-z0-9_\./\\-]*)"'
    split_values = call.split(',')
    return [g.group()[1:-1] for g in [re.search(pattern, f) for f in split_values] if g is not None]


def get_time(date_string, time_string):
    return time.mktime(time.strptime(date_string + time_string[0:8], '%Y%m%d%H:%M:%S'))


if __name__ == "__main__":
    result = process_file(TEST_FILE, '20170406')
    pp = pprint.PrettyPrinter(indent=1)
    pp.pprint(result)
