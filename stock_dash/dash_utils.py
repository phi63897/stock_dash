import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table 
from dash.exceptions import PreventUpdate

import flask
from flask import Flask
import pandas as pd
import dateutil.relativedelta
from datetime import date
import datetime
import yfinance as yf
import numpy as np
import praw
import sqlite3

import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def ticker_inputs(inputID, pickerID, MONTH_CUTTOFF):
    #calculate the current date
    currentDate = date.today()
    #calculate past date for the max allowed date
    pastDate = currentDate -     dateutil.relativedelta.relativedelta(months=MONTH_CUTTOFF)
    
    #return the layout components
    return html.Div([
            dcc.Input(id = inputID, type="text", placeholder="MSFT")
            , html.P(" ")  
            , dcc.DatePickerRange(
            id = pickerID,
            min_date_allowed=pastDate,
            start_date = pastDate,
            #end_date = currentDate
            )])

def make_card(alert_message, color, cardbody, style_dict = None):
    
    return  dbc.Card([  dbc.Alert(alert_message, color=color)
        ,dbc.CardBody(cardbody)
        ], style = style_dict)

def make_item(button, cardbody, i):
    # This function makes the accordion items 
    return dbc.Card([
        dbc.CardHeader(
            html.H2(
                dbc.Button(
                    button,
                    color="link",
                    id=f"group-{i}-toggle"))),
        dbc.Collapse(
            dbc.CardBody(cardbody),
            id=f"collapse-{i}")])

def make_table(id, dataframe, lineHeight = '17px', page_size = 5):
    return   dash_table.DataTable(
        id=id,
        css=[{
            'selector': '.row', 
            'rule': '''
                line-height: 17px;
                max-height: 34px; min-height: 34px; height: 34px;
                display: block;
                overflow-y: hidden;
                margin: 0;
            '''
        }],
        columns=[
            {"name": i, "id": i, "presentation"='markdown'} for i in dataframe.columns
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'},
            style_cell={'textAlign': 'left'},
            style_data={
                'whiteSpace': 'normal',
            },
        style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ],
        style_cell_conditional=[
            {'if': {'column_id': 'title'},
            'width': '130px'},
            {'if': {'column_id': 'post'},
            'width': '500px'},
            {'if': {'column_id': 'datetime'},
            'width': '130px'},
            {'if': {'column_id': 'url'},
            'width': '500px'},
            {'if': {'column_id': 'text'},
            'width': '500px'}],
        page_current=0,
        page_size=page_size,
        page_action='custom',
filter_action='custom',
        filter_query='',
sort_action='custom',
        sort_mode='multi',
        sort_by=[]
        )#end table
