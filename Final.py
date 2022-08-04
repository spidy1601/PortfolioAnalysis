#!/usr/bin/env python
# coding: utf-8

# # This Program is capable of the followings
# **1.] To see Graphically "How your Stock Porfolio has performed against standard benchmark(Here I have taken Sensex) and invested amount over a period of time"**
# 
# **2.] To see "How invidual Stock has Performed over time" - its individual value as well as total value Graphically**
# 
# **3.] Total Value of your Portfolio**
# 
# **4.] Trailing PE Ratio of the Portfolio**
# 
# **5.] Percentage Change of X Day/s**
# 
# **6.] Amount Change of X Day/s**
# 
# **7.] Pie Chart representing Allocation of shares in the Portfolio** 
# 
# **8.] Difference of the Current Value from the maximum Value**
# 
# **9.] Printing Summary**
# 
# **10.] Exported Templated Details to Pdf**

# In[51]:


import yfinance as yf #This is an API which fetch real time financial data 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go #For Graphical representation
from itertools import cycle
from pandas_datareader import data as pdr
import datetime
# from datetime import datetime
import os
import re
yf.pdr_override()


# In[52]:


#Input_Excel_sheet=input("Enter your ")


# In[53]:


#All the inputs required
UserName = input("Enter UserName (i.e Your Name): ")
if not os.path.exists("Users"):
    os.mkdir("Users")
if not os.path.exists("Users/"+UserName):
    os.mkdir("Users/"+UserName)
if not os.path.exists("Users/"+UserName+"/images"):
    os.mkdir("Users/"+UserName +"/images")
if not os.path.exists("Users/"+UserName+"/resources"):
    os.mkdir("Users/"+UserName+"/resources")
sheet = pd.read_excel("Users/"+UserName+"/resources/"+UserName+"_data.xlsx")
#StockIndex = int(input("Enter the SR no according to the excel file for individual Stocks: ")) -1
GraphFileName = UserName+"Graph.png"
#Days=int(input("Enter Number of Days X, i.e Difference,Change : Today - X days:= ")) #Enter Number of days you want the Percentage change(mind it this is not days but sessions) 
PieFileName = UserName+"Pie.png"
PdfFileName = UserName+"_PortFolio.pdf"


# In[54]:


# sheet = pd.read_excel(input("Please, Enter Location of the file: "))
MultipliedInvested = pd.DataFrame(sheet, columns = ['PUR_DATE','TOTAL_INVESTMENT'])
MultipliedInvested = MultipliedInvested.groupby(MultipliedInvested['PUR_DATE'].dt.strftime('%Y-%m-%d'))['TOTAL_INVESTMENT'].sum()
MultipliedInvested.name = "Invested"
MultipliedInvested = MultipliedInvested.to_frame()
MultipliedInvested=MultipliedInvested.reset_index()
MultipliedInvested.sort_values('PUR_DATE')

sumInvest=0
listttt = []
for i in MultipliedInvested['Invested']:
    sumInvest += i
    listttt.append(sumInvest)
MultipliedInvested['Till_now'] = listttt
MultipliedInvested.plot(x='PUR_DATE',y='Till_now')
#for inserting today's date data 
tod= datetime.date.today()
tod=tod.strftime("%Y-%m-%d")
MultipliedInvested.loc[len(MultipliedInvested.index)] = [tod,0,MultipliedInvested.iloc[-1,-1] ]
MultipliedInvested


# In[55]:


def PortfolioValue(sheet,currentDate):
    dataQuantity = sheet['QTY']
    datalist1 = []
    global total_rows
    total_rows=sheet["COMP_NAME"].count()
    for i in range(total_rows):
        data = pdr.get_data_yahoo(sheet.COMP_SYMBOL[i],start=sheet.PUR_DATE[i],end=currentDate)
        data.fillna(method='ffill', inplace=True)
        multiplyQuantity = data['Close'] * dataQuantity[i] #Only CurrentValue from that stock
        datalist1.append(multiplyQuantity)
    print("Total Value of your Portfolio is : ",end="")
    global Current_Value
    Current_Value = sum([datalist1[i][-1] for i in range(total_rows)])
    print(Current_Value) #3277975.437860489
    return datalist1,dataQuantity


