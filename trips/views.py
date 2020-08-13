from __future__ import print_function
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json
import sys
#import c3pyo as c3

# Create your views here.
def welcome(request):
	return render(request, 'index.html')


def questionnaire(request):
	SCOPE = ["https://spreadsheets.google.com/feeds"]
	SECRETS_FILE = "My Project-1c0a7983e6a1.json"
	SPREADSHEET = "BackHarbor"

	credentials = ServiceAccountCredentials.from_json_keyfile_name(
	            SECRETS_FILE, scopes=SCOPE)
	gc = gspread.authorize(credentials)
	workbook = gc.open(SPREADSHEET)
	# Get the first sheet
	sheet = workbook.sheet1
	data = pd.DataFrame(sheet.get_all_records())

	column_names = {
					'1.您認為前往該景點的交通便捷?': 'traffic',
	                '2.您認為該景點的停車位設置合理?': 'parking_lot_location',
	                '3.您認為該景點收費合理?': 'fee',
	                '4.您認為遊樂項目豐富有趣?': 'rides',
	                '5.您認為該景點環境衛生乾淨?': 'clean',
	                '6.您認為該景點設施安全?': 'rides_safe',
	                '7.您認為該景點趣味性佳?': 'amusement',
	                '8.您認為該景點內步道規劃路線合理?': 'trail_setting',
	                '9.您認為該景點工作人員服務態度佳?': 'staff_service',
	                '10.您認為在該景點的購物選擇多樣?': 'souvenir',
	                '11.您認為景點滿足您的期待?': 'satisfied',
	                '12.您會再次選擇遊玩該景點': 'visit_again',
	                '13.您會向家人或朋友推薦該景點?': 'recommend',
	                '14.您的性別是': 'gender',
	                '15.您的年齡': 'age',
	                '16.此次隨行的同伴是?': 'parter',
	                '17.此次旅遊時間?': 'season',
	                '18.您認為該景點的分類標籤是': 'type',
	                '時間戳記':'time_mark',

	}

	data.rename(columns=column_names, inplace=True)
		 
	def likert(new_data,Q):
		Q_list = []

		sum_men = 0
		sum_women = 0
		for i in range(0, len(data['traffic'])):
		    if data['gender'][1] == "男":
		        sum_men += data['traffic'][i]
		    else:
		        sum_women += data['traffic'][i]

		new_data['man'] = sum_men
		new_data['woman'] = sum_women
			
	likert_questions_list = ['traffic',
							'parking_lot_location',
							'fee',
							'rides',
							'clean',
							'rides_safe',
							'amusement',
							'trail_setting',
							'staff_service',
							'souvenir',
							'satisfied',
							'visit_again',
							'recommend',
							]
		
	likert_data = {}
	nominal_data = {}
	test = []
	for q in likert_questions_list:	
		#likert(likert_data,str(q))
		sum_men = []
		sum_women = []
		value = []
		men = {}
		women = {}
		for i in range(0, len(data[q])):
		    if data['gender'][i] == "男":
		        sum_men.append(data[q][i])
		    else:
		        sum_women.append(data[q][i])
		men = {str(p):sum_men.count(p) for p in sum_men}		
		women = {str(p):sum_women.count(p) for p in sum_women}
		value.append(men)
		value.append(women)
		likert_data[q] = value
		for points in range(1,6):
			for items in range(0,len(likert_data[q])):
				if str(points) not in likert_data[q][items]:
					likert_data[q][items][str(points)] = 0

	for q in likert_questions_list:	
		sum_15 = []
		sum_16 = []
		sum_21 = []
		sum_26 = []
		sum_31 = []
		sum_36 = []
		sum_41 = []
		year_value = []
		final_15 = {}
		final_16 = {}
		final_21 = {}
		final_26 = {}
		final_31 = {}
		final_36 = {}
		final_41 = {}
		for i in range(0, len(data[q])):
			if data['age'][i] == "15歲以下":
				sum_15.append(data[q][i])
			elif data['age'][i] == "16-20歲":
				sum_16.append(data[q][i])
			elif data['age'][i] == "21-25歲":
				sum_21.append(data[q][i])
			elif data['age'][i] == "26-30歲":
				sum_26.append(data[q][i])
			elif data['age'][i] == "31-35歲":
				sum_31.append(data[q][i])
			elif data['age'][i] == "36-40歲":
				sum_36.append(data[q][i])			
			else:
				sum_41.append(data[q][i])
		final_15 = {str(p):sum_15.count(p) for p in sum_15}		
		final_16 = {str(p):sum_16.count(p) for p in sum_16}
		final_21 = {str(p):sum_21.count(p) for p in sum_21}	
		final_26 = {str(p):sum_26.count(p) for p in sum_26}	
		final_31 = {str(p):sum_31.count(p) for p in sum_31}
		final_36 = {str(p):sum_36.count(p) for p in sum_36}
		final_41 = {str(p):sum_41.count(p) for p in sum_41}
		year_value.append(final_15)
		year_value.append(final_16)
		year_value.append(final_21)
		year_value.append(final_26)
		year_value.append(final_31)
		year_value.append(final_36)
		year_value.append(final_41)
		nominal_data[q] = year_value
		for points in range(1,6):
			for items in range(0,len(nominal_data[q])):
				if str(points) not in nominal_data[q][items]:
					nominal_data[q][items][str(points)] = 0
    
	return render(request, 'result.html',{'gender_data':json.dumps(likert_data),'year_data':json.dumps(nominal_data),'test':test})
