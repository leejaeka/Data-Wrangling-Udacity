# -*- coding: utf-8 -*-
'''
Find the time and value of max load for each of the regions
COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
and write the result out in a csv file, using pipe character | as the delimiter.

An example output can be seen in the "example.csv" file.
'''

import xlrd
import os
import csv
#from zipfile import ZipFile

datafile = "2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"


#def open_zip(datafile):
#    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
 #       myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    sheet_data = [[sheet.cell_value(r, col) for col in range(sheet.ncols)] for r in range(sheet.nrows)]
    data = {}
    # YOUR CODE HERE
    # Remember that you can use xlrd.xldate_as_tuple(sometime, 0) to convert
    # Excel date to Python tuple of (year, month, day, hour, minute, second)
    #Find the time and value of max load for each of the regions
    #COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
    #and write the result out in a csv file, using pipe character | as the delimiter.
    for i in range(1,9):
        area = sheet.col_values(i, start_rowx=1, end_rowx=None)
        
        temp = {'Year': 0,
                'Month': 0,
                'Day': 0,
                'Hour': 0,
                'Max Load':0}
        temp['Max Load'] = max(area)
        temp_idx = area.index(temp['Max Load'])+1 
        temp_date = xlrd.xldate_as_tuple(sheet.cell_value(temp_idx,0),0)
        temp['Year'] = temp_date[0]
        temp['Month'] = temp_date[1]
        temp['Day'] = temp_date[2]
        temp['Hour'] = temp_date[3]
        data[sheet_data[0][i]] = temp
    
    return data

def save_file(data, filename):
    # YOUR CODE HERE
    with open(filename, "w") as f:
        w = csv.writer(f, delimiter='|')
        w.writerow(["Station", "Year", "Month", "Day", "Hour", "Max Load"])
        print(data)
        for key, value in data.items():
            w.writerow([key, value['Year'], value['Month'], value['Day'], value['Hour'], value['Max Load']])
    
def test():
    #open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)
    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            print(line)
            station = line['Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        assert max_answer == max_line

                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        print(number_of_rows)
        assert number_of_rows == 8

        # Check Station Names
        assert set(stations) == set(correct_stations)

        
if __name__ == "__main__":
    test()
