from __future__ import print_function
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

SCOPE = ["https://spreadsheets.google.com/feeds"]
SECRETS_FILE = "My Project-1c0a7983e6a1.json"
SPREADSHEET = "questions response"

credentials = ServiceAccountCredentials.from_json_keyfile_name(
            SECRETS_FILE, scopes=SCOPE)

gc = gspread.authorize(credentials)
print("The following sheets are available")
print(gc)
print("\n")
for sheet in gc.openall():
        print("{} - {}\n\n\n".format(sheet.title, sheet.id))

workbook = gc.open(SPREADSHEET)
# Get the first sheet
sheet = workbook.sheet1
print(sheet.acell("b2").value)

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
	 
question_sort = ['traffic',
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
				'gender',
				'age',
				'parter',
				'season',
				'type',
				'time_mark',
				]

data = data[question_sort]

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



'''def likert(new_data,Q):
	Q_list = []
	for i in data[Q]:
		if i == '非常同意':
			Q_list.append(5)
		elif i =='同意':
			Q_list.append(4)
		elif i =='普通':
			Q_list.append(3)
		elif i =='不同意':
			Q_list.append(2)
		elif i =='非常不同意':
			Q_list.append(1)
		else:
			Q_list.append("")
	Q_list.append(np.mean(Q_list))
	Q_list.append(np.std(Q_list))
	new_data[Q] = Q_list
	#new_data = pd.DataFrame(data = new_data)
	
likert_data = {}
for q in likert_questions_list:	
	likert(likert_data,str(q))
print(likert_data)'''

nominal_question_list = ['gender',
						'age',
						'parter',
						'season',
						'type',
						'time_mark',
						]

def nominal_question(new_data,Q):
	Q_list = []
	for i in data[Q]:
		if i == '41歲以上':
			Q_list.append(7)
		elif i =='36-40歲':
			Q_list.append(6)
		elif i =='31-35歲':
			Q_list.append(5)
		elif i =='26-30歲' or i == '單獨旅行' or i == '冬季(12-2月)' or i == '特殊遊憩區':
			Q_list.append(4)
		elif i =='21-25歲' or i == '朋友' or i == '秋季(9-1月)' or i == '自然':
			Q_list.append(3)
		elif i =='16-20歲' or i == '家庭' or i == '夏季(6-8月)' or i == '主題遊樂園區':
			Q_list.append(2)
		elif i =='15歲以下' or i == '伴侶' or i == '春季(3-5月)' or i == '人文' or i == '女':
			Q_list.append(1)
		elif i =='男':
			Q_list.append(0)
		else:
			Q_list.append("")
	#Q_list.append(np.mean(Q_list))
	#Q_list.append(np.std(Q_list))
	new_data[Q] = Q_list

nominal_data = {}
for nq in nominal_question_list:
	nominal_question(nominal_data,str(nq))
print(nominal_data)

'''test_data = data["gender"].value_counts(normalize = True)
x_axis = []
y_axis = []
for x, y in test_data.iteritems():
	if x == '男':
		x_axis.append('man')
	elif x =='女':
		x_axis.append('woman')
	else:
		x_axis.append("")
	#x_axis.append(x)
	y_axis.append(y * 100)
print(x_axis)
print(y_axis)
colors = []
for x_value in x_axis:
	colors.append('g')
	plt.style.use("ggplot")
	x_pos = np.arange(len(x_axis))
	rects = plt.bar(x_pos, y_axis, width = 0.7, color = colors, align = "center", alpha = 0.7)
for rect in rects:
	rec_x = rect.get_x()
	rec_width = rect.get_width()
	rec_height = rect.get_height()
	height_format = float("{0:.1f}".format(rec_height))
plt.text(rec_x + rec_width / 2, rec_height , str(height_format) + "%", horizontalalignment = "center", verticalalignment = 'bottom')
plt.xticks(x_pos, x_axis)
plt.xlabel("gender")
plt.ylabel("Frequency Distribution")
plt.title("gender frequency distribution")
plt.legend(loc = 1)
plt.tight_layout()
#plt.savefig(image_path_name1, dpi = 100)
plt.show()

print(test_data)'''



#data.timestamp = pd.to_datetime(data.timestamp)

