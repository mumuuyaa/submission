import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import io  

st.title("Mumu's Bike🚴")
st.subheader("by: Mudia Rahmah")

day_data = pd.read_csv("dashboard/day_data.csv")
hour_data = pd.read_csv("dashboard/hour_data.csv")

st.subheader("Data Harian")
st.markdown("""**Data yang sudah dibersinkan (day_data.csv)**""")
st.dataframe(day_data)

st.subheader("Data Jam")
st.markdown("""**Data yang sudah dibersinkan (hour_data.csv)**""")
st.dataframe(hour_data)




st.subheader("Exploratory Data Analysis (EDA)")
st.markdown("""**Explore day_data.csv**""")

df = pd.DataFrame(day_data)

bike_rental_data = day_data[['dteday', 'cnt']]
bike_rental_data = bike_rental_data.rename(columns={
    'dteday': 'Tanggal Sewa',
    'cnt': 'Jumlah Sewa Harian'
})

st.markdown("""**Data Sewa Sepeda Harian**""")

st.dataframe(bike_rental_data)



st.markdown("""**Explore hour_data.csv**""")

df = pd.DataFrame(hour_data)

bike_rental_data = hour_data[['dteday', 'hr']]
bike_rental_data = bike_rental_data.rename(columns={
    'dteday': 'Tanggal Sewa',
    'hr': 'Waktu Penyewaan'
})

st.markdown("""**Data Sewa Sepeda Per Jam**""")

st.dataframe(bike_rental_data)

st.markdown("""**Insight:**""")
st.markdown("""
* Terdapat fluktuasi yang cukup signifikan pada jumlah penyewaan sepeda setiap harinya, yang kemungkinan dipengaruhi oleh faktor-faktor seperti cuaca atau hari libur dan sebagainya.
* Semakin tinggi suhu, cenderung semakin banyak orang yang menyewa sepeda.
* Kelembaban yang tinggi mungkin sedikit mengurangi minat masyarakat untuk bersepeda.
* Kecepatan angin yang terlalu tinggi dapat mengurangi kenyamanan bersepeda dan berpotensi menurunkan jumlah penyewaan.
""")



st.subheader("Visualization & Explanatory Analysis")

st.subheader("Pertanyaan 1: Apakah ada perbedaan dalam sewa sepeda antara hari libur dan hari biasa?")

df = pd.DataFrame(day_data)

try:
    avg_rental_holiday = day_data.groupby('holiday')['cnt'].mean()
    avg_rental_weekday = day_data.groupby('weekday')['cnt'].mean()
except KeyError:
    st.error("Kolom 'holiday' atau 'weekday' tidak ditemukan. Periksa nama kolom atau data Anda.")
else:
    # -- Streamlit App --

    st.markdown("""**Perbandingan Sewa Sepeda antara Holiday dan Weekday**""")

    
    combined_data = pd.concat([avg_rental_holiday, avg_rental_weekday], axis=1).reset_index()
    combined_data.columns = ['Hari', 'Holiday', 'Weekday']

   
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(combined_data['Hari'], combined_data['Holiday'], label='Holiday', color='skyblue')
    ax.bar(combined_data['Hari'], combined_data['Weekday'], label='Weekday', color='lightgreen')
    ax.set_xlabel('Hari')
    ax.set_ylabel('Rata-rata Sewa Sepeda')
    ax.set_title('Perbandingan Sewa Sepeda antara Holiday dan Weekday')
    ax.legend()

    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    st.image(buf.getvalue(), width=700)

    
    plt.close()

    
    st.markdown("""**Data Rata-rata Sewa Sepeda**""")
    st.dataframe(combined_data)

st.markdown("""**Insight diagram Perbandingan Sewa Sepeda antara Holiday dan Weekday:**""")
st.markdown("""
* Grafik batang menunjukkan adanya perbedaan yang cukup signifikan antara rata-rata penyewaan sepeda pada hari libur dan hari biasa.
* Rata-rata penyewaan sepeda pada hari libur cenderung lebih sedikit dibandingkan dengan hari biasa. Ini ditunjukkan oleh batang biru yang lebih pendek dibandingkan batang hijau.
* Rata-rata penyewaan sepeda pada hari biasa lebih tinggi.
""")




df = pd.DataFrame(day_data)


