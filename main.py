import streamlit as st
import pandas as pd
import numpy as np
from bcb import sgs
import plotly.graph_objects as go

def fetch_main_data():
    data = {'Inflação':433}
    df = sgs.get(data,start = '1994-08-01')
    return df

df = fetch_main_data()

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

st.title('Inflação')
st.line_chart(df)