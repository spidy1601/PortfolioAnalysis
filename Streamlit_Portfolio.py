from ast import Global
import yfinance as yf #This is an API which fetch real time financial data 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go #For Graphical representation
from itertools import cycle
from pandas_datareader import data as pdr
import datetime
import streamlit as st

import time

yf.pdr_override()


st.set_page_config(page_title="Portfolio Analysis", page_icon="AppResources/ICON.png", layout="wide", initial_sidebar_state="auto", menu_items=None)


st.header("PORTFOLIO ANALYSIS")
st.write("Made with ❤️ by *Devarsh Shah*")
with open('style.css') as fa:
    st.markdown(f'<style>{fa.read()}</style>',unsafe_allow_html=True)

st.info("It is software that aggregates real-time data and delivers comprehensive analysis on a basic dashboard interface.")
tab1, tab2, tab3, tab4= st.tabs(["🗃 Stocks' Data","📈 DashBoard","📑Tutorial", "🙂About Developer"])

tab1.subheader("My Stocks")
tab3.subheader("Why and How to Use?")
tab3.markdown("##### [Why]<br>If your answer is YES to any of the below questions, then you must try this FREE website(Your data is secured and we don’t have access to it, so feel free to use it!)<br><ul><li>Want to see your Portfolio’s value on Particular date?</li><li>Want to compare Sensex and your Portfolio’s return(i.e if you had invested in the Index fund instead of your Portfolio)?</li><li>Want to know The highest Value your Portfolio had achieved?</li><li>Want to see the pattern of Portfolio’s value vs Time Period?</li></ul>",unsafe_allow_html=True)
tab3.write("##### [How?]")
tab3.video("https://youtu.be/cnDjfSu64bg")

tab4.write("Consider [buying me a coffee](https://www.buymeacoffee.com/devarsh) if you feel somewhat motivated or impressed.")
tab4.write("Let's Connect On [LinkedIn](https://www.linkedin.com/in/devarsh-shah-256115194/)!")
tab4.image("AppResources/Devarsh.jpg",width=300)
tab4.write("Hello friend, I am Devarsh Shah, the creator of this WEBAPP. I'm in my final year of a computer engineering degree and doing side projects out of curiosity. Also, I am looking for a good internship (ping me on my linkedin).")

