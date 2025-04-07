# -*- coding: utf-8 -*-
"""Capstone_rekomendasi.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_7BGS23UY5ROUGyw_EnVp3VZSAS6eKW_
"""

import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS  # Impor Flask-CORS

app = Flask(__name__)
CORS(app)
df = pd.read_csv("bandung.csv")
df.drop_duplicates(inplace=True)


def rekomendasi_populer(df, top_n=50, kota_pilihan=None):
    # Hitung skor popularitas
    global df 
    bobot_rating = 0.7
    df["skor_popularitas"] = df["Rating"] * bobot_rating

    # Filter berdasarkan kota jika diberikan
    if kota_pilihan:
       df = df[df["Kota"].astype(str) == str(kota_pilihan)]

    df["Kota"] = df["Kota"].str.strip()

    # Urutkan berdasarkan skor popularitas
    df_sorted = df.sort_values(by="skor_popularitas", ascending=False)

    # Ambil top N tempat wisata
    top_wisata = df_sorted.head(top_n)

    # Pilih kolom yang akan ditampilkan
    rekomendasi = top_wisata[["Nama Tempat Wisata", "Kota", "Jenis Wisata", "Rating", "Deskripsi Singkat"]]

    return rekomendasi

@app.route('/rekomendasi', methods=['GET'])
def get_rekomendasi_wisata():
    file_path = "bandung.csv"
    kota_pilihan = None
    rekomendasi = rekomendasi_populer(file_path, top_n=500, kota_pilihan=kota_pilihan)
    return jsonify(rekomendasi.to_dict(orient='records'))

if __name__ == "__main__":
   app.run()
