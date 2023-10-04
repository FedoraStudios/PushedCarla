import json
import csv

data_from_csv = []

with open('data_set.txt', 'r') as f:
	data_from_txt = json.loads(f.read())
    
    field_names = ['brake', 'hand_brake', 'throttle', 'steer']
    csvfilestore = open('C277project.csv', 'w', newline = '')
    writer = csv.DictWriter(csvfilestore, field_names = field_names)
    writer.write header()
    writer.write rows(data_from_txt)

with open('C277project.csv', 'r') as f:
	reader = csv.reader(f)
	for row in reader:
		data_from_csv.append(row)

print(data_from_csv)