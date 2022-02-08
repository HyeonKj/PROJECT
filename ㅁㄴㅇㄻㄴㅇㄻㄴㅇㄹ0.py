# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 11:41:53 2022

@author: user
"""

class Crawler:
    def __init__(self,url):
        self.url = "http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13"
       
    def crawl(self,url):
        
    def SaveDataToDB(self):
        print("Now saving")
        
        
url = "http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13"
crawler=Crawler(url)
