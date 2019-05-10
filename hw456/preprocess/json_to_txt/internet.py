# -*- coding: UTF-8 -*-
import csv
import numpy as np
import os

list_swear = []
# list of ZH

list_guilty = []
# [0]: # of guilty
# [1]: # of total cases

list_date = []
# list of dates

list_tf = []
# list of term freq

csv_in = open('dict_raw.csv', newline = '', encoding = 'utf-8')
rows = csv.reader(csv_in)

csv_ZH = open('dict_internet.csv', 'w', newline = '', encoding = 'utf-8')
writerZH = csv.writer(csv_ZH)

for row in rows:
	"""
	row[0]: date
	row[1]: guilty or not
	row[2~]: ZH
	"""
	for i in range(3, len(row)):
		if int(row[2]) == 0:
			continue
		if row[i] in list_swear:
			index = list_swear.index(row[i])
			list_date[index].append(row[0])
			list_guilty[index][0] += int(row[1])
			list_guilty[index][1] += 1
		else:
			list_swear.append(row[i])
			list_date.append([row[0]])
			list_guilty.append([int(row[1]), 1])
		
for i in range(len(list_swear)):
	writerZH.writerow([list_swear[i]] + list_guilty[i] + list_date[i])

		