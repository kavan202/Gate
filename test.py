import pandas as pd
import requests
from bs4 import BeautifulSoup
def mark(url):
    paper=requests.get(url).text
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
    if (result['Q_ID'][0] == 22848211141):
        ans = pd.read_csv('K.csv')
        ans["Key"] = ans["Key"].str.replace(";", ",")
    else:
        ans = pd.read_csv('Goti.csv')
        ans["Key"] = ans["Key"].str.replace(" ", "")
        
    fr = pd.merge(result, ans, on=['Q_ID','Type'], how='inner')
    fr = fr.drop(columns=['Q.No'])
    x=0
    for i in range(len(fr)):
        if fr['Status'][i] in ['Not Attempted and Marked For Review','Not Answered']:
            pass
        else :
            if fr['Type'][i] == 'NAT':
                l,h = map(float, fr['Key'][i].split('to'))
                if l <= float(fr['Answer'][i]) <= h:
                    x+=fr['Marks'][i]
            else :
                if fr['Answer'][i] == fr['Key'][i]:
                    x+=fr['Marks'][i]
                else:
                    if fr['Type'][i] == 'MCQ':
                        x-=(fr['Marks'][i])*0.33
    return x