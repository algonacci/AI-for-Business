import pickle

import pandas as pd
from flask import Blueprint, render_template, request
from kmodes.kprototypes import KPrototypes
from sklearn.preprocessing import LabelEncoder, StandardScaler

bp = Blueprint("customer_segmentation", __name__)


with open('cluster.pkl', 'rb') as file:
    model = pickle.load(file)

kproto = KPrototypes(n_clusters=5, random_state=75)


@bp.route("/customer_segmentation", methods=["GET", "POST"])
def customer_segmentation():
    if request.method == "POST":
        df = pd.read_csv(request.files["file"], sep="\t")
        kolom_numerik = ['Umur', 'NilaiBelanjaSetahun']
        kolom_kategorikal = ['Jenis Kelamin', 'Profesi', 'Tipe Residen']
        df_std = StandardScaler().fit_transform(df[kolom_numerik])
        df_std = pd.DataFrame(data=df_std, index=df.index,
                              columns=df[kolom_numerik].columns)
        df_encode = df[kolom_kategorikal].copy()
        for col in kolom_kategorikal:
            df_encode[col] = LabelEncoder().fit_transform(df_encode[col])
        df_model = df_encode.merge(
            df_std, left_index=True, right_index=True, how='left')
        clusters = model.predict(df_model, categorical=[0, 1, 2])
        print('Segment pelangan {}\n'.format(clusters))
        df_final = df.copy()
        df_final['Cluster'] = clusters
        df_final['Segmen'] = df_final['Cluster'].map({
            0: 'Diamond Young Member',
            1: 'Diamond Senior Member',
            2: 'Silver Member',
            3: 'Gold Young Member',
            4: 'Gold Senior Member'
        })
        table = df_final.to_html(classes="table table-stripped", index=False)
        return render_template("pages/customer_segmentation.html", table=table)

    else:
        return render_template("pages/customer_segmentation.html")
