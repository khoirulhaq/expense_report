import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import settings


st.set_page_config(
    page_title="Expense Report",
    page_icon="💲",
)

st.title("Pengeluaran Keseluruhan")
#st.sidebar.success("Select a page above.")


#st.header('Pengeluaran per Bulan')
df = settings.load_data()
df['Tanggal'] = pd.to_datetime(df['Tanggal'])
df['Tahun-Bulan'] = df['Tanggal'].dt.strftime('%Y-%m')
df_new = df.groupby(df['Tahun-Bulan'])['Nominal'].sum().reset_index()
df_new['Tahun-Bulan'] = pd.to_datetime(df_new['Tahun-Bulan'], format='%Y-%m')
df_new['Bulan'] = df_new['Tahun-Bulan'].dt.month
df_new['Tahun'] = df_new['Tahun-Bulan'].dt.year
nama_bulan = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 
            7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

df_new['Bulan_nama'] = df_new['Bulan'].map(nama_bulan)
df_new['Bulan_Tahun_nama'] = df_new['Bulan_nama'] + ' ' + df_new['Tahun'].astype(str)

df_month = df_new.copy()
fig_bar = px.bar(df_month, x='Bulan_Tahun_nama', y='Nominal', labels={'Nominal': 'Total Pengeluaran', 'Bulan_Tahun_nama': 'Bulan'}, title='Total Pengeluaran per Bulan')
st.plotly_chart(fig_bar)
# =======================
df_day = df.groupby(pd.Grouper(key='Tanggal', freq='D'))['Nominal'].sum().reset_index()
fig_line = px.line(df_day, x='Tanggal', y='Nominal', labels={'Nominal': 'Total Pengeluaran', 'Tanggal': 'Bulan'})
st.plotly_chart(fig_line)

st.header('Kategori')
filt_cat = df.groupby('Kategori')['Nominal'].sum().reset_index()
fig_cat = px.pie(filt_cat, values='Nominal', names='Kategori', title='Pengeluaran Berdasarkan Kategori')
st.plotly_chart(fig_cat)


st.header('Dompet')
filt_dom = df.groupby('Dompet')['Nominal'].sum().reset_index()
fig_dom  = px.pie(filt_dom, values='Nominal', names='Dompet', title='Pengeluaran Berdasarkan Dompet')
st.plotly_chart(fig_dom)

# New feature: Display expenses by note
st.header('Pencarian Berdasarkan Catatan')

# Input field for user to enter the note to search for
note_to_search = st.text_input("Masukkan catatan yang ingin Anda cari:")

# Input field for user to enter the number of rows to display

# Filter data based on the note entered by the user
if note_to_search:
    note_to_search = note_to_search.lower()  # Convert the search term to lowercase
    filtered_df = df[df['Catatan'].str.lower().str.contains(note_to_search, na=False)]  # Use str.contains() for partial matches and case-insensitive search
    
    total_expenses = filtered_df['Nominal'].sum()
    st.write(f"Total pengeluaran untuk catatan yang mengandung '{note_to_search}': Rp {total_expenses:,}")
    # Display the number of rows found
    num_rows_to_display = st.number_input("Masukkan jumlah baris yang ingin ditampilkan:", min_value=1, max_value=len(df), value=3)
    num_rows_found = len(filtered_df)
    st.write(f"Jumlah baris yang ditemukan: {num_rows_found}")
    # Display the specified number of rows from the filtered DataFrame
    st.write(f"{num_rows_to_display} baris pertama dari hasil pencarian:")
    filtered_df['Tanggal'] = filtered_df['Tanggal'].dt.date
    st.write(filtered_df.head(num_rows_to_display).iloc[:, :-1])








    