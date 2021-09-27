from flask import Flask, request
import pymongo
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import os
app = Flask(__name__)
client = pymongo.MongoClient("mongodb+srv://ok31719:Loss_Sent12636@goldbread.bplvo.gcp.mongodb.net/Goldbread?retryWrites=true&w=majority")
db = client["Goldbread"]
collection = db['Transaction']
Transaction = db['Transaction']
  
@app.route('/')
def Association():
  data = pd.DataFrame(list(Transaction.find()))
  data['month'] = pd.DatetimeIndex(data['date']).month
  data = data[data['month'] == 11]
  data = data.drop(columns=['_id', 'index', 'date','month'])
  data = data.set_index('po')
  frequent_itemsets = apriori(data, min_support=0.07, use_colnames=True)
  rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
  rules = rules[['antecedents','consequents','support', 'confidence', 'lift']]
  rules_con = rules[rules['confidence']> 0.75]
  return rules_con.to_json(orient='records', force_ascii=0, double_precision=3)
    
if __name__ == '__main__':
  app.run(debug=False)