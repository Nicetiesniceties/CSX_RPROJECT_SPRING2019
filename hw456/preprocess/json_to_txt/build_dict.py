# -*- coding: UTF-8 -*-
import json
import sys
import os
import csv

path = '/4TB/schen/insult_data/'
csvfile = open('dict_raw.csv', 'w', newline = '', encoding = 'utf-8')
writer = csv.writer(csvfile)

for filename in os.listdir(path):
	period = filename.rfind(',')
	if period + 9 == filename.rfind('.'):
		date = int(filename[period + 1: period + 9])
	else:
		date = int(filename[period - 8 : period])

	file_path = path + filename
	with open(file_path, 'r', encoding = 'utf-8') as fi:
		data = fi.read()
		if (data.find('『') == -1 and data.find('』') == -1):
			continue
		swear = data[data.find('『') + 1 : data.find('』')]
		swear_list = swear.split('、')
		if data.find('以「') != -1:
			start = data.find('以「') + 2
			while True:
				end = data.find('」', start)
				swear_list.extend(data[start : end].split('、'))
				if data[end + 1] == '、':
					start = end + 3
				else:
					break
		if swear_list == []:
			continue
		swear_list = list(set(swear_list))
		swear_list.insert(0, date)
		if data.find('無罪') == -1:
			guilty = 0
		else:
			guilty = 1
		swear_list.insert(1, guilty)
		if data.find('網路') != -1 or data.find('網絡') != -1:
			internet = 1
		else:
			internet = 0
		swear_list.insert(2, internet)
		if swear_list != []:
			print(swear_list)
			writer.writerow(swear_list)