# Imports

import sys
import datetime
import collections
import json
from pprint import pprint
from typing import OrderedDict
import urllib.request
import urllib.parse

import matplotlib.pyplot as plt

releases_api_url = "https://api.github.com/repos/noah-nuebling/mac-mouse-fix/releases"
history_file_path = 'stats_history.json'

# Main

def main():

    if len(sys.argv) == 1: # Print current downloads
        releases = load_releases()
        releases = sorted_by_release(releases, 'published_at')
        total_downloads = 0
        for r in releases:
            short_version = r['name']
            downloads = r['assets'][0]['download_count']
            total_downloads += downloads
            print(f'{short_version}: {downloads}')
        print(f'\ntotal: {total_downloads}')

    elif len(sys.argv) >= 2:

        command_line_argument = sys.argv[1]

        if command_line_argument == 'record':
            # Load existing log

            history = load_history()
            releases = load_releases()

            current_time = datetime.datetime.utcnow()

            for r in releases:

                # Get short version
                short_version = r['name']

                # Get download count
                downloads = r['assets'][0]['download_count']

                # Append to log
                make_path(history, short_version, str(current_time))['download_count'] = downloads
                # log[short_version][current_time]['download_count'] = downloads

            # Print
            print(f'New datapoints recorded for {current_time}. View them with `./stats print`')

            # Write log to file
            with open(history_file_path, 'w') as outfile:
                outfile.write(json.dumps(history))
        elif command_line_argument == 'print':
            history = load_history()
            print_nested(sorted_by_release(history, 'name'))
        elif command_line_argument == 'plot':
            # Load venv with matplotlib
            
            # plt.plot([1,2,3,4])
            # plt.ylabel('Some nums')
            # plt.show()
            
        else:
            raise Exception('Unknown command line argument.')
    else:
        raise Exception('Too many command line arguments.')

def load_releases():
    request = urllib.request.urlopen(releases_api_url)
    releases = json.load(request)
    return releases

def load_history():
    log = {}
    try:
        with open(history_file_path, 'r') as f:
            log = json.load(f)
    except Exception as e:
        print(f'Exception while opening history file: {e}')
    return log

# Source: https://stackoverflow.com/questions/60808884/python-to-create-dict-keys-path-similarly-to-mkdir-p
def make_path(my_dict: dict, *paths: str) -> dict:
    while paths:
        key, *paths = paths
        my_dict = my_dict.setdefault(key, {})
    return my_dict

def print_nested(val, nesting = -4): 
	if isinstance(val, dict): 
		print('') 
		nesting += 4
		for k in val: 
			print(nesting * ' ', end='') 
			print(k, end=': ') 
			print_nested(val[k],nesting) 
	else: 
		print(val) 

def sorted_by_release(arg, key):
    if isinstance(arg, list):
        return sorted(arg, key = lambda i: i[key])
    elif isinstance(arg, dict):
        return collections.OrderedDict(sorted(arg.items()))
    else:
        raise Exception('Unexpected argument type')

main()
