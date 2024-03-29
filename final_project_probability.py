# -*- coding: utf-8 -*-
"""Final_Project_Probability.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WPjx0gu3oZLUi12QEiSKEr9MSof1czBq

**IMPORT DATASET**

---
"""

#Import Library yang akan dibutuhkan
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from scipy import stats
from scipy.stats import ttest_ind
from scipy.stats import chi2_contingency
from scipy.stats import levene
from statsmodels.stats.proportion import proportions_ztest
import copy

path_database = "/content/drive/MyDrive/insurance.csv"

df = pd.read_csv(path_database)

from google.colab import drive
drive.mount('/content/drive')

df.head(5)

df.describe()

"""**ANALISA STATISTIK DESKRIPTIF**

---


Analisa statistik deskriptif bertujuan untuk merangkum
karakter-karakter berdasarkan data. Proses merangkum ini dapat dilakukan dengan eksplorasi data. Ekplorasi data berguna untuk mengetahui insight atau informasi dari sebuah data misalnya persebaran data, menghitung rata-rata, mengetahui nilai tertinggi dan terendah pada sebuah data.


Berikut data yang akan dieksplorasi sebagai berikut:


1. Rata-rata umur nasabah asuransi
2. Rata-rata nilai BMI dari nasabah yang perokok
3. Rata-rata umur nasabah yang perokok
4. Rata-rata umur nasabah perempuan perokok dengan nasabah laki-laki perokok
5. Jumlah tagihan berdasarkan nasabah perokok dengan nasabah non perokok




"""

#1. Rata-rata Umur Nasabah Asuransi
mean_age = df['age'].mean()
df.describe()

#Visualisasi data dengan Matplotlib
plt.figure(figsize=(10,6))
plt.hist(df['age'],bins=10, edgecolor='green')
plt.axvline(mean_age,color='blue',linestyle='dashed',linewidth=1.5, label="Rata-rata Umur")
plt.xlabel('Age')
plt.ylabel('Range')
plt.title('Distrubsi Data Umur')
plt.legend()
#plt.savefig("img/distibusi-data-umur.jpeg")
plt.show()

#2. Rata-rata Nilai BMI dari Nasabah yang Perokok
df['bmi'].groupby(df['smoker']).mean()

#3. Rata-rata Umur Nasabah yang Perokok
df['age'].groupby(df['smoker']).mean()

#4. Rata-rata Umur Nasabah Perempuan Perokok dan Nasabah Laki-laki Perokok
df.groupby(['sex', 'smoker']).mean('age')

#5. Jumlah Tagihan Nasabah Perokok dengan Nasabah Nonperokok
df['charges'].groupby(df['smoker']).mean()

"""**ANALISA VARIABEL KATEGORIK**

---

Dataset diolah untuk memperdalam analisa. Analisa data digunakan dengan identifikasi peluang berdasarkan kondisi tertentu. Berikut analisa data variable kategorik:


1. Tagihan asuransi berdasarkan gender
2. Tagihan asuransi pada tiap daerah
3. Proporsi data pada tiap daerah
4. Proporsi nasabah perokok dan nasabah nonperokok
5. Peluang seseorang adalah nasabah perempuan yang perokok


"""

#1. Tagihan Asuransi berdasarkan Gender
df['charges'].groupby(df['sex']).sum()

#2. Tagihan Asuransi di Tiap Daerah
df['charges'].groupby(df['region']).sum()

#3. Proposi Data di Tiap Daerah
df['charges'].groupby(df['region']).describe()

df['sex'].groupby(df['region']).describe()

#4. Proporsi Data Nasabah Perokok dengan Nasabah Nonperokok
df.groupby(['smoker']).agg('count')

#5. Peluang Seseorang adalah Nasabah Perempuang yang Perokok

#Menghitung nasabah yg perokok
n_smokers = df['smoker'].where(df['smoker']=='yes').value_counts()

#Menghitung nasabah perempuan perokok
n_female_smoker = df['smoker'].where(df['sex']=='female').value_counts()

#Menghitung peluang seseorang adalah perempuan dan dia adalah perokok
smoker_female_smoker= n_female_smoker[1]/n_smokers
print(f"Peluang seseorang adalah perempuan dan dia adalah perokok: {smoker_female_smoker:}")

