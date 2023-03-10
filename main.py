import streamlit as st
import pandas as pd
import numpy as np
from bcb import sgs,currency
from datetime import date

def absolute(serie):
    valor_atual = 915.9300
    yield valor_atual
    for valor in serie[:-1]:
        valor = valor / 100
        valor_atual += (valor_atual * valor)
        yield valor_atual

def fetch_main_data():
    data = {'Inflação':433,'PIB':22109,'Emprego Formal':28763,'SELIC':432}
    for key in data:
        if key not in st.session_state:
            df = sgs.get({key:data[key]},start = '1994-08-01').dropna()
            st.session_state[key] = df
    if 'Inflação' in st.session_state:
        st.session_state['Inflação']['Inflação'] = ((((1 + (st.session_state['Inflação']['Inflação'] / 100)) ** 12) - 1) * 100).apply(lambda x: round(x,2))

    if 'USD' not in st.session_state:
        cy = currency.get('USD', start = '1994-08-01',end = str(date.today())).dropna()
        st.session_state['USD'] = cy

def enrich_data():
    if 'Inflação Acumulada' not in st.session_state:
        df = st.session_state['Inflação'].copy()
        df['Inflação Acumulada'] = [valor for valor in absolute(df['Inflação'].values)]
        st.session_state['Inflação Acumulada'] = df[['Inflação Acumulada']].copy()

def main_window():
    data = {'Inflação':'inverse','PIB':'normal','SELIC':'inverse','USD':'inverse','Emprego Formal':'normal'}
    cols = st.columns(len(data))
    for name,col in zip(data.keys(),cols):
        df = st.session_state[name]
        last_value = df[name].iloc[-1]
        before = df[name].iloc[-2]
        dif_percent = round(100 * (last_value - before) / before,2)
        col.metric(name,last_value,str(dif_percent) + '%',data[name])

fetch_main_data()

st.set_page_config(page_title = 'Economia Brasileira',layout = 'wide',page_icon = '&#128200')
style = '''
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
.block-container {padding-top:1rem;}
.e1fqkh3o4 {padding-top:1rem;}
</style>
'''
st.markdown(style,unsafe_allow_html=True)

main_window()
st.title('Economia Brasileira')