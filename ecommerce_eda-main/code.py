from IPython import get_ipython
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')
import warnings
warnings.filterwarnings('ignore')
df = pd.read_csv("data.csv",engine='python')
df.head()
df.describe(include='all')
missing_data = df.isnull()
for columns in missing_data.columns.values.tolist():
    print(columns)
    print(missing_data[columns].value_counts())
    print("")
df.describe(include=["object"])
df.rename(index=str, columns={"InvoiceNo":"invoice_no","StockCode":"stock_code","Description":"description","Quantity":"quantity","InvoiceDate":"invoice_date","UnitPrice":"unit_price","CustomerID":"customer_id","Country":"country"},inplace=True)
df.columns
df.isnull().sum().sort_values(ascending=False)
df[df.isnull().any(axis=1)].head()
df.dropna(inplace=True)
df.isnull().sum()
df.dtypes
df['invoice_date'] = pd.to_datetime(df["invoice_date"], format='%m/%d/%Y %H:%M')
df["description"] = df["description"].str.lower()
df[["description","invoice_date"]].head()
df["customer_id"] = df.customer_id.astype("int64")
df.customer_id.dtype
df = df[df["quantity"] > 0]
df["quantity"]
df.insert(loc=2, column='year_month', value=df['invoice_date'].map(lambda x: 100*x.year + x.month))
df.insert(loc=3, column='month', value=df.invoice_date.dt.month)
df.insert(loc=4, column='day', value=(df.invoice_date.dt.dayofweek)+1)
df.insert(loc=5, column='hour', value=df.invoice_date.dt.hour)
df["amount_spent"] = df["unit_price"]*df["quantity"]
df.columns
df_cleaned = df[['invoice_no','invoice_date','stock_code','description','quantity','unit_price','amount_spent','customer_id','country','month', 'day', 'hour']]
df_cleaned.head()
df_cleaned.to_excel("cleaned_data.xlsx",index=False)
df = df_cleaned
cust_orders = df[["invoice_no","customer_id","country"]]
cust_orders.head(3)
cust_orders = df.groupby(by=["customer_id","country"],as_index=False)["invoice_no"].count()
cust_orders = cust_orders.sort_values(["invoice_no"],ascending=False)
cust_orders = cust_orders.reset_index()
cust_orders.head()
cust_orders.drop("index",axis=1,inplace=True)
cust_orders.head()
cust_orders.rename(columns={"invoice_no":"no_of_orders"}, inplace=True)
cust_orders = cust_orders.head(20)
x = cust_orders["customer_id"]
y = cust_orders["no_of_orders"]
plt.figure(figsize=(23,8))
sns.barplot(x,y)
plt.xlabel("Customer")
plt.ylabel("No. of Orders Placed")
plt.title("Top Customers With the Greatest No. of Orders Placed")
plt.show()
country_orders = df[["country","invoice_no"]]
country_orders.head(3)
country_orders = country_orders.groupby(by=["country"],as_index=False)["invoice_no"].count()
country_orders.head(4)
country_orders = country_orders.sort_values(["invoice_no"],ascending=False)
country_orders.head()
country_orders = country_orders.reset_index(drop=True)
country_orders.rename(columns={"invoice_no":"no_of_orders"},inplace=True)
country_orders
country_orders = country_orders.head(10)
country_orders
x = country_orders["no_of_orders"]
y = country_orders["country"]
plt.figure(figsize=(24,8))
sns.barplot(x,y)
plt.xlabel("No. of Orders Placed")
plt.ylabel("Country")
plt.title("No. of Orders wrt to Country")
plt.show()
customer_spend = df[["customer_id","amount_spent"]]
customer_spend = customer_spend.groupby(by=["customer_id"],as_index=False)["amount_spent"].sum()
customer_spend = customer_spend.sort_values(["amount_spent"],ascending=False)
customer_spend.head()
customer_spend = customer_spend.reset_index(drop=True)
customer_spend = customer_spend.head(20)
customer_spend
x = customer_spend["customer_id"]
y = customer_spend["amount_spent"]
plt.figure(figsize=(24,8))
sns.barplot(x,y)
plt.xlabel("Customer")
plt.ylabel("Amount Spent")
plt.title("Greatest Spenders")
plt.show()
country_spend = df[["country","amount_spent"]]
country_spend = country_spend.groupby(by=["country"],as_index=False)["amount_spent"].sum()
country_spend = country_spend.sort_values(["amount_spent"],ascending=False)
country_spend = country_spend.head(10)
country_spend
country_spend = country_spend.reset_index(drop=True)
country_spend
plt.figure(figsize=(24,8))
sns.barplot(x="amount_spent",y="country",data=country_spend)
plt.xlabel("Country")
plt.ylabel("Amount Spent")
plt.title("Greatest Spending Countries")
plt.show()