"""**ANALISA VARIABEL KONTINYU**

---

1. Mana yang lebih mungkin terjadi:

    a. Seseorang dengan BMI di atas 25 mendapatkan tagihan kesehatan di atas $16.700, atau

    b. Seseorang dengan BMI di bawah 25 mendapatkan tagihan kesehatan di atas $16.700


2. Mana yang lebih mungkin terjadi:

    a. Seseorang perokok dengan BMI di atas 25 mendapatkan tagihan kesehatan di atas $16.700, atau

    b. Seseorang nonperokok dengan BMI di atas 25 mendapatkan tagihan kesehatan di atas $16.700


"""

#Menghitung jumlah tagihan nasabah di atas 16700k
n_sample= df[df['charges'] > 16700].value_counts().sum()
print(f'Jumlah orang yang mendapatkan tagihan di atas $16.700 adalah {n_sample:.0f} orang')

#Menghitung BMI di atas 25 dan tagihan di tagihan di atas $16.700
#Menghitung jumlah nasabah dengan BMI di atas 25
data_a= df.where((df['bmi'] > 25) & (df['charges']>16700)).value_counts().sum()
print(f"Peluang seseorang dengan BMI di atas 25 dengan tagihan di atas $16.700 adalah {data_a:.0f} orang")

#Menghitung peluang seseorang dengan BMI di atas 25 dan tagihan di atas $16.700
peluang_a= data_a/n_sample
print(f"Peluang nasabah dengan BMI di atas 25 dan tagihan di atas $16.700 adalah {peluang_a:.2f}")

#Menghitung BMI di bawah 25 dan tagihan di atas $16.700
#Menghitung jumlah nasabah dengan BMI di bawah 25
data_b= df.where((df['bmi'] < 25) & (df['charges']>16700)).value_counts().sum()
print(f"Peluang seseorang dengan BMI di bawah 25 dengan tagihan di atas $16.700 adalah {data_b:.0f} orang")

#Menghitung peluang seseorang dengan BMI di bawah 25 dan tagihan di atas 16700
peluang_b= data_b/n_sample
print(f"Peluang nasabah dengan BMI di bawah 25 dan tagihan di atas $16.700 adalah {peluang_b:.2f}")

#Menghitung jumlah nasabah yang BMI di atas 25 dan tagihannya di atas $16.700
n_data = df[df['bmi']>25].where(df['charges']>16700).value_counts().sum()
print(f"Jumlah nasabah yang BMI di atas 25 dan tagihannya di atas 16700K {n_data:.0f} orang")

#Menghitung nasabah perokok yang BMI di atas 25 dan tagihannya di atas $16.700
data_1 = df.where((df['smoker']=='yes') & (df['bmi']>25) & (df['charges']>16700)).value_counts().sum()
print(f"Jumlah nasabah perokok yang BMI di atas 25 dengan tagihan di atas $16.700 {data_1:.0f} orang")

#Peluang nasabah perokok yang BMI di atas 25 dan tagihan di atas $16.700
p_smoker = data_1/n_data
print(f"Peluang nasabah perokok yang BMI di atas 25 dan tagihannya di atas $16.700 {p_smoker:.2f}")

#Menghitung nasabah nonperokok yang BMI di atas 25 dengan tagihan di atas $16.700
data_2 = df.where((df['smoker']=='no') & (df['bmi']>25) & (df['charges']>16700)).value_counts().sum()
print(f"Jumlah nasabah nonperokok yang BMI di atas 25 dengan tagihan di atas $16.700 {data_2:.0f} orang")

#Peluang nasabah nonperokok yang BMI di atas 25 dengan tagihan di atas $16.700
p_no_smoker = data_2/n_data
print(f"Peluang nasabah nonperokok yang BMI di atas 25 dengan tagihan di atas $16.700 {p_no_smoker:.2f}")

"""**ANALISA KORELASI VARIABEL**

---
Variabel-variabel yang telah dianalisis dicari keterikatannya satu sama lain dengan method corr(). Pada method corr, data yang hanya bersifat numerikal yang dapat dicari keterikatannya satu dengan lainnya. Variabel-variabel yang akan dicari keterikatannya yaitu umur, bmi, jumlah anak dan tagihan asuransi.


"""