# In[56]:


def PlotPortfolioValues(datalist1,GraphFileName=None,compare=None):
    Total = pd.concat(datalist1,axis=1,join = 'outer')
    Total = Total.fillna(0)
    global Date_wise_Total
    Date_wise_Total = Total.transpose()
    Date_wise_Total = Date_wise_Total.sum()
    Date_wise_Total.name = "Value"
    Date_wise_Total = Date_wise_Total.to_frame()
    Date_wise_Total=Date_wise_Total.reset_index()
    #Date_wise_Total
    drawGraph(list(Date_wise_Total.Date),list(Date_wise_Total.Value),compare=compare,text="Portfolio Value over Time",showInvest='yes',GraphFileName=GraphFileName)
      


# In[57]:


def stockGraph(i,individual=None):
    i=i  # Choose i = x-2 where x:cell number in sheet 

    Date_wise_Total1 = DataList[i].transpose()
    Date_wise_Total1.name = "mul"
    Date_wise_Total1 = Date_wise_Total1.to_frame()
    Date_wise_Total1=Date_wise_Total1.reset_index()
    Date_wise_Total1
    x = list(Date_wise_Total1.Date)
    text = sheet['COMP_NAME'][i]
    if individual == "yes": 
        y = list(Date_wise_Total1['mul']/dataQuantity[i]) #dividing by its number of quantity
        drawGraph(x,y,"Stock Price of "+text)
    else:
        y = list(Date_wise_Total1['mul'])
        drawGraph(x,y,"Stock's Value of "+text)


# In[58]:


def drawGraph(x,y,text,showInvest = None,GraphFileName=None,compare=None):    
    fig2 = go.Figure()

    fig2.add_trace(
        go.Scatter(x=x, y=y))
        #go.Scatter(x=list(Date_wise_Total1.Date), y=list(Date_wise_Total1.mul)))
        
    if showInvest == 'yes':
        fig2.add_trace(
        go.Scatter(
            x=list(compare.PUR_DATE),
            y=list(compare.Till_now)
        ))
        
        #Here Nifty's portfolio is compared
        fig2.add_trace(
        go.Scatter(
            x=list(compare.PUR_DATE),
            y=list(compare.CURRENT_VALUE)
        ))

    # Set title
    fig2.update_layout(
        title_text=text
    )

    # Add range slider
    fig2.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    
    if showInvest == 'yes':
        names = cycle(['Value', 'Invested','Sensex'])
        fig2.for_each_trace(lambda t:  t.update(name = next(names)))
        
    if GraphFileName:
        fig2.write_image("Users/"+UserName+"/images/"+GraphFileName)
    else:
        fig2.show()


# In[59]:


tom = datetime.date.today() + datetime.timedelta(days=1)
tom=tom.strftime("%Y-%m-%d")


# In[60]:


Nifty_Personalised=pd.DataFrame(columns=['PUR_DATE','Quan'])
Nifty_Personalised['PUR_DATE']=pd.date_range(start=MultipliedInvested.loc[0,'PUR_DATE'],end=tom)
Nifty_Personalised["PUR_DATE"]=Nifty_Personalised["PUR_DATE"].dt.strftime("%Y-%m-%d")
res = pd.merge(Nifty_Personalised, MultipliedInvested,on='PUR_DATE',how='left')
#res=res.drop("Till_now",axis=1)

sensex = pdr.get_data_yahoo("^BSESN",start=sheet.PUR_DATE.min(),end=tom)
sensex=sensex.drop(["Open","High","Low","Adj Close","Volume"],axis=1)
sensex=sensex.reset_index()

