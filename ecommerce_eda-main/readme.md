# ECOMMERCE Exploratory Data Analysis
## **PROJECT SYNOPSIS**
> In this project, the EDA protocol for an ecommerce dataset has been shown. The analysis reveals some insightful information for this ecommerce retailer operating in the UK, so do check it out!
___
## **TOOLS USED**
This project uses Python for both the analysis and the visualization. An eclectic range of Python libraries have, however, been used:
- Python 3.8 (analysis + visualization)
- Jupypter Notebook (IDE)
___

## **DATASET DESCRIPTION**
This is a transnational data set which contains all the transactions occurring between 01/12/2010 and 09/12/2011 for a UK-based and registered non-store online retail.The company mainly sells unique all-occasion gifts. Many customers of the company are wholesalers.
Typically e-commerce datasets are proprietary and consequently hard to find among publicly available data. However, The UCI Machine Learning Repository has made this dataset containing actual transactions from 2010 and 2011. The dataset is maintained on their site, where it can be found by the title "Online Retail".
Per the UCI Machine Learning Repository, this data was made available by Dr Daqing Chen, Director: Public Analytics group. chend '@' lsbu.ac.uk, School of Engineering, London South Bank University, London SE1 0AA, UK.
It can be downloaded using this link: https://www.kaggle.com/carrie1/ecommerce-data