correlation_df= df[['age', 'sex','bmi','charges',]].corr(method='pearson')

#Visualisasi data dengan heatmap
sns.heatmap(correlation_df, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()

"""Hasil korelasi antar variabel berkorelasi positif dengan nilai korelasi yang berbeda-beda. Korelasi yang memiliki nilai besar yaitu variabel tagihan dengan usia sebesar 0,3. Selanjutnya korelasi dari variable bmi dan tagihan sebesar 0,2.

**PENGUJIAN HIPOTESA**

---
"""

Pada pengujian hipotesa ini akan menguji 3 populasi pada data. Berikut pengujian hipotesa sebagai berikut:
1. Tagihan asuransi berdasarkan nasabah Perokok dan Nonperokok
2. Tagihan asuransi berdasarkan gender

#1. Tagihan asuransi berdasarkan nasabah perokok dan nonperokok

#H0: "Tagihan asuransi nasabah perokok > tagihan asuransi nasabah nonperokok"
#H1: "Tagihan asuransi nasabah perokok < tagihan asuransi nasabah nonperokok"

#Pengelompokan data

#Pengelompokan data tagihan asuransi berdasarkan nasabah perokok
smokers= df[df['smoker']=='yes']['charges']
#print(f"Jumlah data tagihan dari nasabah perokok: {smokers}")

#Banyaknya jumlah data sampel tagihan asuransi berdasarkan nasabah perokok
n_smoker=df['charges'].where(df['smoker']=='yes').value_counts().sum()
print(f"Banyaknya data sampel tagihan asuransi berdasarkan nasabah perokok: {n_smoker:.0f}")

#Pengelompokan data tagihan asuransi berdasarkan nasabah nonperokok
non_smoker=df[df['smoker']=='no']['charges']
#print(f"Jumlah data tagihan dari nasabah perokok: {non_smoker}")


#Banyaknya jumlah data sampel tagihan asuransi berdasarkan nasabah nonperokok
n_nonsmoker= df['charges'].where(df['smoker']=='no').value_counts().sum()
print(f"Banyaknya data sampel tagihan asuransi berdasarkan nasabah nonperokok: {n_nonsmoker:.0f}")

#Tingkat siginifikansi
alpha = 0.05

#Uji Statistik
t_statistic, p_value= stats.ttest_ind(smokers, non_smoker)
print('uji t-statistik:{}'.format(t_statistic))
print('p_value:{}'.format(p_value))

if p_value < alpha:
  print("H0 ditolak. Tagihan asuransi nasabah perokok > tagihan asuransi nasabah nonperokok.")
else:
  print("H0 diterima.Tagihan asuransi nasabah perokok < tagihan asuransi nasabah nonperokok.")

#2. Tagihan asuransi berdasarkan gender

#H0: "Tagihan asuransi nasabah laki-laki > tagihan asuransi nasabah perempuan"
#H1: "Tagihan asuransi nasabah laki-laki < tagihan asuransi nasabah perempuan"

#Pengelompokan data

#Pengelompokan data tagihan asuransi berdasarkan nasabah perempuan
female= df[df['sex']=='female']['charges']
#print(f"Jumlah data tagihan dari nasabah perempuan: {female}")

#Jumlah tagihan berdasarkan gender
charge_by_gender=df['charges'].groupby(df['sex']).mean()
print(f"Tagihan berdasarkan: {charge_by_gender}")

#Pengelompokan data tagihan asuransi berdasarkan nasabah laki-laki
male=df[df['sex']=='male']['charges']
#print(f"Jumlah data tagihan dari nasabah laki-laki: {male}")

#Tingkat siginifikansi
alpha = 0.05

#Uji Statistik
t_statistic, p_value= stats.ttest_ind(female, male)
print('uji t-statistik:{}'.format(t_statistic))
print('p_value:{}'.format(p_value))

if p_value < alpha:
  print("H0 ditolak. Tagihan asuransi nasabah laki-laki > tagihan asuransi nasabah perempuan.")
else:
  print("H0 diterima. Tagihan asuransi nasabah laki-laki < tagihan asuransi nasabah perempuan.")