def questionnaire02(request):
	SCOPE = ["https://spreadsheets.google.com/feeds"]
	SECRETS_FILE = "My Project-1c0a7983e6a1.json"
	SPREADSHEET = "WhiteSeedBeach"

	credentials = ServiceAccountCredentials.from_json_keyfile_name(
	            SECRETS_FILE, scopes=SCOPE)

	gc = gspread.authorize(credentials)

	workbook = gc.open(SPREADSHEET)
	# Get the first sheet
	sheet = workbook.sheet1
	data = pd.DataFrame(sheet.get_all_records())
	print(data)
    
	column_names = {
					'1.您認為前往該景點的交通便捷?': 'traffic',
	                '2.您認為該景點的停車位設置合理?': 'parking_lot_location',
	                '3.您認為該景點收費合理?': 'fee',
	                '4.您認為遊樂項目豐富有趣?': 'rides',
	                '5.您認為該景點環境衛生乾淨?': 'clean',
	                '6.您認為該景點設施安全?': 'rides_safe',
	                '7.您認為該景點趣味性佳?': 'amusement',
	                '8.您認為該景點內步道規劃路線合理?': 'trail_setting',
	                '9.您認為該景點工作人員服務態度佳?': 'staff_service',
	                '10.您認為在該景點的購物選擇多樣?': 'souvenir',
	                '11.您認為景點滿足您的期待?': 'satisfied',
	                '12.您會再次選擇遊玩該景點': 'visit_again',
	                '13.您會向家人或朋友推薦該景點?': 'recommend',
	                '14.您的性別是': 'gender',
	                '15.您的年齡': 'age',
	                '16.此次隨行的同伴是?': 'parter',
	                '17.此次旅遊時間?': 'season',
	                '18.您認為該景點的分類標籤是': 'type',
	                '時間戳記':'time_mark',

	}

	data.rename(columns=column_names, inplace=True)
	
	def likert(new_data,Q):
		Q_list = []
		sum_men = 0
		sum_women = 0
		for i in range(0, len(data['traffic'])):
		    if data['gender'][1] == "男":
		        sum_men += data['traffic'][i]
		    else:
		        sum_women += data['traffic'][i]

		new_data['man'] = sum_men
		new_data['woman'] = sum_women
	likert_questions_list = ['traffic',
							'parking_lot_location',
							'fee',
							'rides',
							'clean',
							'rides_safe',
							'amusement',
							'trail_setting',
							'staff_service',
							'souvenir',
							'satisfied',
							'visit_again',
							'recommend',
							]
		
	likert_data = {}
	nominal_data = {}
	test = []
	for q in likert_questions_list:	
		#likert(likert_data,str(q))
		sum_men = []
		sum_women = []
		value = []
		men = {}
		women = {}
		for i in range(0, len(data[q])):
		    if data['gender'][i] == "男":
		        sum_men.append(data[q][i])
		    else:
		        sum_women.append(data[q][i])
		men = {str(p):sum_men.count(p) for p in sum_men}		
		women = {str(p):sum_women.count(p) for p in sum_women}
		value.append(men)
		value.append(women)
		likert_data[q] = value
		for points in range(1,6):
			for items in range(0,len(likert_data[q])):
				if str(points) not in likert_data[q][items]:
					likert_data[q][items][str(points)] = 0

	for q in likert_questions_list:	
		sum_15 = []
		sum_16 = []
		sum_21 = []
		sum_26 = []
		sum_31 = []
		sum_36 = []
		sum_41 = []
		year_value = []
		final_15 = {}
		final_16 = {}
		final_21 = {}
		final_26 = {}
		final_31 = {}
		final_36 = {}
		final_41 = {}
		for i in range(0, len(data[q])):
			if data['age'][i] == "15歲以下":
				sum_15.append(data[q][i])
			elif data['age'][i] == "16-20歲":
				sum_16.append(data[q][i])
			elif data['age'][i] == "21-25歲":
				sum_21.append(data[q][i])
			elif data['age'][i] == "26-30歲":
				sum_26.append(data[q][i])
			elif data['age'][i] == "31-35歲":
				sum_31.append(data[q][i])
			elif data['age'][i] == "36-40歲":
				sum_36.append(data[q][i])			
			else:
				sum_41.append(data[q][i])
		final_15 = {str(p):sum_15.count(p) for p in sum_15}		
		final_16 = {str(p):sum_16.count(p) for p in sum_16}
		final_21 = {str(p):sum_21.count(p) for p in sum_21}	
		final_26 = {str(p):sum_26.count(p) for p in sum_26}	
		final_31 = {str(p):sum_31.count(p) for p in sum_31}
		final_36 = {str(p):sum_36.count(p) for p in sum_36}
		final_41 = {str(p):sum_41.count(p) for p in sum_41}
		year_value.append(final_15)
		year_value.append(final_16)
		year_value.append(final_21)
		year_value.append(final_26)
		year_value.append(final_31)
		year_value.append(final_36)
		year_value.append(final_41)
		nominal_data[q] = year_value
		for points in range(1,6):
			for items in range(0,len(nominal_data[q])):
				if str(points) not in nominal_data[q][items]:
					nominal_data[q][items][str(points)] = 0
    
	return render(request, 'result02.html',{'gender_data':json.dumps(likert_data),'year_data':json.dumps(nominal_data),'test':data})
