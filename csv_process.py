import csv

fh = open('hashtags_match.txt', 'w+')
with open('../stream_result_match.csv', mode='r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        fh.write("#"+row[0]+'\n')

csvFile.close()
fh.close()