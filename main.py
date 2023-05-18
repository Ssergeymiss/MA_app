import numpy as np
import pandas as pd
from tensorflow import keras
import streamlit as st
import pandas as pd
import xlsxwriter
import mysql.connector
import os


def fetch_table_data(table_name):

    cnx = mysql.connector.connect(
        host="193.164.150.80",
        database='fedinst_office',
        user='user_view',
        password='vH56ui2GdKHQ7Em'
    )

    cursor = cnx.cursor()
    #cursor.execute('select * from ' + table_name)

    # if table_name == 'qq85_sttlkofficeinvoice':
    #     cursor.execute('select id, user_id from ' + table_name)
    # if table_name == 'qq85_sttlkofficepayment':
    #     cursor.execute('select invoice_id from ' + table_name)
    if table_name == 'qq85_stthomeoffice_label':
        cursor.execute('select * from ' + table_name)
    # else:
    #     cursor.execute('select * from ' + table_name)
    if table_name == 'qq85_stthomeofficereport1':
        cursor.execute('select user_id, sumpay, reportdate from ' + table_name)
    header = [row[0] for row in cursor.description]

    rows = cursor.fetchall()


    cnx.close()

    return header, rows


def export(table_name):

    workbook = xlsxwriter.Workbook(table_name + '.xlsx')
    worksheet = workbook.add_worksheet('MENU')

    # Create style for cells
    header_cell_format = workbook.add_format({'bold': True, 'border': True, 'bg_color': 'yellow'})
    body_cell_format = workbook.add_format({'border': True})

    header, rows = fetch_table_data(table_name)

    row_index = 0
    column_index = 0

    for column_name in header:
        worksheet.write(row_index, column_index, column_name, header_cell_format)
        column_index += 1

    row_index += 1
    for row in rows:
        column_index = 0
        for column in row:
            worksheet.write(row_index, column_index, column, body_cell_format)
            column_index += 1
        row_index += 1

    print(str(row_index) + ' rows written successfully to ' + workbook.filename)

    # Closing workbook
    workbook.close()



# Загружаем необходимые таблицы из БД
# export('qq85_sttlkofficeinvoice')#Заявки на услуги
# export('qq85_stthomeoffice_lpr')#Заявки на услуги
# export('qq85_sttlkofficepayment')#Оплаченные заявки

# export('qq85_stthomeoffice_label_dict')
# позволяет преобразовать данные из xlsx to csv
def refactor_data(data_path,name_new):
    read_file = pd.read_excel (data_path+".xlsx")
    read_file.to_csv (name_new,
                      index = None,
                      header=True)


# refactor_data('qq85_sttlkoffice_lpr',"lpr.csv")
# refactor_data('qq85_sttlkofficeinvoice',"invoice.csv")
# refactor_data('qq85_stthomeoffice_label',"label.csv")

st.title("Анализ конверсии менеджеров")
st.write("** Данное приложение позволяет предсказать рост/упадок общей конверсии на основании последних разговоров с клиентами")

if os.path.isfile("qq85_stthomeofficereport1.xlsx") == False:
    export('qq85_stthomeofficereport1')  # Заявки нулевые
    refactor_data('qq85_stthomeofficereport1', "report.csv")
    st.write("qq85_stthomeofficereport1 успешно загружена")
else:
    st.write("qq85_stthomeofficereport1 успешно загружена")
if os.path.isfile("qq85_stthomeoffice_label.xlsx") == False:
    export('qq85_stthomeoffice_label')#Заявки на услуги
    refactor_data('qq85_stthomeoffice_label', "label.csv")
    st.write("qq85_stthomeoffice_label успешно загружена")
else:
    st.write("qq85_stthomeoffice_label успешно загружена")


report=pd.read_csv("report.csv")
report['reportdate'] =  pd.to_datetime(report['reportdate'], format='%d.%m.%Y')
print(report["reportdate"][0])
r_user_id=report["user_id"]
check_user=r_user_id.tolist()
r_data=report["reportdate"]

r_data=r_data.tolist()

import datetime as dt

while True:
    print("Введите id менеджера")
    #your_name = st.text_input("Enter your name")
    # user_id_initial = st.text_input("Введите id менеджера")
    # user_id_initial=int(user_id_initial)
    user_id_initial=st.text_input("Введите user_id менеджера")
    user_id_initial=int(user_id_initial)
    if user_id_initial in check_user:
        #print("Введите начальный invoice_id")
        id_initial =  st.text_input("Введите начальную дату dd-mm-yyyy")
        id_initial=str(id_initial)
        #id_initial=str(input())
        id_initial=dt.datetime.strptime(id_initial,'%d-%m-%Y')
        id_end=st.text_input("Введите конечную дату dd-mm-yyyy")
        id_end = str(id_end)
        #id_end=str(input())
        id_end=dt.datetime.strptime(id_end, '%d-%m-%Y')
        #id_initial=int(id_initial)

        break
    else:
        continue
print(id_initial,id_end)
report=report.loc[(report['reportdate'] >= id_initial)
                     & (report['reportdate'] < id_end)]
report=report[report.user_id==user_id_initial]
#report=report[report.reportdate==id_initial]



st.write("Сформированы записи по менеджеру")
st.write(report.head(),"Количество записей",len(report),sep="\n")


r_user_id=report["user_id"]

r_unik_user=r_user_id.unique()
r_user_count=r_user_id.tolist()

r_Manager_df={}

for i in r_unik_user:

    r_Manager_df[i] = r_user_count.count(i)
r_ls = list(r_Manager_df.items())

df_M=pd.DataFrame(columns=["user_id","count"])


