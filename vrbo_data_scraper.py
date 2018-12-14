# vrbo data scraper

import re
import os

###########
# Targets #
###########
# Location
# Distance (hours)
# $$$
# Bed Spots
# Bathrooms
# Size (sq ft)
# Secluded?

directory = 'vrbo_texts'
input_dir  = 'inputs'
output_dir = 'outputs'

def dir_setup(path):
    '''Makes a directory at path if it doesn't exist already'''
    if not os.path.exists(path): os.makedirs(path)

def make_log():
    buffer = []
    def log(s):
        nonlocal buffer
        buffer.append(s)
    def flush():
        nonlocal buffer
        rv = '\n'.join(buffer)
        buffer = []
        return rv
    return log, flush

log, flush = make_log()

dir_setup(directory)
dir_setup('{}/{}'.format(directory, input_dir))
dir_setup('{}/{}'.format(directory, output_dir))

os.chdir(directory)

for file_name in os.listdir(input_dir):
    try:
        print('processing {}'.format(file_name))
        file_base_name = re.findall(r'.*(?=\.)', file_name)[0]
        text = open(f'{input_dir}/{file_name}').read()

        # Later check if values were modified
        location = None
        distance = None
        price = None
        bed_spots = None
        bathrooms = None
        sq_ft = None
        secluded = None

        # Location
        location = re.findall(r'(?<=Where\n).*', text)
        # Distance (hours)
        # do by hand
        # $$$
        price = re.findall(r'(?<=Total).+', text)
        # Bed Spots
        bed_spots = re.findall(r'(?<=Sleeps: ).+', text)
        # Bathrooms
        bathrooms = re.findall(r'(?<=Bathrooms: )\d+', text)
        # Size (sq ft)
        sq_ft = re.findall(r'\d+(?= sq\. ft\.)', text)
        # Secluded?
        # look on g-maps

        # print(location)
        # print(price)
        # print(bed_spots)
        # print(bathrooms)
        # print(sq_ft)

        key = ['location'
              ,'price'
              ,'bed_spots'
              ,'bathrooms'
              ,'sq_ft'
              ]
        for i, e in enumerate([location, price, bed_spots, bathrooms, sq_ft]):
            if len(e) == 0:
                log(f'{file_name}: found nothing for {key[i]}')

        location = '/'.join(location) if location else ''
        distance = '/'.join(distance) if distance else ''
        price = '/'.join(price) if price else ''
        bed_spots = '/'.join(bed_spots) if bed_spots else ''
        bathrooms = '/'.join(bathrooms) if bathrooms else ''
        sq_ft = '/'.join(sq_ft) if sq_ft else ''
        secluded = '/'.join(secluded) if secluded else ''

        # fields = [location, distance, price, bed_spots, bathrooms, sq_ft, secluded]

        spreadsheet_template = '{}\t{}\t{}\t{}\t{}\t{}\t{}'
        output_file_name = f'{output_dir}/{file_base_name}_output.txt'
        output = open(output_file_name, 'w')
        output.write(spreadsheet_template.format(location, distance, price, bed_spots, bathrooms, sq_ft, secluded))
    except:
        log(f'failed for {file_name}; i={i}; e={e}')
        print(f'failed for {file_name}')
    log(f'succeeded for {file_name}')

print(flush(), sep = '\n', file=open('error.log', 'w'))