def questionnaire03(request):
	SCOPE = ["https://spreadsheets.google.com/feeds"]
	SECRETS_FILE = "My Project-1c0a7983e6a1.json"
	SPREADSHEET = "NationalPark"

	credentials = ServiceAccountCredentials.from_json_keyfile_name(
	            SECRETS_FILE, scopes=SCOPE)

	gc = gspread.authorize(credentials)

	workbook = gc.open(SPREADSHEET)
	# Get the first sheet
	sheet = workbook.sheet1
	data = pd.DataFrame(sheet.get_all_records())

	column_names = {
					'1.您認為前往該景點的交通便捷?': 'traffic',
	                '2.您認為該景點的停車位設置合理?': 'parking_lot_location',
	                '3.您認為該景點收費合理?': 'fee',
	                '4.您認為遊樂項目豐富有趣?': 'rides',
	                '5.您認為該景點環境衛生乾淨?': 'clean',
	                '6.您認為該景點設施安全?': 'rides_safe',
	                '7.您認為該景點趣味性佳?': 'amusement',
	                '8.您認為該景點內步道規劃路線合理?': 'trail_setting',
	                '9.您認為該景點工作人員服務態度佳?': 'staff_service',
	                '10.您認為在該景點的購物選擇多樣?': 'souvenir',
	                '11.您認為景點滿足您的期待?': 'satisfied',
	                '12.您會再次選擇遊玩該景點': 'visit_again',
	                '13.您會向家人或朋友推薦該景點?': 'recommend',
	                '14.您的性別是': 'gender',
	                '15.您的年齡': 'age',
	                '16.此次隨行的同伴是?': 'parter',
	                '17.此次旅遊時間?': 'season',
	                '18.您認為該景點的分類標籤是': 'type',
	                '時間戳記':'time_mark',

	}

	data.rename(columns=column_names, inplace=True)
		 
	def likert(new_data,Q):
		Q_list = []
		sum_men = 0
		sum_women = 0
		for i in range(0, len(data['traffic'])):
		    if data['gender'][1] == "男":
		        sum_men += data['traffic'][i]
		    else:
		        sum_women += data['traffic'][i]

		new_data['man'] = sum_men
		new_data['woman'] = sum_women

	likert_questions_list = ['traffic',
							'parking_lot_location',
							'fee',
							'rides',
							'clean',
							'rides_safe',
							'amusement',
							'trail_setting',
							'staff_service',
							'souvenir',
							'satisfied',
							'visit_again',
							'recommend',
							]
		
	likert_data = {}
	nominal_data = {}
	test = []
	for q in likert_questions_list:	
		#likert(likert_data,str(q))
		sum_men = []
		sum_women = []
		value = []
		men = {}
		women = {}
		for i in range(0, len(data[q])):
		    if data['gender'][i] == "男":
		        sum_men.append(data[q][i])
		    else:
		        sum_women.append(data[q][i])
		men = {str(p):sum_men.count(p) for p in sum_men}		
		women = {str(p):sum_women.count(p) for p in sum_women}
		value.append(men)
		value.append(women)
		likert_data[q] = value
		for points in range(1,6):
			for items in range(0,len(likert_data[q])):
				if str(points) not in likert_data[q][items]:
					likert_data[q][items][str(points)] = 0

	for q in likert_questions_list:	
		sum_15 = []
		sum_16 = []
		sum_21 = []
		sum_26 = []
		sum_31 = []
		sum_36 = []
		sum_41 = []
		year_value = []
		final_15 = {}
		final_16 = {}
		final_21 = {}
		final_26 = {}
		final_31 = {}
		final_36 = {}
		final_41 = {}
		for i in range(0, len(data[q])):
			if data['age'][i] == "15歲以下":
				sum_15.append(data[q][i])
			elif data['age'][i] == "16-20歲":
				sum_16.append(data[q][i])
			elif data['age'][i] == "21-25歲":
				sum_21.append(data[q][i])
			elif data['age'][i] == "26-30歲":
				sum_26.append(data[q][i])
			elif data['age'][i] == "31-35歲":
				sum_31.append(data[q][i])
			elif data['age'][i] == "36-40歲":
				sum_36.append(data[q][i])			
			else:
				sum_41.append(data[q][i])
		final_15 = {str(p):sum_15.count(p) for p in sum_15}		
		final_16 = {str(p):sum_16.count(p) for p in sum_16}
		final_21 = {str(p):sum_21.count(p) for p in sum_21}	
		final_26 = {str(p):sum_26.count(p) for p in sum_26}	
		final_31 = {str(p):sum_31.count(p) for p in sum_31}
		final_36 = {str(p):sum_36.count(p) for p in sum_36}
		final_41 = {str(p):sum_41.count(p) for p in sum_41}
		year_value.append(final_15)
		year_value.append(final_16)
		year_value.append(final_21)
		year_value.append(final_26)
		year_value.append(final_31)
		year_value.append(final_36)
		year_value.append(final_41)
		nominal_data[q] = year_value
		for points in range(1,6):
			for items in range(0,len(nominal_data[q])):
				if str(points) not in nominal_data[q][items]:
					nominal_data[q][items][str(points)] = 0

	return render(request, 'result03.html',{'gender_data':json.dumps(likert_data),'year_data':json.dumps(nominal_data),'test':test})
def questionnaire04(request):
	SCOPE = ["https://spreadsheets.google.com/feeds"]
	SECRETS_FILE = "My Project-1c0a7983e6a1.json"
	SPREADSHEET = "street"

	credentials = ServiceAccountCredentials.from_json_keyfile_name(
	            SECRETS_FILE, scopes=SCOPE)

	gc = gspread.authorize(credentials)
	
	workbook = gc.open(SPREADSHEET)
	# Get the first sheet
	sheet = workbook.sheet1
	data = pd.DataFrame(sheet.get_all_records())

	column_names = {
					'1.您認為前往該景點的交通便捷?': 'traffic',
	                '2.您認為該景點的停車位設置合理?': 'parking_lot_location',
	                '3.您認為該景點收費合理?': 'fee',
	                '4.您認為遊樂項目豐富有趣?': 'rides',
	                '5.您認為該景點環境衛生乾淨?': 'clean',
	                '6.您認為該景點設施安全?': 'rides_safe',
	                '7.您認為該景點趣味性佳?': 'amusement',
	                '8.您認為該景點內步道規劃路線合理?': 'trail_setting',
	                '9.您認為該景點工作人員服務態度佳?': 'staff_service',
	                '10.您認為在該景點的購物選擇多樣?': 'souvenir',
	                '11.您認為景點滿足您的期待?': 'satisfied',
	                '12.您會再次選擇遊玩該景點': 'visit_again',
	                '13.您會向家人或朋友推薦該景點?': 'recommend',
	                '14.您的性別是': 'gender',
	                '15.您的年齡': 'age',
	                '16.此次隨行的同伴是?': 'parter',
	                '17.此次旅遊時間?': 'season',
	                '18.您認為該景點的分類標籤是': 'type',
	                '時間戳記':'time_mark',

	}

	data.rename(columns=column_names, inplace=True)
		 
	def likert(new_data,Q):
		Q_list = []
		sum_men = 0
		sum_women = 0
		for i in range(0, len(data['traffic'])):
		    if data['gender'][1] == "男":
		        sum_men += data['traffic'][i]
		    else:
		        sum_women += data['traffic'][i]

		new_data['man'] = sum_men
		new_data['woman'] = sum_women

	likert_questions_list = ['traffic',
							'parking_lot_location',
							'fee',
							'rides',
							'clean',
							'rides_safe',
							'amusement',
							'trail_setting',
							'staff_service',
							'souvenir',
							'satisfied',
							'visit_again',
							'recommend',
							]
		
	likert_data = {}
	nominal_data = {}
	test = []
	for q in likert_questions_list:	
		#likert(likert_data,str(q))
		sum_men = []
		sum_women = []
		value = []
		men = {}
		women = {}
		for i in range(0, len(data[q])):
		    if data['gender'][i] == "男":
		        sum_men.append(data[q][i])
		    else:
		        sum_women.append(data[q][i])
		men = {str(p):sum_men.count(p) for p in sum_men}		
		women = {str(p):sum_women.count(p) for p in sum_women}
		value.append(men)
		value.append(women)
		likert_data[q] = value
		for points in range(1,6):
			for items in range(0,len(likert_data[q])):
				if str(points) not in likert_data[q][items]:
					likert_data[q][items][str(points)] = 0

	for q in likert_questions_list:	
		sum_15 = []
		sum_16 = []
		sum_21 = []
		sum_26 = []
		sum_31 = []
		sum_36 = []
		sum_41 = []
		year_value = []
		final_15 = {}
		final_16 = {}
		final_21 = {}
		final_26 = {}
		final_31 = {}
		final_36 = {}
		final_41 = {}
		for i in range(0, len(data[q])):
			if data['age'][i] == "15歲以下":
				sum_15.append(data[q][i])
			elif data['age'][i] == "16-20歲":
				sum_16.append(data[q][i])
			elif data['age'][i] == "21-25歲":
				sum_21.append(data[q][i])
			elif data['age'][i] == "26-30歲":
				sum_26.append(data[q][i])
			elif data['age'][i] == "31-35歲":
				sum_31.append(data[q][i])
			elif data['age'][i] == "36-40歲":
				sum_36.append(data[q][i])			
			else:
				sum_41.append(data[q][i])
		final_15 = {str(p):sum_15.count(p) for p in sum_15}		
		final_16 = {str(p):sum_16.count(p) for p in sum_16}
		final_21 = {str(p):sum_21.count(p) for p in sum_21}	
		final_26 = {str(p):sum_26.count(p) for p in sum_26}	
		final_31 = {str(p):sum_31.count(p) for p in sum_31}
		final_36 = {str(p):sum_36.count(p) for p in sum_36}
		final_41 = {str(p):sum_41.count(p) for p in sum_41}
		year_value.append(final_15)
		year_value.append(final_16)
		year_value.append(final_21)
		year_value.append(final_26)
		year_value.append(final_31)
		year_value.append(final_36)
		year_value.append(final_41)
		nominal_data[q] = year_value
		for points in range(1,6):
			for items in range(0,len(nominal_data[q])):
				if str(points) not in nominal_data[q][items]:
					nominal_data[q][items][str(points)] = 0

	return render(request, 'result04.html',{'gender_data':json.dumps(likert_data),'year_data':json.dumps(nominal_data),'test':test})
