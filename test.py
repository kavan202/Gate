import pandas as pd
import requests
from bs4 import BeautifulSoup
def mark(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    paper=requests.get(url,headers=headers).text
    soup= BeautifulSoup(paper,'html.parser')
    result = pd.DataFrame(columns=["Type", "Q_ID","Status","Answer"])
    for i in soup.find_all('td',class_='bold'):
        if i.text in ['MCQ','MSQ']:
            Type = i.text
            Q_ID = int(i.find_next('td',class_='bold').text)
            Status = i.find_next('td',class_='bold').find_next('td',class_='bold').text
            Answer = i.find_next('td',class_='bold').find_next('td',class_='bold').find_next('td',class_='bold').text
            result.loc[len(result)] = [Type, Q_ID, Status, Answer]
        elif i.text in ['NAT']:
            Type = i.text
            Q_ID = int(i.find_next('td',class_='bold').text)
            Status = i.find_next('td',class_='bold').find_next('td',class_='bold').text
            Answer = i.find_previous('td',class_='bold').text
            result.loc[len(result)] = [Type, Q_ID, Status, Answer]
    if result.empty:
        return 0
    if (result['Q_ID'].iloc[0] == 22848211141):
        ans = pd.read_csv('K.csv')
        ans["Key"] = ans["Key"].str.replace(";", ",")
    else:
        ans = pd.read_csv('Goti.csv')
        ans["Key"] = ans["Key"].str.replace(" ", "")
        
    fr = pd.merge(result, ans, on=['Q_ID','Type'], how='inner')
    fr = fr.drop(columns=['Q.No'])
    x=0
    for i in range(len(fr)):
        status = fr['Status'].iloc[i]
        q_type = fr['Type'].iloc[i]
        answer = fr['Answer'].iloc[i]
        key = fr['Key'].iloc[i]
        marks_val = fr['Marks'].iloc[i]
        
        if status in ['Not Attempted and Marked For Review', 'Not Answered']:
            pass
        else:
            if q_type == 'NAT':
                l, h = map(float, key.split('to'))
                if l <= float(answer) <= h:
                    x += marks_val
            else:
                if answer == key:
                    x += marks_val
                else:
                    if q_type == 'MCQ':
                        x -= (marks_val) * 0.33
    return x