bike_rental_data = df[['dteday', 'cnt', 'holiday']]
bike_rental_data = bike_rental_data.rename(columns={
    'dteday': 'Tanggal Sewa',
    'cnt': 'Jumlah Sewa Harian',
    'holiday': 'Hari Libur'
})
bike_rental_data['Hari Libur'] = bike_rental_data['Hari Libur'].map({0: 'Tidak Libur', 1: 'Libur'})
bike_rental_data['Tanggal Sewa'] = pd.to_datetime(bike_rental_data['Tanggal Sewa'], format='%Y-%m-%d')
bike_rental_data['Hari'] = bike_rental_data['Tanggal Sewa'].dt.day_name()

st.subheader("Analisis Sewa Sepeda")


selected_day_type = st.selectbox("Pilih Jenis Plot", ["Hari Libur", "Hari dalam Seminggu"])


if selected_day_type == "Hari Libur":
    st.markdown("""**Rata-rata Jumlah Sewa Harian pada Hari Libur**""")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x='Hari Libur', y='Jumlah Sewa Harian', data=bike_rental_data, ax=ax)
    plt.xlabel('Hari Libur')
    plt.ylabel('Rata-rata Jumlah Sewa Harian')
    st.pyplot(fig)
elif selected_day_type == "Hari dalam Seminggu":
    st.markdown("""**Rata-rata Jumlah Sewa Harian Berdasarkan Hari**""")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='Hari', y='Jumlah Sewa Harian', data=bike_rental_data, ax=ax)
    plt.xlabel('Hari')
    plt.ylabel('Rata-rata Jumlah Sewa Harian')
    st.pyplot(fig)


st.markdown("""**Insight diagram Rata-rata Sewa Sepeda:**""")
st.markdown("""
* Rata-rata sewa sepeda pada hari biasa cenderung lebih tinggi dibandingkan dengan hari libur. Hal ini ditunjukkan oleh ketinggian batang pada grafik 'Rata-rata Jumlah Sewa Harian pada Hari Libur'.
* Fluktuasi sewa sepeda pada hari biasa lebih besar dibandingkan dengan hari libur. Hal ini terlihat dari perbedaan tinggi batang pada grafik 'Rata-rata Jumlah Sewa Harian Berdasarkan Hari'.
""")






data = day_data
day_df = pd.DataFrame(data)


season_mapping = {1: 'Winter', 2: 'Fall', 3: 'Summer', 4: 'Spring'}
day_df['season_name'] = day_df['season'].map(season_mapping)


day_df['month'] = pd.to_datetime(day_df['dteday']).dt.month


st.subheader("Pertanyaan 2: Apakah lebih banyak orang menyewa sepeda di musim panas atau musim dingin?")


selected_plot = st.selectbox("Pilih Jenis Plot", ["Berdasarkan Bulan", "Berdasarkan Musim"])


def plot_by_month(data):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='month', y='cnt', data=data, ax=ax)
    plt.title('Rata-rata Jumlah Sewa Harian Berdasarkan Bulan')
    plt.xlabel('Bulan')
    plt.ylabel('Rata-rata Jumlah Sewa Harian')
    return fig

def plot_by_season(data):
    avg_rental_season = data.groupby('season_name')['cnt'].mean()
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.bar(avg_rental_season.index, avg_rental_season.values)
    plt.xlabel('Musim')
    plt.ylabel('Rata-rata Sewa Sepeda')
    plt.title('Perbandingan Sewa Sepeda di Setiap Musim')
    return fig


if selected_plot == "Berdasarkan Bulan":
    fig = plot_by_month(day_df)
else:
    fig = plot_by_season(day_df)


st.pyplot(fig)

st.markdown("""**Insight:**""")
st.markdown("""
* Batang yang mewakili musim panas lebih tinggi dibandingkan dengan batang yang mewakili musim dingin. Ini menunjukkan bahwa rata-rata jumlah penyewaan sepeda pada musim panas jauh lebih besar.
* Cuaca yang hangat dan cerah pada musim panas cenderung mendorong lebih banyak orang untuk beraktivitas di luar ruangan, termasuk bersepeda. Sebaliknya, cuaca dingin dan hujan pada musim dingin dapat mengurangi minat orang untuk bersepeda.
""")





data = hour_data
df = pd.DataFrame(data)