def questionnaire05(request):
	SCOPE = ["https://spreadsheets.google.com/feeds"]
	SECRETS_FILE = "My Project-1c0a7983e6a1.json"
	SPREADSHEET = "DragonPark"

	credentials = ServiceAccountCredentials.from_json_keyfile_name(
	            SECRETS_FILE, scopes=SCOPE)

	gc = gspread.authorize(credentials)
	
	workbook = gc.open(SPREADSHEET)
	# Get the first sheet
	sheet = workbook.sheet1
	data = pd.DataFrame(sheet.get_all_records())

	column_names = {
					'1.您認為前往該景點的交通便捷?': 'traffic',
	                '2.您認為該景點的停車位設置合理?': 'parking_lot_location',
	                '3.您認為該景點收費合理?': 'fee',
	                '4.您認為遊樂項目豐富有趣?': 'rides',
	                '5.您認為該景點環境衛生乾淨?': 'clean',
	                '6.您認為該景點設施安全?': 'rides_safe',
	                '7.您認為該景點趣味性佳?': 'amusement',
	                '8.您認為該景點內步道規劃路線合理?': 'trail_setting',
	                '9.您認為該景點工作人員服務態度佳?': 'staff_service',
	                '10.您認為在該景點的購物選擇多樣?': 'souvenir',
	                '11.您認為景點滿足您的期待?': 'satisfied',
	                '12.您會再次選擇遊玩該景點': 'visit_again',
	                '13.您會向家人或朋友推薦該景點?': 'recommend',
	                '14.您的性別是': 'gender',
	                '15.您的年齡': 'age',
	                '16.此次隨行的同伴是?': 'parter',
	                '17.此次旅遊時間?': 'season',
	                '18.您認為該景點的分類標籤是': 'type',
	                '時間戳記':'time_mark',

	}

	data.rename(columns=column_names, inplace=True)
		 
	def likert(new_data,Q):
		Q_list = []
		sum_men = 0
		sum_women = 0
		for i in range(0, len(data['traffic'])):
		    if data['gender'][1] == "男":
		        sum_men += data['traffic'][i]
		    else:
		        sum_women += data['traffic'][i]

		new_data['man'] = sum_men
		new_data['woman'] = sum_women
						
	likert_questions_list = ['traffic',
							'parking_lot_location',
							'fee',
							'rides',
							'clean',
							'rides_safe',
							'amusement',
							'trail_setting',
							'staff_service',
							'souvenir',
							'satisfied',
							'visit_again',
							'recommend',
							]
		
	likert_data = {}
	nominal_data = {}
	test = []
	for q in likert_questions_list:	
		#likert(likert_data,str(q))
		sum_men = []
		sum_women = []
		value = []
		men = {}
		women = {}
		for i in range(0, len(data[q])):
		    if data['gender'][i] == "男":
		        sum_men.append(data[q][i])
		    else:
		        sum_women.append(data[q][i])
		men = {str(p):sum_men.count(p) for p in sum_men}		
		women = {str(p):sum_women.count(p) for p in sum_women}
		value.append(men)
		value.append(women)
		likert_data[q] = value
		for points in range(1,6):
			for items in range(0,len(likert_data[q])):
				if str(points) not in likert_data[q][items]:
					likert_data[q][items][str(points)] = 0

	for q in likert_questions_list:	
		sum_15 = []
		sum_16 = []
		sum_21 = []
		sum_26 = []
		sum_31 = []
		sum_36 = []
		sum_41 = []
		year_value = []
		final_15 = {}
		final_16 = {}
		final_21 = {}
		final_26 = {}
		final_31 = {}
		final_36 = {}
		final_41 = {}
		for i in range(0, len(data[q])):
			if data['age'][i] == "15歲以下":
				sum_15.append(data[q][i])
			elif data['age'][i] == "16-20歲":
				sum_16.append(data[q][i])
			elif data['age'][i] == "21-25歲":
				sum_21.append(data[q][i])
			elif data['age'][i] == "26-30歲":
				sum_26.append(data[q][i])
			elif data['age'][i] == "31-35歲":
				sum_31.append(data[q][i])
			elif data['age'][i] == "36-40歲":
				sum_36.append(data[q][i])			
			else:
				sum_41.append(data[q][i])
		final_15 = {str(p):sum_15.count(p) for p in sum_15}		
		final_16 = {str(p):sum_16.count(p) for p in sum_16}
		final_21 = {str(p):sum_21.count(p) for p in sum_21}	
		final_26 = {str(p):sum_26.count(p) for p in sum_26}	
		final_31 = {str(p):sum_31.count(p) for p in sum_31}
		final_36 = {str(p):sum_36.count(p) for p in sum_36}
		final_41 = {str(p):sum_41.count(p) for p in sum_41}
		year_value.append(final_15)
		year_value.append(final_16)
		year_value.append(final_21)
		year_value.append(final_26)
		year_value.append(final_31)
		year_value.append(final_36)
		year_value.append(final_41)
		nominal_data[q] = year_value
		for points in range(1,6):
			for items in range(0,len(nominal_data[q])):
				if str(points) not in nominal_data[q][items]:
					nominal_data[q][items][str(points)] = 0

	return render(request, 'result05.html',{'gender_data':json.dumps(likert_data),'year_data':json.dumps(nominal_data),'test':test})
