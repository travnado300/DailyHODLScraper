from flask import Flask, make_response, jsonify
import pandas as pd

app = Flask(__name__)

@app.route("/")
def return_data():
    bitcoinHeadlines = pd.read_csv("bitcoinPricesAdded.csv")
    ethereumHeadlines = pd.read_csv("ethereumPricesAdded.csv")
    combined = pd.concat([bitcoinHeadlines, ethereumHeadlines])

    submit = []
    for index, row in combined.iterrows():
        submit.append({"Title":row["Title"], "Author":row["Author"], "Date":row["Date"], "Link":row["Link"], "Crypto":row["Crypto"], "7 Days Before":row["7 Days Before"], "3 Days Before":row["3 Days Before"], "1 Day Before":row["1 Day Before"], "Day of Writing":row["Day of Writing"],"Next Day":row["Next Day"], "3 Days After":row["3 Days After"], "7 Days After":row["7 Days After"], "14 Days After":row["14 Days After"], "30 Days After":row["30 Days After"], "60 Days After":row["60 Days After"], "90 Days After":row["90 Days After"]})

    return make_response(jsonify(submit), 200)

if __name__ == "__main__":
    app.run()
