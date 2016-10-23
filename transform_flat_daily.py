import csv
import json
import re
from datetime import date
from datetime import datetime

def transform(file, date, output_file_path, write_header=False):
    with open(file) as data_file:
        data = []
        for data_line in data_file:
            line_data = json.loads(data_line)
            data.extend(line_data)
        # data = json.load(data_file)
        del data[0]['Coordinate']
        headers = data[0].keys()
        headers.append('UpdatedISO')
        f = csv.DictWriter(open(output_file_path, "a"), headers)
        if write_header:
            f.writeheader()
        for d in data:
            updated_time_str = d['Updated']
            updated_time = datetime.strptime(updated_time_str + "M", "%I:%M:%S%p")
            last_updated = datetime.combine(
                date, #datetime.now(),
                updated_time.timetz(),
            )
            last_updated_string = last_updated.strftime('%s')
            last_updated_iso_sting = last_updated.isoformat()
            time_diff = d['UpdatedAgo']
            match_time_diff = re.search("(\d*)m?(\d*)s? ago",time_diff)
            num_time_diff = -1
            if match_time_diff:
                num_time_diff = 0
                if 'm' in time_diff:
                    num_time_diff += int(match_time_diff.group(1))*60
                    if 's' in time_diff:
                        num_time_diff += int(match_time_diff.group(2))
                if 's' in time_diff:
                    num_time_diff += int(match_time_diff.group(1))
            d['UpdatedAgo'] = num_time_diff
            if 'Coordinate' in d:
                del d["Coordinate"]
            d["Updated"] = last_updated_string
            d["UpdatedISO"] = last_updated_iso_sting
            f.writerow(d)

output_path = '~/busdata/1010-1014_out.csv'
file_path = '~/busdata/Fri1014/'
transform(file_path + 'boop_1.txt', date(2016,10,10), output_path, write_header=True)
transform(file_path + 'boop_2.txt', date(2016,10,11), output_path)
transform(file_path + 'boop_3.txt', date(2016,10,12), output_path)
transform(file_path + 'boop_4.txt', date(2016,10,13), output_path)
transform(file_path + 'boop_5.txt', date(2016,10,14), output_path)
