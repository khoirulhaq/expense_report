# pages/tambah_data.py

import streamlit as st
import pandas as pd
from datetime import datetime
import settings
import os


def tambah_data(df):
    st.header('Tambah Data Pengeluaran')

    with st.form(key='add_expense_form'):
        new_nominal = st.number_input("Nominal:", value=0)
        new_date = st.date_input("Tanggal:", value=datetime.today())
        new_wallet = st.selectbox("Dompet:", ["Cash", "OVO", "BJB", "Livin", "ShopeePay", "Lainnya"])
        

        categories = [
            "Makanan/Minuman",
            "Komunikasi",
            "Transportasi",
            "Pendidikan/Ilmu",
            "Hiburan",
            "Kesehatan",
            "Kebersihan",
            "Belanja",
            "Darurat",
            "Tempat tinggal",
            "Produktivitas",
            "Lainnya"
        ]

        new_category = st.selectbox("Kategori:", categories)

        new_note = st.text_input("Catatan:")
        new_priority = st.selectbox("Prioritas:", ["Harus", "Butuh","Ingin"])

        submit_button = st.form_submit_button(label='Tambah Data')

    if submit_button:
        new_data = {'Nominal': new_nominal, 'Tanggal': new_date, 'Dompet': new_wallet,
                    'Kategori': new_category, 'Catatan': new_note, 'Prioritas': new_priority}
        df = df.append(new_data, ignore_index=True)
        #df['Tanggal'] = pd.to_datetime(df['Tanggal'], format='%d/%m/%Y')
        
        st.success("Data berhasil ditambahkan.")
    
    return df

def hapus_data(df):
    st.header('Hapus Data Pengeluaran')

    remove_index = st.number_input("Masukkan indeks data yang ingin dihapus:", min_value=0, max_value=len(df)-1, step=1)
    remove_button = st.button("Hapus Data")

    if remove_button:
        if 0 <= remove_index < len(df):
            df = df.drop(remove_index)
            st.success("Data berhasil dihapus.")
        else:
            st.error("Indeks data tidak valid.")
            
    
    
    return df

df = settings.load_data()
df = tambah_data(df)
df = hapus_data(df)

# Tampilkan dataset terakhir berdasarkan tanggal
st.header('Dataset Terakhir Berdasarkan Tanggal')
#df_latest = df.sort_values(by='Tanggal', ascending=False).head(5)
path_dir = 'data/'
data_files = os.listdir(path_dir)
file_path = os.path.join(path_dir, data_files[0])
#df.reset_index(drop=True, inplace=True)
df['Tanggal'] = pd.to_datetime(df['Tanggal']).dt.date
df = df.sort_values(by='Tanggal', ascending=True)
df.to_csv(file_path, index=False)
st.write(df.reset_index(drop=True).tail(10))