Here is a brief context of the data:
- Company - UK-based and registered non-store online retail
- Products for selling - Mainly all-occasion gifts
- Customers - Most are wholesalers (local or international)
- Transactions Period - 1st Dec 2010 - 9th Dec 2011 (One year)
___
## **METHODOLOGY**
1. Imports of Libraries and Packages
2. Import of Dataset
3. Data Wrangling/Preprocessing
4. Exploratory Data Analysis
___
## **ANALYSIS**
### **Environment and Imports**
We first import the libraries and the necessary packages
```
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
%matplotlib inline
import warnings
warnings.filterwarnings('ignore')
```
Next, we import the dataset.
```
df = pd.read_csv("data.csv",engine='python')
df.head()
```
![1](https://user-images.githubusercontent.com/76584894/115151681-662a2800-a087-11eb-9cef-c0c04cde2ff1.JPG)
### **Data Preprocessing**
We now proceed towards preprocessing the data. For this, there are a few steps that need to be followed. These stay the same more or less, regardless of the nature of data:
1. Dataset Description
```
df.describe(include='all')
```
![2](https://user-images.githubusercontent.com/76584894/115151690-70e4bd00-a087-11eb-8e31-82c613ccc925.JPG)
2. Identification of Missing Data in Each Attribute
```
missing_data = df.isnull()
for columns in missing_data.columns.values.tolist():
    print(columns)
    print(missing_data[columns].value_counts())
    print("")
```
![3](https://user-images.githubusercontent.com/76584894/115151702-7a6e2500-a087-11eb-91ec-4df2ea58da76.JPG)

3. Identification of the rows which have missing data
```
df[df.isnull().any(axis=1)].head()
```
![4](https://user-images.githubusercontent.com/76584894/115151711-835ef680-a087-11eb-8b03-0902c7706f00.JPG)

4. Description of Categorical Variables
```
df.describe(include=["object"])
```
![5](https://user-images.githubusercontent.com/76584894/115151718-8b1e9b00-a087-11eb-99df-7b75318fff03.JPG)

5. Removing the Rows with Missing Data
```
df.dropna(inplace=True)
```
6. Changing Column Names (if necessary)
```
df.rename(index=str, columns={"InvoiceNo":"invoice_no","StockCode":"stock_code","Description":"description","Quantity":"quantity","InvoiceDate":"invoice_date","UnitPrice":"unit_price","CustomerID":"customer_id","Country":"country"},inplace=True)
```
![6](https://user-images.githubusercontent.com/76584894/115151745-b1443b00-a087-11eb-914d-2c160a4c84f1.JPG)

7. Identifying the Datatype for Each Attribute
```
df.dtypes
```
![7](https://user-images.githubusercontent.com/76584894/115151775-d46eea80-a087-11eb-8360-7fab0a53472f.JPG)

___
___
> **We now move towards preprocessing/wrangling which is case-specific and may or may not have to be repeated for every dataset.**
___
___
***"invoice_date" to datetime dtype***
```
df['invoice_date'] = pd.to_datetime(df["invoice_date"], format='%m/%d/%Y %H:%M')
```
***"description" to all lower caps***
```
df["description"] = df["description"].str.lower()
df[["description","invoice_date"]].head()
```
![1](https://user-images.githubusercontent.com/76584894/115151866-33ccfa80-a088-11eb-8ad0-25ffb7fa541f.JPG)

***"customer_id" to int64 dtype***
```
df["customer_id"] = df.customer_id.astype("int64")
df.customer_id.dtype
```
***Removing "quantity" with negative values***
```
df = df[df["quantity"] > 0]
df["quantity"].head()
```
***Adding New Columns for Data-Parsing***
```
df.insert(loc=2, column='year_month', value=df['invoice_date'].map(lambda x: 100*x.year + x.month))

df.insert(loc=3, column='month', value=df.invoice_date.dt.month)
# +1 to make Monday=1.....until Sunday=7

df.insert(loc=4, column='day', value=(df.invoice_date.dt.dayofweek)+1)

df.insert(loc=5, column='hour', value=df.invoice_date.dt.hour)
```
***Adding New Column for Revenue/Amount Spent***
```
df["amount_spent"] = df["unit_price"]*df["quantity"]

df_cleaned = df[['invoice_no','invoice_date','stock_code','description','quantity','unit_price','amount_spent','customer_id','country','month', 'day', 'hour']]

df_cleaned.head()
```
![8](https://user-images.githubusercontent.com/76584894/115151913-6e369780-a088-11eb-97a2-b06ee152d035.JPG)

```
df_cleaned.to_excel("cleaned_data.xlsx",index=False)
```
### **Exploratory Data Analysis**
```
df = df_cleaned
df.head()
```
***Top 20 Customers with the Most No. of Orders Placed***
```
cust_orders = df[["invoice_no","customer_id","country"]]
cust_orders = df.groupby(by=["customer_id","country"],as_index=False)["invoice_no"].count()
cust_orders = cust_orders.sort_values(["invoice_no"],ascending=False)
cust_orders = cust_orders.reset_index()
cust_orders.drop("index",axis=1,inplace=True)
cust_orders.rename(columns={"invoice_no":"no_of_orders"}, inplace=True)
cust_orders = cust_orders.head(20)
cust_orders.head()
```
![9](https://user-images.githubusercontent.com/76584894/115151951-958d6480-a088-11eb-8143-3b03694d145a.JPG)

> For Plotting it
```
x = cust_orders["customer_id"]
y = cust_orders["no_of_orders"]
plt.figure(figsize=(23,8))
sns.barplot(x,y)
plt.xlabel("Customer")
plt.ylabel("No. of Orders Placed")
plt.title("Top Customers With the Greatest No. of Orders Placed")
plt.show()
```
![10](https://user-images.githubusercontent.com/76584894/115151996-c372a900-a088-11eb-85a1-f385c0d55a4c.png)


***Top 10 Countries with the Most No. of Orders Placed***
```
country_orders = df[["country","invoice_no"]]
country_orders = country_orders.groupby(by=["country"],as_index=False)["invoice_no"].count()
country_orders = country_orders.sort_values(["invoice_no"],ascending=False)
country_orders = country_orders.reset_index(drop=True)
country_orders.rename(columns={"invoice_no":"no_of_orders"},inplace=True)
country_orders = country_orders.head(10)
country_orders
```
![11](https://user-images.githubusercontent.com/76584894/115152144-5b709280-a089-11eb-98e3-bb8fe4ed37d8.JPG)



> For Plotting it
```
x = country_orders["no_of_orders"]
y = country_orders["country"]
plt.figure(figsize=(24,8))
sns.barplot(x,y)
plt.xlabel("No. of Orders Placed")
plt.ylabel("Country")
plt.title("No. of Orders wrt to Country")
plt.show()
```
![12](https://user-images.githubusercontent.com/76584894/115152146-61667380-a089-11eb-8da9-8f6521ea9394.png)




***Top 20 Customers with the Greatest Spending***
```
customer_spend = df[["customer_id","amount_spent"]]
customer_spend = customer_spend.groupby(by=["customer_id"],as_index=False)["amount_spent"].sum()
customer_spend = customer_spend.sort_values(["amount_spent"],ascending=False)
customer_spend = customer_spend.reset_index(drop=True)
customer_spend = customer_spend.head(20)
customer_spend
```
![13](https://user-images.githubusercontent.com/76584894/115152155-688d8180-a089-11eb-8cea-e4a7ad29d425.JPG)


> For Plotting it
```
x = customer_spend["customer_id"]
y = customer_spend["amount_spent"]
plt.figure(figsize=(24,8))
sns.barplot(x,y)
plt.xlabel("Customer")
plt.ylabel("Amount Spent")
plt.title("Greatest Spenders")
plt.show()
```

![14](https://user-images.githubusercontent.com/76584894/115152163-6deacc00-a089-11eb-8b3c-e00054f7041e.png)



***Top 10 Countries with the Greatest Spending***
```
country_spend = df[["country","amount_spent"]]
country_spend = country_spend.groupby(by=["country"],as_index=False)["amount_spent"].sum()
country_spend = country_spend.sort_values(["amount_spent"],ascending=False)
country_spend = country_spend.head(10)
country_spend = country_spend.reset_index(drop=True)
country_spend
```
![15](https://user-images.githubusercontent.com/76584894/115152172-76db9d80-a089-11eb-90e8-74bd24994b24.JPG)


> For Plotting it
```
plt.figure(figsize=(24,8))
sns.barplot(x="amount_spent",y="country",data=country_spend)
plt.xlabel("Country")
plt.ylabel("Amount Spent")
plt.title("Greatest Spending Countries")
plt.show()
```

![16](https://user-images.githubusercontent.com/76584894/115152175-7ba05180-a089-11eb-8968-1a0388c9c19c.png)



> **TO BE CONTINUED FROM HERE!**

___
## **SUMMARY AND REFLECTION**
This is an exploratory data analysis project which involves some fundamental concepts of EDA and data preprocessing (also known as data wrangling) in Python using an IDE. 
> All rights related to the published dataset are reserved with the issuing authorities of the same (Kaggle).

> The project may be used only as a learning resource; no part of the same must be copied for any other usage whatsover.