with open("AppResources/Demo_Excel_File.xlsx","rb") as file:
    btn = tab1.download_button(
            label="Demo_Excel_File.xlsx",
            data=file,
            file_name="Demo_Excel_File.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

tab2.subheader("🖥️My Dashboard")


# UserName = input("Enter UserName (i.e Your Name): ")
# if not os.path.exists("Users"):
#     os.mkdir("Users")
# if not os.path.exists("Users/"+UserName):
#     os.mkdir("Users/"+UserName)
# if not os.path.exists("Users/"+UserName+"/images"):
#     os.mkdir("Users/"+UserName +"/images")
# if not os.path.exists("Users/"+UserName+"/resources"):
#     os.mkdir("Users/"+UserName+"/resources")
sheet_file = tab1.file_uploader("Upload your excel file : (Download the 'Demo_Excel_File.xlsx' given above then update it and upload that file in below dropbox)",accept_multiple_files=False)

if not sheet_file:
    default_sheet="Users/Spidyy/resources/Spidyy_data.xlsx"
    tab2.success("This is the demo portfolio.")
    sheet = pd.read_excel(default_sheet)
else:
    try:
        sheet = pd.read_excel(sheet_file)
    except:
        st.error("Please upload the file in excel format")
        st.stop()
    tab1.success("Your Dashboard is loading in the 'Dashboard' section.")
 
tab1.table(sheet)
#StockIndex = int(input("Enter the SR no according to the excel file for individual Stocks: ")) -1
# GraphFileName = UserName+"Graph.png"
# #Days=int(input("Enter Number of Days X, i.e Difference,Change : Today - X days:= ")) #Enter Number of days you want the Percentage change(mind it this is not days but sessions) 
# PieFileName = UserName+"Pie.png"
# PdfFileName = UserName+"_PortFolio.pdf"


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
#MultipliedInvested.plot(x='PUR_DATE',y='Till_now')
#for inserting today's date data 
tod= datetime.date.today()
tod=tod.strftime("%Y-%m-%d")
MultipliedInvested.loc[len(MultipliedInvested.index)] = [tod,0,MultipliedInvested.iloc[-1,-1] ]
#MultipliedInvested



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
    global fig2
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
    
    fig2.update_layout(height=750) 
        
    # if GraphFileName:
    #     fig2.write_image("Users/"+UserName+"/images/"+GraphFileName)
    # else:
        # fig2.show()
    #tab2.plotly_chart(fig2)



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
#print(lenlist)
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
#oldres


# In[63]:


# Main 
tom = datetime.date.today() + datetime.timedelta(days=1)
tom=tom.strftime("%Y-%m-%d")
EndDate = tom
try:
    DataList,dataQuantity = PortfolioValue(sheet,EndDate)
except:
    st.error("Make sure all your Entered details are correct.")
    st.stop()
PlotPortfolioValues(DataList,GraphFileName=None,compare=oldres) 

nifdifvalue = Current_Value-oldres.iloc[-1,5]
nifdif = ((Current_Value-oldres.iloc[-1,5])/oldres.iloc[-1,5])*100

#For Finding Maximum Value ever of the Portfolio
ValueMax = Date_wise_Total.max()["Value"]
DifValueMax = Current_Value - ValueMax
DifMaxDate = Date_wise_Total.iloc[Date_wise_Total["Value"].argmax(),0]
DifMaxPer = (DifValueMax/ValueMax)*100
#For gains
Gain = Current_Value - MultipliedInvested.iloc[-1,-1]
GainPer = (Gain/MultipliedInvested.iloc[-1,-1])*100

PortMax=max(list(Date_wise_Total.Value))
PortMaxPer = ((Current_Value-PortMax)/PortMax) * 100

col1, col2, col3, col4 = tab2.columns(4)
col1.metric("Total Value", f"Rs.{Current_Value: ,.0f}", f"{GainPer: ,.2f}% 💸")
col2.metric("Total Invested", f"Rs.{MultipliedInvested.iloc[-1,-1]: ,.0f}","💰")
col3.metric("Outperform Sensex by",f"Rs.{nifdifvalue: ,.0f}",delta=f"{nifdif: ,.2f}% 😎")
col4.metric("The Peak", f"Rs.{PortMax: ,.0f}",delta=f"{PortMaxPer: ,.2f}% 🥲")

peak_string = f"Your Portfolio had achieved All Time high of Rs. {PortMax: ,.0f} but now it's down by {PortMaxPer: ,.2f}% 🥲"

if GainPer>0 and nifdif>0: 
    with tab2.expander("Your Portfolio Analysis"):
        st.write(f"Your Portfolio is Profitable! i.e. Rs. {Gain: ,.0f} in profit💸")
        st.write(f"You would have Rs. {nifdifvalue:,.0f} less, if you had Invested this amount in same periodic manner in Indian Benchmark(Sensex) 😇")
        st.write(peak_string)
elif GainPer>0 and nifdif<0:
    with tab2.expander("Your Portfolio Analysis"):
        st.write(f"Your Portfolio is Profitable! i.e. Rs. {Gain: ,.0f} in profit💸")
        st.write(f"You would have Rs. {abs(nifdifvalue):,.0f} more, if you had Invested this amount in same periodic manner in Indian Benchmark(Sensex) 🥲")
        st.write(peak_string)
elif GainPer<0 and nifdif<0:
    with tab2.expander("Your Portfolio Analysis"):
        st.write(f"Your Portfolio is not Profitable! i.e. Rs. {abs(Gain): ,.0f} in loss💸")
        st.write(f"You would have Rs. {abs(nifdifvalue):,.0f} more, if you had Invested this amount in same periodic manner in Indian Benchmark(Sensex) 🥲")
        st.write(peak_string)
else:
    with tab2.expander("Your Portfolio Analysis"):
        st.write(f"Your Portfolio is not Profitable! i.e. Rs. {abs(Gain): ,.0f} in loss💸")
        st.write(f"You would have Rs. {abs(nifdifvalue):,.0f} less,if you had Invested the same amount in the same periodic manner in Indian Benchmark(Sensex) 😇")
        st.write(peak_string)

tab2.plotly_chart(fig2,use_container_width=True)

