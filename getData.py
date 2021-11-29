#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 11:52:58 2021

@author: user
"""

import pandas as pd
import time
from bs4 import BeautifulSoup
import undetected_chromedriver.v2 as uc
from insertData import GOODSdb
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def scrapData():
    goods_list = pd.read_csv('material/goods_list.csv', engine='python', sep=',', header=0, names=['Brand', 'Goods Name', 'URL', 'UpdateDate'])

    driver = uc.Chrome()
    
    result = []
    
    for i in range(0,len(goods_list)):
        
        driver.get(goods_list.iloc[i]['URL'])
        time.sleep(5)
        
        html = driver.page_source
        
        soup = BeautifulSoup(html)
        
        record = soup.findAll('div',{'class':'weekly-promo'})
        
        
        for j in range(1,len(record)):
            
            date = record[j].find('div',{'class':'dated'})['data-date']
            
            for z in record[j].findAll('div',{'class':'promo'}):
                temp = {'BRAND':goods_list.iloc[i]['Brand'], 'GOODS':goods_list.iloc[i]['Goods Name'], 'DATE':date}
                temp['TYPE'] = z['data-category']
                temp['PRICE'] = z.find('span',{'data-price-type':'single'}).text.split(' ')[-1]
                if(temp['PRICE'] == "--"):
                    temp['PRICE'] = '0'
                
                result.append(temp)
    
    driver.close()        
            
    df = pd.DataFrame(result)
    
    
    print('scrapping successfully ')

    return df


def check_and_insert():
    db = GOODSdb()
    
    old_result = db.showData()
    result = scrapData()
    
    try:
        record = pd.merge(old_result,result, how="outer", indicator=True)
        new_record = record[record['_merge'] == 'right_only'].iloc[:,:-1]
        
        for i in range(0,len(new_record)):
            db.insertData(new_record.iloc[i]['BRAND'], new_record.iloc[i]['GOODS'], new_record.iloc[i]['DATE'], new_record.iloc[i]['TYPE'], new_record.iloc[i]['PRICE'])
            
        print('updating successfully ')
        
    except:
        print('updating Nothing')
        
def create_excel():
    db = GOODSdb()
    check_and_insert()
    result = db.showData()
    
    file_name = "excel/" + time.strftime("%D").replace('/','-') + '-daily_price.xlsx'
    
    result.to_excel(file_name)
    
    print('creating successfully ')
    
    return file_name

#this function is mainly helping you upload the data to the Google Sheet
'''def upload_file():
    
    file_name = create_excel()
    
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('../client_secret.json', scope)
    print('pass')
    client = gspread.authorize(creds)
    print('pass2')
    sheet = client.open_by_key('').sheet1
    #sheet = client.open("消委會 - 每日更新").sheet1
    df = pd.read_excel(file_name)
    df = df.iloc[:,1:]
    
    sheet.clear()
    record = []
    #columns
    col = list(df.columns)
    record.append(col)
    
    for i in range(1,len(df)):
        
        temp = list(df.iloc[i])
        record.append(temp)
        
    sheet.append_rows(record)
    
    print('uploading successfully ')'''

create_excel()
