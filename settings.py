import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

def load_data(path_dir = 'data/'):
    data_files = os.listdir(path_dir)
    if not data_files:
        st.error("Tidak ada file data yang ditemukan di direktori.")
        st.stop()
    else:
        file_path = os.path.join(path_dir, data_files[0])
        df = pd.read_csv(file_path)
        #df['Tanggal'] = pd.to_datetime(df['Tanggal'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
        return df

def filter_data(df, start_date, end_date):
    # Konversi kolom Tanggal ke tipe data datetime.date jika belum
    if df['Tanggal'].dtype == 'datetime64[ns]':
        df['Tanggal'] = df['Tanggal'].dt.date
    
    # Filter dataframe berdasarkan rentang tanggal
    filtered_df = df.loc[(df['Tanggal'] >= start_date) & (df['Tanggal'] <= end_date)]
    
    return filtered_df
    