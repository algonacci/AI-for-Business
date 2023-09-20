from flask import Blueprint, render_template, request
import pandas as pd
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

            # Perform one-hot encoding using TransactionEncoder
            te_ary = te.fit(df.groupby('Kode Transaksi')['Nama Barang'].apply(
                list)).transform(df.groupby('Kode Transaksi')['Nama Barang'].apply(list))
            df_encoded = pd.DataFrame(te_ary, columns=te.columns_)

            frequent_itemsets = apriori(
                df_encoded, min_support=0.1, use_colnames=True)

            rules = association_rules(
                frequent_itemsets, metric="lift", min_threshold=1.0)

            # rules = rules[["antecedents", "consequents",
            #                "support", "confidence", "lift"]]

            # Sort the rules by lift in descending order
            rules = rules.sort_values(by="lift", ascending=False)

            # Create a set to keep track of seen rule identifiers
            seen_rules = set()

            # Create a list to store unique rules
            unique_rules = []

            for index, row in rules.iterrows():
                # Create a tuple representing the sorted rule (antecedents and consequents)
                sorted_rule = tuple(
                    sorted(row["antecedents"]) + sorted(row["consequents"]))

                # Check if the sorted rule is in the set of seen rules
                if sorted_rule not in seen_rules:
                    seen_rules.add(sorted_rule)
                    unique_rules.append(row)

            # Create a DataFrame from the unique rules
            unique_rules_df = pd.DataFrame(unique_rules)

            unique_rules_html = unique_rules_df.to_html(
                classes="table table-stripped", index=False)

            return render_template("pages/market_basket_analysis.html", rules=unique_rules_html)

    return render_template("pages/market_basket_analysis.html")