sensex["Date"]=sensex["Date"].dt.strftime("%Y-%m-%d")
res1 = pd.merge(res, sensex,left_on='PUR_DATE',right_on='Date',how='left')
res1=res1.drop('Date',axis=1)
res1["CURRENT_VALUE"]=0
oldres=res1

Invested_list = list()
prev=res1['Invested'][0]
for i in res1['Invested']:
    if i>0:
        Invested_list.append(i)
        prev=i
    else:
        Invested_list.append(prev)
oldres['Invested']=Invested_list

tillnow_list=list()
prevtill=res1['Till_now'][0]
for i in res1['Till_now']:
    if i>0:
        tillnow_list.append(i)
        prevtill=i
    else:
        tillnow_list.append(prevtill)
oldres['Till_now']=tillnow_list

sumquan=oldres["Invested"][0]/oldres["Close"][0]
quan_list=list()
quan_list.append(sumquan)
lenlist=len(oldres["Invested"])
print(lenlist)
oldres["Close"]=oldres['Close'].ffill() #ffill fills upper value
for j in range(1,lenlist):
    if oldres["Invested"][j]==oldres["Invested"][j-1]:
        quan_list.append(sumquan)
    else:
        sumquan=sumquan+(oldres["Invested"][j]/oldres["Close"][j])
        quan_list.append(sumquan)
oldres["Quan"]=quan_list

# oldres["Close"]=oldres['Close'].ffill() #ffill fills upper value
oldres['CURRENT_VALUE']=oldres["Quan"]*oldres["Close"]
oldres


# In[63]:


# Main 
tom = datetime.date.today() + datetime.timedelta(days=1)
tom=tom.strftime("%Y-%m-%d")
EndDate = tom
DataList,dataQuantity = PortfolioValue(sheet,EndDate)
PlotPortfolioValues(DataList,GraphFileName,compare=oldres) 


# In[64]:


##### Individual performance of a stock
# StockIndex = int(input("Enter the SR no according to the excel file: ")) -1
# stockGraph(StockIndex,"yes")
# stockGraph(StockIndex)


# In[65]:


# I have replaced pe ratio with nifty50 return% 

#This is to Calculate Current Portfolio PE Ratio by Weighted harmonic mean PE, while ignoring -ves
# Refrence : https://twitter.com/10kdiver/status/1424040654540210181?s=20

# PElist=[]
# for i in range(total_rows):
#     data_demo=yf.Ticker(sheet.COMP_SYMBOL[i])
#     try:
#         pe=data_demo.info["trailingPE"]
#     except:
#         pe=0
#     print(i)
#     PElist.append(pe)


# In[66]:


Latest_value=[]
for i in range(total_rows):
    Latest_value.append(DataList[i][-1])
L_value=Latest_value #This will be used in Pie Chart
# Latest_value=pd.DataFrame(Latest_value)
# PElist=pd.DataFrame(PElist) #PE
# Latest_value = Latest_value/Current_Value #W
# WPE = Latest_value/PElist
# # Replacing infinite with nan
# WPE.replace([np.inf, -np.inf], np.nan, inplace=True)
# # Dropping all the rows with nan values
# WPE.dropna(inplace=True)
# result = 1/WPE.sum() #Value of PE ratio
# result[0] 


# In[67]:


# #Nifty50 return meanwhile we were invested
# nif = pdr.get_data_yahoo("^NSEI",start=sheet.PUR_DATE.min(),end=tom)
# nifdif = (nif.iloc[-1,1]-nif.iloc[0,2])/nif.iloc[0,2]
# nifdif *= 100
# nifdif

#Instead of above comparision, I have used Sip Comparision
nifdif = ((Current_Value-oldres.iloc[-1,5])/oldres.iloc[-1,5])*100
nifdif


# In[68]:


#To know Percentage Change of X Day/s

