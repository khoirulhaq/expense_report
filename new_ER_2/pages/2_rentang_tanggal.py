import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import settings


df = settings.load_data()
df['Tanggal'] = pd.to_datetime(df['Tanggal'])

start_date = st.sidebar.date_input("Start date", datetime.now().replace(day=1))
end_date = st.sidebar.date_input("End date", datetime.now())
st.header('Riwayat Pengeluaran')
filtered_df = settings.filter_data(df, start_date, end_date)
st.write(filtered_df.sort_values(by='Tanggal', ascending=False))

day_total_expenses = filtered_df.groupby('Tanggal')['Nominal'].sum().reset_index()
day_title = 'Total Pengeluaran Harian'

#st.write(day_total_expenses)
day_total_expenses.columns = ['Tanggal', 'Total Pengeluaran']
day_fig = px.line(day_total_expenses, x='Tanggal', y='Total Pengeluaran', title=day_title)
st.plotly_chart(day_fig)

st.header('Kategori')
filt_cat = filtered_df.groupby('Kategori')['Nominal'].sum().reset_index()
fig_cat = px.pie(filt_cat, values='Nominal', names='Kategori', title='Pengeluaran Berdasarkan Kategori')
st.plotly_chart(fig_cat)

st.header('Dompet')
filt_dom = filtered_df.groupby('Dompet')['Nominal'].sum().reset_index()
fig_dom  = px.pie(filt_dom, values='Nominal', names='Dompet', title='Pengeluaran Berdasarkan Dompet')
st.plotly_chart(fig_dom)

st.header('Pencarian Berdasarkan Catatan')

# Input field for user to enter the note to search for
note_to_search = st.text_input("Masukkan catatan yang ingin Anda cari:")

# Input field for user to enter the number of rows to display

# Filter data based on the note entered by the user
if note_to_search:
    note_to_search = note_to_search.lower()  # Convert the search term to lowercase
    filtered_df = filtered_df[filtered_df['Catatan'].str.lower().str.contains(note_to_search, na=False)]  # Use str.contains() for partial matches and case-insensitive search
    
    total_expenses = filtered_df['Nominal'].sum()
    st.write(f"Total pengeluaran untuk catatan yang mengandung '{note_to_search}': Rp {total_expenses:,}")
    # Display the number of rows found
    num_rows_to_display = st.number_input("Masukkan jumlah baris yang ingin ditampilkan:", min_value=1, max_value=len(df), value=3)
    num_rows_found = len(filtered_df)
    st.write(f"Jumlah baris yang ditemukan: {num_rows_found}")
    # Display the specified number of rows from the filtered DataFrame
    st.write(f"{num_rows_to_display} baris pertama dari hasil pencarian:")
    #filtered_df['Tanggal'] = filtered_df['Tanggal'].dt.date
    st.write(filtered_df.head(num_rows_to_display).iloc[:, :-1])







