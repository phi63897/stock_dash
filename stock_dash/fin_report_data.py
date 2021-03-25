import pandas as pd
import requests
from datetime import date
import os

def get_financial_report(ticker):
    iex_token = os.getenv('iex_token')
    base_url = "https://cloud.iexapis.com/"

    balanceRequest = "stable/stock/{ticker}/balance-sheet?period=annual&last=5&token={token}".format(ticker=ticker, token = iex_token)
    balanceSheet = requests.get(base_url + balanceRequest).json()["balancesheet"]

    cashRequest = "stable/stock{ticker}/cash-flow?period=annual&last=5&token={token}".format(ticker=ticker, token = iex_token)
    # cashFlowRes = (requests.get(base_url + cashRequest)).json()["cashflow"]

    incomeRequest = "stable/stock/{ticker}/income?period=annual&last=5&token={token}".format(ticker=ticker, token = iex_token)
    incomeStatement = requests.get(base_url+incomeRequest).json()["income"]

    eps=["-"]
    epsGrowth = ["-"]
    totalasset = [year["totalAssets"] for year in balanceSheet]
    totalasset.reverse()
    netIncome = [year["netIncome"] for year in incomeStatement]
    netIncome.reverse()
    longtermDebt = [year["longTermDebt"] for year in balanceSheet]
    longtermDebt.reverse()
    interestIncome = [year["interestIncome"] for year in incomeStatement]
    interestIncome.reverse()
    ebit= [year["ebit"] for year in incomeStatement]
    ebit.reverse()
    shareholderEquity = [year["shareholderEquity"] for year in balanceSheet]
    shareholderEquity.reverse()
    roa = [netIncome[i]/totalasset[i] for i in range(len(totalasset))]



    # load all the data into dataframe
    fin_df= pd.DataFrame({'eps': eps,'eps Growth': epsGrowth,'net Income': netIncome,'shareholder Equity': shareholderEquity,'roa':
                  roa,'longterm Debt': longtermDebt,'interest income': interestIncome,'ebit': ebit},index=range(date.today().year-5,date.today().year))

    fin_df.reset_index(inplace=True)

    return fin_df