# Days=int(input("Enter Number of Days X, i.e Difference,Change : Today - X days:= ")) #Enter Number of days you want the Percentage change(mind it this is not days but sessions) 
# Change = Date_wise_Total.iloc[-1,1]-Date_wise_Total.iloc[-1-Days,1]
# DayPercentage=(Change/Date_wise_Total.iloc[-1-Days,1])*100
# DayPercentage,Change


# In[69]:


LC_value=L_value/Current_Value
df_L_value=pd.DataFrame(L_value)
df_L_value["COMP_NAME"] = sheet["COMP_NAME"]

df_L_value["LC_VALUE"] = LC_value
df_L_value


# In[70]:


Labels = []
LC = list(df_L_value["LC_VALUE"])
j=0
for i in LC:
    if i>=0.009:
        Labels.append(df_L_value.iloc[j,1])
    else:
        Labels.append("Others")
    j +=1
df_L_value["Labels"] = pd.DataFrame(Labels)
df_L_value


# In[71]:


df_L_value = df_L_value.groupby(['Labels']).sum()


# In[72]:


figPie = go.Figure(data=[go.Pie(labels=list(df_L_value.index), values=list(df_L_value[0].values))])
figPie.update_layout(
        title_text="Pie Chart of stock's Contribution in PortFolio"
    )
if PieFileName:
    figPie.write_image("Users/"+UserName+"/images/"+PieFileName)
else:
    figPie.show()


# In[73]:


#For Finding Maximum Value ever of the Portfolio
ValueMax = Date_wise_Total.max()["Value"]
DifValueMax = Current_Value - ValueMax
DifMaxDate = Date_wise_Total.iloc[Date_wise_Total["Value"].argmax(),0]
DifMaxPer = (DifValueMax/ValueMax)*100
#For gains
Gain = Current_Value - MultipliedInvested.iloc[-1,-1]
GainPer = (Gain/MultipliedInvested.iloc[-1,-1])*100

DayChange = Date_wise_Total.iloc[-1,1]-Date_wise_Total.iloc[-1-1,1]
DayChangePer=(DayChange/Date_wise_Total.iloc[-1-1,1])*100

new_line = '\n'
# rupee =u'\u20B9'
#summary = f"==> Summary{new_line}{new_line}Current Value Of the Portfolio is : Rs. {Current_Value: .2f}{new_line}Today's gain : ₹{DayChange: .2f}{new_line}Percentage Change : {DayChangePer:.2f}%{new_line}{new_line}Total invested : ₹{MultipliedInvested.iloc[-1,-1]}{new_line}Total Gain : ₹{Gain: .2f}{new_line}Percentage Gain : {GainPer: .2f}%{new_line}{new_line}P/E Ratio of the Portfolio : {result[0]:.2f}{new_line}{new_line}Maximum Value of Your Portfolio achieved : ₹ {ValueMax:.2f}{new_line}On This Date : {DifMaxDate:%B %d, %Y}{new_line}{new_line}Amount decreased by : ₹ {DifValueMax: .2f}{new_line}Percentage Change : {DifMaxPer: .2f} %".replace("₹","Rs.")
#summary = "==> Summary\n\nCurrent Value Of the Portfolio is : Rs.{0: .2f}\nToday's gain : Rs. {1: .2f}\nPercentage Change : {2:.2f}%\n\nTotal invested : Rs. {3}\nTotal Gain : Rs.{4: .2f}\nPercentage Gain : {5: .2f}%\n\nP/E Ratio of the Portfolio : {6:.2f}\n\nMaximum Value of Your Portfolio achieved : Rs. {7:.2f}\nOn This Date : {8:%B %d %Y}\n\nAmount decreased by : Rs. {9: .2f}\nPercentage Change : {10: .2f} %".format(Current_Value,DayChange,DayChangePer,MultipliedInvested.iloc[-1,-1],Gain,GainPer,result[0],ValueMax,DifMaxDate,DifValueMax,DifMaxPer)
#print(summary)


