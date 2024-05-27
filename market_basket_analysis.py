import pandas as pd
from flask import Blueprint, render_template, request
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

bp = Blueprint("market_basket_analysis", __name__)
te = TransactionEncoder()


@bp.route("/market_basket_analysis", methods=["GET", "POST"])
def market_basket_analysis():
    if request.method == "POST":
        uploaded_file = request.files["file"]
        if uploaded_file.filename != "":
            df = pd.read_csv(uploaded_file, sep="\t")
            # df = df[(df['Nama Produk'] != 'Extra Packing Bubble Wrap')
            #         & (df['Nama Produk'] != 'Extra Packing Bubblewrap')]

            print(df)

            te_ary = te.fit(df.groupby('Kode Transaksi')['Nama Barang'].apply(
                list)).transform(df.groupby('Kode Transaksi')['Nama Barang'].apply(list))
            df_encoded = pd.DataFrame(te_ary, columns=te.columns_)

            frequent_itemsets = apriori(
                df_encoded, min_support=0.001, use_colnames=True)

            rules = association_rules(
                frequent_itemsets, metric="lift", min_threshold=0.001)

            # Sort the rules by lift in descending order
            rules = rules.sort_values(by="lift", ascending=False)

            # Filter out duplicate rules
            unique_rules_df = rules.drop_duplicates(
                subset="lift", keep="first")

            print(unique_rules_df)

            unique_rules_html = unique_rules_df.to_html(
                classes="table table-stripped", index=False)

            return render_template("pages/market_basket_analysis.html", rules=unique_rules_html)

    return render_template("pages/market_basket_analysis.html")