def questionnaire06(request):
	SCOPE = ["https://spreadsheets.google.com/feeds"]
	SECRETS_FILE = "My Project-1c0a7983e6a1.json"
	SPREADSHEET = "GaHouse"

	credentials = ServiceAccountCredentials.from_json_keyfile_name(
	            SECRETS_FILE, scopes=SCOPE)

	gc = gspread.authorize(credentials)
	
	workbook = gc.open(SPREADSHEET)
	# Get the first sheet
	sheet = workbook.sheet1
	data = pd.DataFrame(sheet.get_all_records())

	column_names = {
					'1.您認為前往該景點的交通便捷?': 'traffic',
	                '2.您認為該景點的停車位設置合理?': 'parking_lot_location',
	                '3.您認為該景點收費合理?': 'fee',
	                '4.您認為遊樂項目豐富有趣?': 'rides',
	                '5.您認為該景點環境衛生乾淨?': 'clean',
	                '6.您認為該景點設施安全?': 'rides_safe',
	                '7.您認為該景點趣味性佳?': 'amusement',
	                '8.您認為該景點內步道規劃路線合理?': 'trail_setting',
	                '9.您認為該景點工作人員服務態度佳?': 'staff_service',
	                '10.您認為在該景點的購物選擇多樣?': 'souvenir',
	                '11.您認為景點滿足您的期待?': 'satisfied',
	                '12.您會再次選擇遊玩該景點': 'visit_again',
	                '13.您會向家人或朋友推薦該景點?': 'recommend',
	                '14.您的性別是': 'gender',
	                '15.您的年齡': 'age',
	                '16.此次隨行的同伴是?': 'parter',
	                '17.此次旅遊時間?': 'season',
	                '18.您認為該景點的分類標籤是': 'type',
	                '時間戳記':'time_mark',

	}

	data.rename(columns=column_names, inplace=True)
		 
	def likert(new_data,Q):
		Q_list = []
		
		sum_men = 0
		sum_women = 0
		for i in range(0, len(data['traffic'])):
		    if data['gender'][1] == "男":
		        sum_men += data['traffic'][i]
		    else:
		        sum_women += data['traffic'][i]

		new_data['man'] = sum_men
		new_data['woman'] = sum_women
						
	likert_questions_list = ['traffic',
							'parking_lot_location',
							'fee',
							'rides',
							'clean',
							'rides_safe',
							'amusement',
							'trail_setting',
							'staff_service',
							'souvenir',
							'satisfied',
							'visit_again',
							'recommend',
							]
		
	likert_data = {}
	nominal_data = {}
	test = []
	for q in likert_questions_list:	
		#likert(likert_data,str(q))
		sum_men = []
		sum_women = []
		value = []
		men = {}
		women = {}
		for i in range(0, len(data[q])):
		    if data['gender'][i] == "男":
		        sum_men.append(data[q][i])
		    else:
		        sum_women.append(data[q][i])
		men = {str(p):sum_men.count(p) for p in sum_men}		
		women = {str(p):sum_women.count(p) for p in sum_women}
		value.append(men)
		value.append(women)
		likert_data[q] = value
		for points in range(1,6):
			for items in range(0,len(likert_data[q])):
				if str(points) not in likert_data[q][items]:
					likert_data[q][items][str(points)] = 0

	for q in likert_questions_list:	
		sum_15 = []
		sum_16 = []
		sum_21 = []
		sum_26 = []
		sum_31 = []
		sum_36 = []
		sum_41 = []
		year_value = []
		final_15 = {}
		final_16 = {}
		final_21 = {}
		final_26 = {}
		final_31 = {}
		final_36 = {}
		final_41 = {}
		for i in range(0, len(data[q])):
			if data['age'][i] == "15歲以下":
				sum_15.append(data[q][i])
			elif data['age'][i] == "16-20歲":
				sum_16.append(data[q][i])
			elif data['age'][i] == "21-25歲":
				sum_21.append(data[q][i])
			elif data['age'][i] == "26-30歲":
				sum_26.append(data[q][i])
			elif data['age'][i] == "31-35歲":
				sum_31.append(data[q][i])
			elif data['age'][i] == "36-40歲":
				sum_36.append(data[q][i])			
			else:
				sum_41.append(data[q][i])
		final_15 = {str(p):sum_15.count(p) for p in sum_15}		
		final_16 = {str(p):sum_16.count(p) for p in sum_16}
		final_21 = {str(p):sum_21.count(p) for p in sum_21}	
		final_26 = {str(p):sum_26.count(p) for p in sum_26}	
		final_31 = {str(p):sum_31.count(p) for p in sum_31}
		final_36 = {str(p):sum_36.count(p) for p in sum_36}
		final_41 = {str(p):sum_41.count(p) for p in sum_41}
		year_value.append(final_15)
		year_value.append(final_16)
		year_value.append(final_21)
		year_value.append(final_26)
		year_value.append(final_31)
		year_value.append(final_36)
		year_value.append(final_41)
		nominal_data[q] = year_value
		for points in range(1,6):
			for items in range(0,len(nominal_data[q])):
				if str(points) not in nominal_data[q][items]:
					nominal_data[q][items][str(points)] = 0

	return render(request, 'result05.html',{'gender_data':json.dumps(likert_data),'year_data':json.dumps(nominal_data),'test':test})
