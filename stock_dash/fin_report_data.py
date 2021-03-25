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

    eps=["-" * 5]
    epsGrowth = ["-" * 5]
    totalasset = reverse([year["totalAssets"] for year in balanceSheet])
    netIncome = reverse([year["netIncome"] for year in incomeStatement])
    longtermDebt = reverse([year["longTermDebt"] for year in balanceSheet])
    interestIncome = reverse([year["interestIncome"] for year in incomeStatement])
    ebit= reverse([year["ebit"] for year in incomeStatement])
    shareholderEquity = reverse([year["shareholderEquity"] for year in balanceSheet])
    roa = [netIncome[i]/totalasset[i] for i in range(len(totalasset))]


    # load all the data into dataframe
    fin_df= pd.DataFrame({'eps': eps,'eps Growth': epsGrowth,'net Income': netIncome,'shareholder Equity': shareholderEquity,'roa':
                  roa,'longterm Debt': longtermDebt,'interest income': interestIncome,'ebit': ebit},index=range(date.today().year-5,date.today().year))

    fin_df.reset_index(inplace=True)

    return fin_df


