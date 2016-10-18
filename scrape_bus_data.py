import argparse
import csv
import time

import get_bus

parser = argparse.ArgumentParser()
parser.add_argument('-w', '--write-header', help='write header to csv',
                    action='store_true')
parser.add_argument('-o', '--output-file', 
    help='csv to output to (default: out_scrape_bus_data.csv)',
    default='out_scrape_bus_data.csv')
parser.add_argument("-v", "--verbosity", action="count", default=0,
                help="increase output verbosity")
args = parser.parse_args()

routes_to_scrape = [
    '2092',
    '312',
    '314',
    '1263',
    '1264',
    '1114',
    '1113',
    '3442',
    '3440',
    '3159',
    '1098',
    '2399',
    '1434',
    '313',
    '3849',
]

if args.verbosity > 0:
    print 'Scraping: ', routes_to_scrape
    print "Output To: ", args.output_file
    

with open(args.output_file ,'a') as out_file:
    dict_writer = get_bus.get_dict_writer(out_file)
    
    if args.write_header:
        dict_writer.writeheader()
        if args.verbosity > 0:
            print "Writing Header: ", get_bus.BusPoint._fields
        
while(True):
    with open(args.output_file ,'a') as out_file:
        dict_writer = get_bus.get_dict_writer(out_file)
        for route_id in routes_to_scrape:
            bus_points = get_bus.get_live_bus_info(route_id)
            for bus_point in bus_points:
                if args.verbosity > 0:
                    print "Writing: ", bus_point
                get_bus.append_bus_point_to_csv(bus_point, dict_writer)
    time.sleep(5)