def questionnaire07(request):
	SCOPE = ["https://spreadsheets.google.com/feeds"]
	SECRETS_FILE = "My Project-1c0a7983e6a1.json"
	SPREADSHEET = "SeaLibrary"

	credentials = ServiceAccountCredentials.from_json_keyfile_name(
	            SECRETS_FILE, scopes=SCOPE)

	gc = gspread.authorize(credentials)

	workbook = gc.open(SPREADSHEET)
	# Get the first sheet
	sheet = workbook.sheet1
	data = pd.DataFrame(sheet.get_all_records())

	column_names = {
					'1.您認為前往該景點的交通便捷?': 'traffic',
	                '2.您認為該景點的停車位設置合理?': 'parking_lot_location',
	                '3.您認為該景點收費合理?': 'fee',
	                '4.您認為遊樂項目豐富有趣?': 'rides',
	                '5.您認為該景點環境衛生乾淨?': 'clean',
	                '6.您認為該景點設施安全?': 'rides_safe',
	                '7.您認為該景點趣味性佳?': 'amusement',
	                '8.您認為該景點內步道規劃路線合理?': 'trail_setting',
	                '9.您認為該景點工作人員服務態度佳?': 'staff_service',
	                '10.您認為在該景點的購物選擇多樣?': 'souvenir',
	                '11.您認為景點滿足您的期待?': 'satisfied',
	                '12.您會再次選擇遊玩該景點': 'visit_again',
	                '13.您會向家人或朋友推薦該景點?': 'recommend',
	                '14.您的性別是': 'gender',
	                '15.您的年齡': 'age',
	                '16.此次隨行的同伴是?': 'parter',
	                '17.此次旅遊時間?': 'season',
	                '18.您認為該景點的分類標籤是': 'type',
	                '時間戳記':'time_mark',

	}

	data.rename(columns=column_names, inplace=True)
		 
	def likert(new_data,Q):
		Q_list = []
		
		sum_men = 0
		sum_women = 0
		for i in range(0, len(data['traffic'])):
		    if data['gender'][1] == "男":
		        sum_men += data['traffic'][i]
		    else:
		        sum_women += data['traffic'][i]

		new_data['man'] = sum_men
		new_data['woman'] = sum_women

	
	likert_questions_list = ['traffic',
							'parking_lot_location',
							'fee',
							'rides',
							'clean',
							'rides_safe',
							'amusement',
							'trail_setting',
							'staff_service',
							'souvenir',
							'satisfied',
							'visit_again',
							'recommend',
							]
		
	likert_data = {}
	nominal_data = {}
	test = []
	for q in likert_questions_list:	
		#likert(likert_data,str(q))
		sum_men = []
		sum_women = []
		value = []
		men = {}
		women = {}
		for i in range(0, len(data[q])):
		    if data['gender'][i] == "男":
		        sum_men.append(data[q][i])
		    else:
		        sum_women.append(data[q][i])
		men = {str(p):sum_men.count(p) for p in sum_men}		
		women = {str(p):sum_women.count(p) for p in sum_women}
		value.append(men)
		value.append(women)
		likert_data[q] = value
		for points in range(1,6):
			for items in range(0,len(likert_data[q])):
				if str(points) not in likert_data[q][items]:
					likert_data[q][items][str(points)] = 0

	for q in likert_questions_list:	
		sum_15 = []
		sum_16 = []
		sum_21 = []
		sum_26 = []
		sum_31 = []
		sum_36 = []
		sum_41 = []
		year_value = []
		final_15 = {}
		final_16 = {}
		final_21 = {}
		final_26 = {}
		final_31 = {}
		final_36 = {}
		final_41 = {}
		for i in range(0, len(data[q])):
			if data['age'][i] == "15歲以下":
				sum_15.append(data[q][i])
			elif data['age'][i] == "16-20歲":
				sum_16.append(data[q][i])
			elif data['age'][i] == "21-25歲":
				sum_21.append(data[q][i])
			elif data['age'][i] == "26-30歲":
				sum_26.append(data[q][i])
			elif data['age'][i] == "31-35歲":
				sum_31.append(data[q][i])
			elif data['age'][i] == "36-40歲":
				sum_36.append(data[q][i])			
			else:
				sum_41.append(data[q][i])
		final_15 = {str(p):sum_15.count(p) for p in sum_15}		
		final_16 = {str(p):sum_16.count(p) for p in sum_16}
		final_21 = {str(p):sum_21.count(p) for p in sum_21}	
		final_26 = {str(p):sum_26.count(p) for p in sum_26}	
		final_31 = {str(p):sum_31.count(p) for p in sum_31}
		final_36 = {str(p):sum_36.count(p) for p in sum_36}
		final_41 = {str(p):sum_41.count(p) for p in sum_41}
		year_value.append(final_15)
		year_value.append(final_16)
		year_value.append(final_21)
		year_value.append(final_26)
		year_value.append(final_31)
		year_value.append(final_36)
		year_value.append(final_41)
		nominal_data[q] = year_value
		for points in range(1,6):
			for items in range(0,len(nominal_data[q])):
				if str(points) not in nominal_data[q][items]:
					nominal_data[q][items][str(points)] = 0

	return render(request, 'result07.html',{'gender_data':json.dumps(likert_data),'year_data':json.dumps(nominal_data),'test':test})