# In[74]:


# Python program to convert text file to PDF using FPDF

from fpdf import FPDF 
WIDTH = 297 #for landscape
HEIGHT = 210

pdf = FPDF('L')  #Defaut is A4 210*297 mm


pdf.add_page() 

#Template Pdf
pdf.image("./AppResources/MyPortfolioApp.png", x = 0, y = 0, w = WIDTH, h = HEIGHT)

pdf.set_font("Arial", size = 12) 
pdf.set_text_color(255,255,255)
# pdf.ln(70)
pdf.text(8, 47, "Portfolio Value")

pdf.set_font("Arial", size = 14)
pdf.text(7,55,f"Rs.{Current_Value: ,.0f}")

pdf.set_text_color(0,0,0)

pdf.set_font("Arial", size = 12) 
pdf.text(58, 47, "Total Invested")
todaydate=datetime.date.today()
pdf.text(240, 31, f"{todaydate: %B %d, %Y}")

pdf.set_font("Arial", size = 14)
pdf.text(57,55,f"Rs.{MultipliedInvested.iloc[-1,-1]: ,.0f}")

pdf.set_font("Arial", size = 12) 
pdf.text(110, 47, "Unrealized Gain")
pdf.text(109,60,f"({GainPer: ,.2f} %)")

pdf.set_font("Arial", size = 14)
pdf.text(109,54,f"Rs.{Gain: ,.0f}")

pdf.set_font("Arial", size = 10) 
pdf.text(161, 47, "Outperformed Sensex, By")

pdf.set_font("Arial", size = 14)
pdf.text(163,55,f"{nifdif: ,.2f}%")

if nifdif>=0:
    pdf.set_text_color(0,255,0)
    pdf.set_font("Arial", size = 14)
    pdf.text(163,55,f"{nifdif: ,.2f}%")
else:
    pdf.set_text_color(255,0,0)
    pdf.set_font("Arial", size = 14)
    pdf.text(163,55,f"{nifdif: ,.2f}%")

# if nifdif>=0:
#     outperform = "Portfolio Outperformed"
#     pdf.set_text_color(0,255,0)
#     pdf.set_font("Arial", size = 10)
#     pdf.text(163,60,f"{outperform}")
# else:
#     outperform = "Sensex Outperformed"
#     pdf.set_text_color(255,0,0)
#     pdf.set_font("Arial", size = 10)
#     pdf.text(163,60,f"{outperform}")

# pdf.set_text_color(0,255,0)

# pdf.set_font("Arial", size = 10)
# pdf.text(163,60,f"{outperform}")

pdf.set_text_color(0,0,0)

pdf.set_font("Arial", size = 12) 
pdf.text(221, 47, "Today's Gain")
pdf.text(220,60,f"({DayChangePer:,.2f}%)")

pdf.set_font("Arial", size = 14)
pdf.text(220,54,f"Rs.{DayChange: ,.0f}")

pdf.image("Users/"+UserName+"/images/"+GraphFileName, x = 2, y = 65, w = WIDTH-10, h = HEIGHT-65)

pdf.add_page()
pdf.image("Users/"+UserName+"/images/"+PieFileName, x = 0, y = 0, w = WIDTH, h = HEIGHT)
# f = open("tss.txt", "r") 

# for x in f: 
#     #text=x.encode('latin-1', 'ignore').decode('latin-1')
#     pdf.cell(200, 10, txt = x, ln = 1, align = 'C') 

# pdf.add_page()



# pdf.add_page()
# pdf.set_text_color(0,200,0)
# pdf.cell(200,10,txt="Hell",ln=1,align='C')
# pdf.add_page()
# pdf.set_text_color(0,0,0)
# pdf.cell(200,10,txt="Hell",ln=1,align='C')
# pdf.footer()
pdf.output("Users/"+UserName+"/resources/"+PdfFileName)

