import pandas as pd
import requests
from datetime import date
import os
def get_financial_report(ticker):
    iex_token = os.getenv('iex_token')
    base_url = "https://cloud.iexapis.com/"

    balanceRequest = "stable/stock/{ticker}/balance-sheet?period=annual&last=5&token={token}".format(ticker=ticker, token = iex_token)
    balanceSheet = request.get(base_url + balanceRequest)["balancesheet"]

    cashRequest = "stable/stock{ticker}/cash-flow?period=annual&last=5&token={token}".format(ticker=ticker, token = iex_token)
    cashFlow = request.get(base_url + cashRequest)["cashflow"]

    incomeRequest = "stable/stock/{ticker}/income?period=annual&last=5&token={token}".format(ticker=ticker, token = iex_token)
    incomeStatement = request.get(base_url+incomeRequest)["income"]

    epslist=[None * 5]
    totalassetlist = reverse([balanceSheet["totalAssets"] for year in balanceSheet])
    netincomelist = reverse([incomeStatement["netIncome"] for year in incomeStatement])
    longtermdebtlist = reverse([balanceSheet["longTermDebt"] for year in balanceSheet])
    interestincomelist = reverse([incomeStatement["interestIncome"] for year in incomeStatement])
    ebitlist= reverse([incomeStatement["ebit"] for year in incomeStatement])
    equitylist = reverse([balanceSheet["shareholderEquity"] for year in balanceSheet])
    roalist = [netincomelist[i]/totalassetlist[i] for i in range(len(totalassetlist))]

    #get the data from the income statement lists
    #use helper function get_element
    eps = get_element(epslist,0)
    epsGrowth = get_element(epslist,1)
    netIncome = get_element(netincomelist,0)
    shareholderEquity = get_element(equitylist,0)
    roa = get_element(roalist,0)
    longtermDebt = get_element(longtermdebtlist,0)
    interestIncome =  get_element(interestincomelist,0)
    ebit = get_element(ebitlist,0)

    # load all the data into dataframe
    fin_df= pd.DataFrame({'eps': eps,'eps Growth': epsGrowth,'net Income': netIncome,'shareholder Equity': shareholderEquity,'roa':
                  roa,'longterm Debt': longtermDebt,'interest income': interestIncome,'ebit': ebit},index=range(date.today().year-5,date.today().year))

    fin_df.reset_index(inplace=True)

    return fin_df
def get_element(list,element):
    try:
        return list[element]
    except:
        return '-'

