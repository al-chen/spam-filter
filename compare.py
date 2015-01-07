import csv
file1 = "valLabels.csv"
for j in [1,2,5,10,25]:
	file2 = "emailOutput" + str(j) + ".csv"
	with open(file1, 'rb') as csv1:
		with open(file2, 'rb') as csv2:
			valLabels = csv.reader(csv1, delimiter=',')
			outputLabels = csv.reader(csv2, delimiter=',')
			count = 0
			for i in range(500):
				if valLabels.next() != outputLabels.next():
					count += 1
			print "k=" + str(j) + ": " + str(count)