avg_rental_hour = df.groupby('hr')['cnt'].mean()

st.subheader("Pertanyaan 3: Jam berapa yang paling sibuk untuk sewa sepeda?")


fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(avg_rental_hour.index, avg_rental_hour.values, marker='o', color='purple')
ax.set_xlabel('Jam')
ax.set_ylabel('Rata-rata Sewa Sepeda')
ax.set_title('Jam Paling Sibuk untuk Sewa Sepeda')
ax.grid(True)


st.pyplot(fig)


st.markdown("""**Rata-rata Sewa Sepeda per Jam:**""")
st.table(avg_rental_hour)

st.markdown("""**Insight:**""")
st.markdown("""
* Titik tertinggi pada grafik berada di sekitar jam 17.00, yang menunjukkan bahwa rata-rata jumlah penyewaan sepeda mencapai puncaknya pada waktu tersebut.
* Secara umum, grafik menunjukkan pola yang meningkat dari pagi hingga sore hari, mencapai puncaknya di sekitar sore hari, kemudian menurun kembali di malam hari.
""")




st.subheader("Analisis Lanjutan")
st.markdown("""**Teknik Clustering**""")

data = day_data
day_df = pd.DataFrame(data)

season_mapping = {1: 'Winter', 2: 'Fall', 3: 'Summer', 4: 'Spring'}
weather_mapping = {1: 'Cerah', 2: 'Berawan', 3: 'Gerimis', 4: 'Hujan'}
day_df['season_name'] = day_df['season'].map(season_mapping)
day_df['weathersit'] = day_df['weathersit'].map(weather_mapping)



fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x='temp', y='cnt', hue='weathersit', data=day_df, ax=ax)
plt.title('Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda')
plt.xlabel('Suhu')
plt.ylabel('Jumlah Sewa')


st.pyplot(fig)

st.markdown("""**Insight:**""")
st.markdown("""
* Titik-titik data yang mewakili cuaca cerah cenderung berada di bagian atas grafik, menunjukkan jumlah penyewaan yang lebih tinggi. Ini mengindikasikan bahwa ketika cuaca cerah, lebih banyak orang memilih untuk menyewa sepeda.
* Titik-titik data untuk cuaca berawan tersebar cukup merata, namun secara umum jumlah penyewaannya lebih rendah dibandingkan dengan cuaca cerah. Ini menunjukkan bahwa cuaca berawan tidak terlalu mempengaruhi minat orang untuk menyewa sepeda.
* Titik-titik data untuk cuaca gerimis cenderung berada di bagian bawah grafik, menunjukkan jumlah penyewaan yang paling rendah. Ini mengindikasikan bahwa cuaca gerimis sangat mengurangi minat orang untuk menyewa sepeda.
""")




st.subheader("Conclusion:")
st.markdown("""
* Berdasarkan analisis kode dan grafik, dapat disimpulkan bahwa ada perbedaan yang signifikan dalam jumlah sewa sepeda antara hari libur dan hari biasa. Rata-rata, jumlah sewa sepeda lebih tinggi pada hari biasa dibandingkan dengan hari libur.
* Grafik tersebut secara jelas menunjukkan adanya preferensi yang kuat terhadap penyewaan sepeda pada musim panas dibandingkan dengan musim dingin. Faktor cuaca yang lebih menyenangkan pada musim panas menjadi salah satu faktor utama yang mempengaruhi tingginya permintaan akan penyewaan sepeda pada musim tersebut.
* Berdasarkan analisis grafik, dapat disimpulkan bahwa jam 17.00 (jam 5 sore) adalah waktu yang paling sibuk untuk menyewa sepeda. Informasi ini sangat berguna bagi penyedia jasa penyewaan sepeda untuk mengatur operasional mereka, seperti penjadwalan karyawan, pengaturan stok sepeda, dan pengembangan strategi pemasaran.
* Cuaca memiliki pengaruh yang signifikan terhadap jumlah penyewaan sepeda. Cuaca cerah adalah kondisi yang paling ideal untuk mendorong orang menyewa sepeda. Cuaca berawan masih memungkinkan orang untuk menyewa sepeda, namun jumlahnya lebih sedikit. Cuaca gerimis sangat mengurangi minat orang untuk menyewa sepeda.
""")