for i in range(len(r_ls)):
   df_M.loc[i] = r_ls[i]# в этом датафрейме хранятся по колонкам идентификатор и количество заявок

report_top=report[report.sumpay != 0]

top_user_id=report_top["user_id"]

t_unik_user=top_user_id.unique()
t_user_count=top_user_id.tolist()

t_Manager_df={}

for i in t_unik_user:

    t_Manager_df[i] = t_user_count.count(i)
t_ls = list(t_Manager_df.items())

t_df_M=pd.DataFrame(columns=["top_user_id","top_count"])


for i in range(len(t_ls)):
   t_df_M.loc[i] = t_ls[i]# в этом датафрейме хранятся по колонкам идентификатор и количество заявок

t_df_M.head()


df_M=df_M.loc[df_M.user_id.isin(t_df_M.top_user_id)==True]

df_M=df_M.sort_values(by=["user_id"])
t_df_M=t_df_M.sort_values(by=["top_user_id"])

df_M = df_M.reset_index(drop=True)
top_count=t_df_M.top_count.tolist()

df_M["top_count"]=top_count

convers=[]

for i in range(len(df_M["user_id"])):
    convers.append(df_M["top_count"][i]/df_M["count"][i])# Считаем конверсию

df_M["convers"]=convers# Добавим столбец Конверсии в наш датафрейм

label=pd.read_csv("label.csv")



df_label=label.loc[label.user_id.isin(df_M["user_id"])==True]# Исключим из датафрейма все значения, которые не соответствуют таблице df_M


user_label=df_label["user_id"].unique()
user_label=sorted(user_label)

df_M=df_M.loc[df_M.user_id.isin(user_label)==True]# сключим из датафрейма все значения, которые не соответствуют таблице df_label



df_label=df_label.sort_values(by=["user_id"])

df_M = df_M.reset_index(drop=True)
df_label = df_label.reset_index(drop=True)

telling=st.text_input("Введите количество последних разговоров")
telling=int(telling)
df_label=df_label[-telling:]
labels=[]
for i in range(len(df_M["user_id"])):#Добавим в список среднее значения всех лэйблов на менеджера
    labels.append(#[df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label1'].mean(),
                   #df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label2'].mean(),
                   #df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label3'].mean(),
                   [df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label4'].mean(),
                   df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label5'].mean(),
                   df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label6'].mean(),
                   df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label7'].mean(),
                   df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label8'].mean(),
                   df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label9'].mean(),
                   #df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label10'].mean(),
                   #df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label11'].mean(),
                   #df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label12'].mean(),
                  # df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label13'].mean(),
                   #df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label14'].mean(),
                   #df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label15'].mean(),
                   df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label16'].mean(),
                   df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label17'].mean(),
                   df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label18'].mean(),
                   df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label19'].mean(),
                   df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label20'].mean(),
                   #df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label21'].mean(),
                   #df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label22'].mean(),
                   #df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label23'].mean(),
                   df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label24'].mean(),
                   df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label25'].mean(),
                   df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label26'].mean(),
                   df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label27'].mean(),
                   df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label28'].mean(),
                   df_label.loc[df_label['user_id'] == df_M["user_id"][i], 'label29'].mean(),
                   ])




col=[#"label1","label2","label3",
     "label4","label5","label6","label7","label8","label9",
     #'label10',"label11","label12","label13","label14","label15",
     "label16","label17","label18","label19",'label20',
     #"label21","label22","label23",
     "label24","label25","label26","label27","label28","label29"]



Averange_M=pd.DataFrame(labels,columns=col)

A_user_id=df_M.user_id.tolist()
Averange_M.insert (loc= 0 , column='user_id', value=A_user_id)

A_convers=[]
for i in range(len(df_M["user_id"])):
    A_convers.append(df_M["top_count"][i]/df_M["count"][i])


answer =  st.text_input("Нажмите 1 если вы хотите сформировать анализ")
answer=int(answer)

if answer==0:

    Averange_M["convers"]=A_convers
    Averange_M.to_excel("Averange_M_df.xlsx")
    refactor_data('Averange_M_df', "Averange_M_df.csv")

else:
    Averange_M.to_excel("Averange_M.xlsx")
    refactor_data('Averange_M',"Averange_M.csv")

st.write(df_M)
st.write("Реальная конверсия за данный период",convers)


def load_model():
    model = keras.models.load_model("model_Man_3.2.h5")
    model.load_weights("Manager_weight_4.2.h5")
    if model:
        st.write("Модель загружена!")
    return model

def Preprocess_df(arr):
    st.write("Усредненные значения меток")
    arr=arr.drop(arr.columns[[0]], axis=1)
    st.write(arr)
    arr = arr.astype(float)
    arr = arr.to_numpy()
    arr = np.array(arr)

    #arr=arr.drop(["Unnamed: 0","user_id"],axis=1)

    #arr=scaler.fit_transform(arr)
    return arr

def print_predictions(preds):
    print(preds)



model = load_model()



result = st.button('Провести анализ')

import os
if result:
    # Предварительная обработка изображения
    x = Preprocess_df(Averange_M)
    # Распознавание изображения
    preds = model.predict(x)
    # Выводим заголовок результатов распознавания жирным шрифтом
    # используя форматирование Markdown
    st.write('**Конверсия, вычисленная по последним ',+ telling,' разговорам:**')
    # Выводим результаты распознавания
    #print(preds)
    st.write(preds)

    os.remove("Averange_M.csv")
    os.remove("Averange_M.xlsx")
    st.write("Объяснение влияния меток")
    st.image("limepng.png")


