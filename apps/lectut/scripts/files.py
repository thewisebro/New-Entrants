import csv
with open('tutorials.csv', 'rb') as csvfile:
  spamreader = csv.reader(csvfile)
  for row in spamreader:
    print row
    print '00000'
