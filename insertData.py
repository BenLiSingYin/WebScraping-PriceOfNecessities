#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 14:08:34 2021

@author: Ben Li
"""

import sqlite3
import pandas as pd

class GOODSdb():
    
    def insertData(self,B,G,D,T,P):
        conn = sqlite3.connect('AllGoodsPrice.db')
        
        c = conn.cursor()
        
        #If you wanna to create a new database, you can unlock below coding and hide the "secord execute"
        
        '''
            c.execute(CREATE TABLE GOODS
                  (BRAND  TEXT  NOT  NULL,
                    GOODS TEXT NOT NULL,
                    DATE TEXT NOT NULL,
                    TYPE TEXT NOT NULL,
                    PRICE TEXT NOT NULL
                    );)
        conn.commit()
        conn.close()
        
        '''
        
        #secord execute
        c.execute('INSERT INTO GOODS (BRAND,GOODS,DATE,TYPE,PRICE) VALUES (\"{}\",\"{}\",\"{}\",\"{}\",\"{}\");'.format(B,G,D,T,P))
        
        #cursor = c.execute('SELECT * FROM GOODS;')
        conn.commit()
                  
        conn.close()
        
        #return cursor
        
    def showData(self):
        conn = sqlite3.connect('AllGoodsPrice.db')
        
        conn.row_factory = sqlite3.Row
        
        result = []
        
        c = conn.cursor()
        
        cursor = c.execute('SELECT * FROM GOODS;')
        
        for i in cursor:
            result.append(dict(i))
            
        return pd.DataFrame(result)
        
        
        