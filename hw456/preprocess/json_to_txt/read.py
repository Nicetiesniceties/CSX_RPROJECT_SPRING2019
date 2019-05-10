# -*- coding: UTF-8 -*-
import json
import sys
import os

path = '/4TB/schen/susan_dataset/'
count = 0
no = 0
for date_dir in os.listdir(path):
	date_path = path + date_dir + '/'
	
	for court_dir in os.listdir(date_path):
		if court_dir.find('地方法院') == -1 and court_dir.find('高等法院') == -1:
			continue
		if court_dir.find('刑事') == -1:
			continue

		court_path = date_path + court_dir + '/'

		for filename in os.listdir(court_path):
			file_path = court_path + filename
			
			with open(file_path, 'r', encoding = 'utf-8') as fi:
				data = fi.read()

				JID = data[data.find("JID") + 6 : data.find("JYEAR") - 3]
				JYEAR = data[data.find("JYEAR") + 8 : data.find("JCASE") - 3]
				JCASE = data[data.find("JCASE") + 8 : data.find("JNO") - 3]
				JNO = data[data.find("JNO") + 6 : data.find("JDATE") - 3]
				JDATE = data[data.find("JDATE") + 8 : data.find("JTITLE") - 3]
				JTITLE = data[data.find("JTITLE") + 9 : data.find("JFULL") - 3]
				JFULL = data[data.find("JFULL") + 6 : ]
				#print(JTITLE)
			if JFULL.find('公然侮辱') != -1:
				count += 1
				if JFULL.find('無罪') != -1:
					no += 1
				print(count, no)
				print(filename)
				with open('/4TB/schen/insult_data/' + filename[: filename.find(".")] + '.txt', 'w', encoding = 'utf-8') as fo:
					fo.write(JID + '\r\n')
					fo.write(JYEAR + '\r\n')
					fo.write(JCASE + '\r\n')
					fo.write(JNO + '\r\n')
					fo.write(JDATE + '\r\n')
					fo.write(JTITLE + '\r\n')
					fo.write(JFULL + '\r\n')