def questionnaire08(request):
	SCOPE = ["https://spreadsheets.google.com/feeds"]
	SECRETS_FILE = "My Project-1c0a7983e6a1.json"
	SPREADSHEET = "MountainLandscape"

	credentials = ServiceAccountCredentials.from_json_keyfile_name(
	            SECRETS_FILE, scopes=SCOPE)

	gc = gspread.authorize(credentials)

	workbook = gc.open(SPREADSHEET)
	# Get the first sheet
	sheet = workbook.sheet1
	data = pd.DataFrame(sheet.get_all_records())

	column_names = {
					'1.您認為前往該景點的交通便捷?': 'traffic',
	                '2.您認為該景點的停車位設置合理?': 'parking_lot_location',
	                '3.您認為該景點收費合理?': 'fee',
	                '4.您認為遊樂項目豐富有趣?': 'rides',
	                '5.您認為該景點環境衛生乾淨?': 'clean',
	                '6.您認為該景點設施安全?': 'rides_safe',
	                '7.您認為該景點趣味性佳?': 'amusement',
	                '8.您認為該景點內步道規劃路線合理?': 'trail_setting',
	                '9.您認為該景點工作人員服務態度佳?': 'staff_service',
	                '10.您認為在該景點的購物選擇多樣?': 'souvenir',
	                '11.您認為景點滿足您的期待?': 'satisfied',
	                '12.您會再次選擇遊玩該景點': 'visit_again',
	                '13.您會向家人或朋友推薦該景點?': 'recommend',
	                '14.您的性別是': 'gender',
	                '15.您的年齡': 'age',
	                '16.此次隨行的同伴是?': 'parter',
	                '17.此次旅遊時間?': 'season',
	                '18.您認為該景點的分類標籤是': 'type',
	                '時間戳記':'time_mark',

	}

	data.rename(columns=column_names, inplace=True)
		 
	def likert(new_data,Q):
		Q_list = []
		sum_men = 0
		sum_women = 0
		for i in range(0, len(data['traffic'])):
		    if data['gender'][1] == "男":
		        sum_men += data['traffic'][i]
		    else:
		        sum_women += data['traffic'][i]

		new_data['man'] = sum_men
		new_data['woman'] = sum_women
					
	likert_questions_list = ['traffic',
							'parking_lot_location',
							'fee',
							'rides',
							'clean',
							'rides_safe',
							'amusement',
							'trail_setting',
							'staff_service',
							'souvenir',
							'satisfied',
							'visit_again',
							'recommend',
							]
		
	likert_data = {}
	nominal_data = {}
	test = []
	for q in likert_questions_list:	
		#likert(likert_data,str(q))
		sum_men = []
		sum_women = []
		value = []
		men = {}
		women = {}
		for i in range(0, len(data[q])):
		    if data['gender'][i] == "男":
		        sum_men.append(data[q][i])
		    else:
		        sum_women.append(data[q][i])
		men = {str(p):sum_men.count(p) for p in sum_men}		
		women = {str(p):sum_women.count(p) for p in sum_women}
		value.append(men)
		value.append(women)
		likert_data[q] = value
		for points in range(1,6):
			for items in range(0,len(likert_data[q])):
				if str(points) not in likert_data[q][items]:
					likert_data[q][items][str(points)] = 0

	for q in likert_questions_list:	
		sum_15 = []
		sum_16 = []
		sum_21 = []
		sum_26 = []
		sum_31 = []
		sum_36 = []
		sum_41 = []
		year_value = []
		final_15 = {}
		final_16 = {}
		final_21 = {}
		final_26 = {}
		final_31 = {}
		final_36 = {}
		final_41 = {}
		for i in range(0, len(data[q])):
			if data['age'][i] == "15歲以下":
				sum_15.append(data[q][i])
			elif data['age'][i] == "16-20歲":
				sum_16.append(data[q][i])
			elif data['age'][i] == "21-25歲":
				sum_21.append(data[q][i])
			elif data['age'][i] == "26-30歲":
				sum_26.append(data[q][i])
			elif data['age'][i] == "31-35歲":
				sum_31.append(data[q][i])
			elif data['age'][i] == "36-40歲":
				sum_36.append(data[q][i])			
			else:
				sum_41.append(data[q][i])
		final_15 = {str(p):sum_15.count(p) for p in sum_15}		
		final_16 = {str(p):sum_16.count(p) for p in sum_16}
		final_21 = {str(p):sum_21.count(p) for p in sum_21}	
		final_26 = {str(p):sum_26.count(p) for p in sum_26}	
		final_31 = {str(p):sum_31.count(p) for p in sum_31}
		final_36 = {str(p):sum_36.count(p) for p in sum_36}
		final_41 = {str(p):sum_41.count(p) for p in sum_41}
		year_value.append(final_15)
		year_value.append(final_16)
		year_value.append(final_21)
		year_value.append(final_26)
		year_value.append(final_31)
		year_value.append(final_36)
		year_value.append(final_41)
		nominal_data[q] = year_value
		for points in range(1,6):
			for items in range(0,len(nominal_data[q])):
				if str(points) not in nominal_data[q][items]:
					nominal_data[q][items][str(points)] = 0

	return render(request, 'result08.html',{'gender_data':json.dumps(likert_data),'year_data':json.dumps(nominal_data),'test':test})
def questionnaire09(request):
	SCOPE = ["https://spreadsheets.google.com/feeds"]
	SECRETS_FILE = "My Project-1c0a7983e6a1.json"
	SPREADSHEET = "SouthBeach"

	credentials = ServiceAccountCredentials.from_json_keyfile_name(
	            SECRETS_FILE, scopes=SCOPE)

	gc = gspread.authorize(credentials)

	workbook = gc.open(SPREADSHEET)
	# Get the first sheet
	sheet = workbook.sheet1
	data = pd.DataFrame(sheet.get_all_records())

	column_names = {
					'1.您認為前往該景點的交通便捷?': 'traffic',
	                '2.您認為該景點的停車位設置合理?': 'parking_lot_location',
	                '3.您認為該景點收費合理?': 'fee',
	                '4.您認為遊樂項目豐富有趣?': 'rides',
	                '5.您認為該景點環境衛生乾淨?': 'clean',
	                '6.您認為該景點設施安全?': 'rides_safe',
	                '7.您認為該景點趣味性佳?': 'amusement',
	                '8.您認為該景點內步道規劃路線合理?': 'trail_setting',
	                '9.您認為該景點工作人員服務態度佳?': 'staff_service',
	                '10.您認為在該景點的購物選擇多樣?': 'souvenir',
	                '11.您認為景點滿足您的期待?': 'satisfied',
	                '12.您會再次選擇遊玩該景點': 'visit_again',
	                '13.您會向家人或朋友推薦該景點?': 'recommend',
	                '14.您的性別是': 'gender',
	                '15.您的年齡': 'age',
	                '16.此次隨行的同伴是?': 'parter',
	                '17.此次旅遊時間?': 'season',
	                '18.您認為該景點的分類標籤是': 'type',
	                '時間戳記':'time_mark',

	}

	data.rename(columns=column_names, inplace=True)
		 
	def likert(new_data,Q):
		Q_list = []
		sum_men = 0
		sum_women = 0
		for i in range(0, len(data['traffic'])):
		    if data['gender'][1] == "男":
		        sum_men += data['traffic'][i]
		    else:
		        sum_women += data['traffic'][i]

		new_data['man'] = sum_men
		new_data['woman'] = sum_women						
	likert_questions_list = ['traffic',
							'parking_lot_location',
							'fee',
							'rides',
							'clean',
							'rides_safe',
							'amusement',
							'trail_setting',
							'staff_service',
							'souvenir',
							'satisfied',
							'visit_again',
							'recommend',
							]
		
	likert_data = {}
	nominal_data = {}
	test = []
	for q in likert_questions_list:	
		#likert(likert_data,str(q))
		sum_men = []
		sum_women = []
		value = []
		men = {}
		women = {}
		for i in range(0, len(data[q])):
		    if data['gender'][i] == "男":
		        sum_men.append(data[q][i])
		    else:
		        sum_women.append(data[q][i])
		men = {str(p):sum_men.count(p) for p in sum_men}		
		women = {str(p):sum_women.count(p) for p in sum_women}
		value.append(men)
		value.append(women)
		likert_data[q] = value
		for points in range(1,6):
			for items in range(0,len(likert_data[q])):
				if str(points) not in likert_data[q][items]:
					likert_data[q][items][str(points)] = 0

	for q in likert_questions_list:	
		sum_15 = []
		sum_16 = []
		sum_21 = []
		sum_26 = []
		sum_31 = []
		sum_36 = []
		sum_41 = []
		year_value = []
		final_15 = {}
		final_16 = {}
		final_21 = {}
		final_26 = {}
		final_31 = {}
		final_36 = {}
		final_41 = {}
		for i in range(0, len(data[q])):
			if data['age'][i] == "15歲以下":
				sum_15.append(data[q][i])
			elif data['age'][i] == "16-20歲":
				sum_16.append(data[q][i])
			elif data['age'][i] == "21-25歲":
				sum_21.append(data[q][i])
			elif data['age'][i] == "26-30歲":
				sum_26.append(data[q][i])
			elif data['age'][i] == "31-35歲":
				sum_31.append(data[q][i])
			elif data['age'][i] == "36-40歲":
				sum_36.append(data[q][i])			
			else:
				sum_41.append(data[q][i])
		final_15 = {str(p):sum_15.count(p) for p in sum_15}		
		final_16 = {str(p):sum_16.count(p) for p in sum_16}
		final_21 = {str(p):sum_21.count(p) for p in sum_21}	
		final_26 = {str(p):sum_26.count(p) for p in sum_26}	
		final_31 = {str(p):sum_31.count(p) for p in sum_31}
		final_36 = {str(p):sum_36.count(p) for p in sum_36}
		final_41 = {str(p):sum_41.count(p) for p in sum_41}
		year_value.append(final_15)
		year_value.append(final_16)
		year_value.append(final_21)
		year_value.append(final_26)
		year_value.append(final_31)
		year_value.append(final_36)
		year_value.append(final_41)
		nominal_data[q] = year_value
		for points in range(1,6):
			for items in range(0,len(nominal_data[q])):
				if str(points) not in nominal_data[q][items]:
					nominal_data[q][items][str(points)] = 0

	return render(request, 'result09.html',{'gender_data':json.dumps(likert_data),'year_data':json.dumps(nominal_data),'test':test})
