# coding=utf8
import os
import shutil
import re
import urllib.request
import urllib.error
#import requests

from bs4 import BeautifulSoup

def cutspace(sentence):
    return sentence.replace(" ","")
def Redeem_date(yearmonth):#到兌獎年月份的網址
    url="https://www.etax.nat.gov.tw/etw-main/web/ETW183W2_"+yearmonth
#htmlContent = urllib.request.urlopen(url).read()
    with urllib.request.urlopen(url) as response:
        html = response.read()
    return html
# =============================================================================
# https://www.etax.nat.gov.tw/etw-main/web/ETW183W2_10403/
# https://www.etax.nat.gov.tw/etw-main/web/ETW183W3_10911/
# https://www.etax.nat.gov.tw/etw-main/web/ETW183W2_10909/
# =============================================================================
def crawler_awards(html):
    soup = BeautifulSoup(html, 'html.parser')
    firstPrize=[]
    addSixPrize=[]
    numadd3=''
    
    #特別獎
    specialPrize = soup.find(headers="specialPrize").string
    specialPrize=cutspace(specialPrize)
    
    #特獎
    grandPrize = soup.find(headers="grandPrize").string
    grandPrize = cutspace(grandPrize)
    
    #頭獎
    firstPrize_nostr = soup.find_all('p',limit=3)
    for i in range(0,firstPrize_nostr.__len__(),1):
        firstPrize.append(str(firstPrize_nostr[i]))
    #增開六獎
    addSixPrize_nostr = soup.find(headers="addSixPrize").string
    addSixPrize_nostr = cutspace(addSixPrize_nostr)
    
    for i in range(0,addSixPrize_nostr.__len__(),1):
        for sixp in addSixPrize_nostr[i].split('、'):
            numadd3=numadd3+sixp
            if numadd3.__len__()==3:
                addSixPrize.append(numadd3)
                numadd3 = ''
                
# =============================================================================
#     print(specialPrize)
#     print(grandPrize)
#     print(firstPrize)
#     print(addSixPrize)
# =============================================================================
    return specialPrize,grandPrize,firstPrize,addSixPrize
# =============================================================================
# gg=filter(str.isdigit, results)
# print(gg)
# =============================================================================
# =============================================================================
# soup = requests.get(url)
# if soup.status_code == requests.codes.ok:
#     results = soup.find_all(class_="number")
#     print(results)
# =============================================================================
def get_Awarded(specialPrize,grandPrize,firstPrize,addSixPrize):
    while(True):
        aw=False
        receipt = input("請輸入統一發票:")
        while (True):
            if receipt.isdigit() and receipt.__len__()==8:
                break
            else:
                receipt = input('請輸入正確格式：')
        #8位數號碼與特別獎號碼相同者獎金1,000萬元
        if specialPrize.find(receipt)!=-1:
            print("恭喜，獲得特別獎1000萬")
            aw=True
        #8位數號碼與特獎號碼相同者獎金200萬元
        if grandPrize.find(receipt)!=-1:
            print("恭喜，獲得特獎200萬")
            aw=True
        #8位數號碼與頭獎號碼相同者獎金20萬元
        for i in range(0,firstPrize.__len__(),1):
            if firstPrize[i].find(receipt,3)!=-1:
                print("恭喜，獲得頭獎20萬")
                aw=True
            #末7 位數號碼與頭獎中獎號碼末7 位相同者各得獎金4萬元
            elif firstPrize[i].find(receipt[1::],4)!=-1:
                print("恭喜，獲得二獎40000元")
                aw=True
            #末6 位數號碼與頭獎中獎號碼末6 位相同者各得獎金1萬元
            elif firstPrize[i].find(receipt[2::],5)!=-1:
                print("恭喜，獲得三獎10000元")
                aw=True
            #末5 位數號碼與頭獎中獎號碼末5 位相同者各得獎金4千元
            elif firstPrize[i].find(receipt[3::],6)!=-1:
                print("恭喜，獲得四獎4000元")
                aw=True
            #末4 位數號碼與頭獎中獎號碼末4 位相同者各得獎金1千元
            elif firstPrize[i].find(receipt[4::],7)!=-1:
                print("恭喜，獲得五獎1000元")
                aw=True
            #末3 位數號碼與 頭10909獎中獎號碼末3 位相同者與增開六獎號碼相同者各得獎金2百元
            elif firstPrize[i].find(receipt[5::],8)!=-1:
                print("恭喜，獲得六獎200元")
                aw=True
        for i in range(0,addSixPrize.__len__(),1):
            if receipt.find(addSixPrize[i],5)!=-1:
                print("恭喜，獲得增開六獎200元")
                aw=True
                break
        if aw!=True:
            print("可惜，沒有獲獎")
        countie=input("要繼續兌獎嗎?(y/n)")
        if(countie=='n'):
            break
        
def init():
    #輸入年月
    yearmonth = input("請輸入年月(EX:10711、10909):")
    #Ministry of Finance財政部
    MFurl = Redeem_date(yearmonth)
    specialPrize,grandPrize,firstPrize,addSixPrize = crawler_awards(MFurl)
    get_Awarded(specialPrize,grandPrize,firstPrize,addSixPrize)
if __name__=='__main__':
    init()