def questionnaire10(request):
	SCOPE = ["https://spreadsheets.google.com/feeds"]
	SECRETS_FILE = "My Project-1c0a7983e6a1.json"
	SPREADSHEET = "BackHarbor"

	credentials = ServiceAccountCredentials.from_json_keyfile_name(
	            SECRETS_FILE, scopes=SCOPE)

	gc = gspread.authorize(credentials)

	workbook = gc.open(SPREADSHEET)
	# Get the first sheet
	sheet = workbook.sheet1
	data = pd.DataFrame(sheet.get_all_records())

	column_names = {
					'1.您認為前往該景點的交通便捷?': 'traffic',
	                '2.您認為該景點的停車位設置合理?': 'parking_lot_location',
	                '3.您認為該景點收費合理?': 'fee',
	                '4.您認為遊樂項目豐富有趣?': 'rides',
	                '5.您認為該景點環境衛生乾淨?': 'clean',
	                '6.您認為該景點設施安全?': 'rides_safe',
	                '7.您認為該景點趣味性佳?': 'amusement',
	                '8.您認為該景點內步道規劃路線合理?': 'trail_setting',
	                '9.您認為該景點工作人員服務態度佳?': 'staff_service',
	                '10.您認為在該景點的購物選擇多樣?': 'souvenir',
	                '11.您認為景點滿足您的期待?': 'satisfied',
	                '12.您會再次選擇遊玩該景點': 'visit_again',
	                '13.您會向家人或朋友推薦該景點?': 'recommend',
	                '14.您的性別是': 'gender',
	                '15.您的年齡': 'age',
	                '16.此次隨行的同伴是?': 'parter',
	                '17.此次旅遊時間?': 'season',
	                '18.您認為該景點的分類標籤是': 'type',
	                '時間戳記':'time_mark',

	}

	data.rename(columns=column_names, inplace=True)
		 
	def likert(new_data,Q):
		Q_list = []

		sum_men = 0
		sum_women = 0
		for i in range(0, len(data['traffic'])):
		    if data['gender'][1] == "男":
		        sum_men += data['traffic'][i]
		    else:
		        sum_women += data['traffic'][i]

		new_data['man'] = sum_men
		new_data['woman'] = sum_women					
	likert_questions_list = ['traffic',
							'parking_lot_location',
							'fee',
							'rides',
							'clean',
							'rides_safe',
							'amusement',
							'trail_setting',
							'staff_service',
							'souvenir',
							'satisfied',
							'visit_again',
							'recommend',
							]
		
	likert_data = {}
	nominal_data = {}
	test = []
	for q in likert_questions_list:	
		#likert(likert_data,str(q))
		sum_men = []
		sum_women = []
		value = []
		men = {}
		women = {}
		for i in range(0, len(data[q])):
		    if data['gender'][i] == "男":
		        sum_men.append(data[q][i])
		    else:
		        sum_women.append(data[q][i])
		men = {str(p):sum_men.count(p) for p in sum_men}		
		women = {str(p):sum_women.count(p) for p in sum_women}
		value.append(men)
		value.append(women)
		likert_data[q] = value
		for points in range(1,6):
			for items in range(0,len(likert_data[q])):
				if str(points) not in likert_data[q][items]:
					likert_data[q][items][str(points)] = 0

	for q in likert_questions_list:	
		sum_15 = []
		sum_16 = []
		sum_21 = []
		sum_26 = []
		sum_31 = []
		sum_36 = []
		sum_41 = []
		year_value = []
		final_15 = {}
		final_16 = {}
		final_21 = {}
		final_26 = {}
		final_31 = {}
		final_36 = {}
		final_41 = {}
		for i in range(0, len(data[q])):
			if data['age'][i] == "15歲以下":
				sum_15.append(data[q][i])
			elif data['age'][i] == "16-20歲":
				sum_16.append(data[q][i])
			elif data['age'][i] == "21-25歲":
				sum_21.append(data[q][i])
			elif data['age'][i] == "26-30歲":
				sum_26.append(data[q][i])
			elif data['age'][i] == "31-35歲":
				sum_31.append(data[q][i])
			elif data['age'][i] == "36-40歲":
				sum_36.append(data[q][i])			
			else:
				sum_41.append(data[q][i])
		final_15 = {str(p):sum_15.count(p) for p in sum_15}		
		final_16 = {str(p):sum_16.count(p) for p in sum_16}
		final_21 = {str(p):sum_21.count(p) for p in sum_21}	
		final_26 = {str(p):sum_26.count(p) for p in sum_26}	
		final_31 = {str(p):sum_31.count(p) for p in sum_31}
		final_36 = {str(p):sum_36.count(p) for p in sum_36}
		final_41 = {str(p):sum_41.count(p) for p in sum_41}
		year_value.append(final_15)
		year_value.append(final_16)
		year_value.append(final_21)
		year_value.append(final_26)
		year_value.append(final_31)
		year_value.append(final_36)
		year_value.append(final_41)
		nominal_data[q] = year_value
		for points in range(1,6):
			for items in range(0,len(nominal_data[q])):
				if str(points) not in nominal_data[q][items]:
					nominal_data[q][items][str(points)] = 0

	return render(request, 'result10.html',{'gender_data':json.dumps(likert_data),'year_data':json.dumps(nominal_data),'test':test})
