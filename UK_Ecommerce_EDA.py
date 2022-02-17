import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

DF = pd.read_csv(r'C:\Users\pagar\Desktop\Data Science\Python\BI Project\Project 2\Ecommerce - UK Retailer.csv',encoding='unicode_escape')

# 1. Perform Basic EDA
    # a. Boxplot – All Numeric Variables
plt.boxplot(DF['Quantity'])
plt.show()

plt.boxplot(DF['UnitPrice'])
plt.show()

    # b. Histogram – All Numeric Variables
plt.hist(DF['Quantity'])
plt.xlabel('Quantity')
plt.show()

plt.hist(DF['UnitPrice'])
plt.xlabel('Unit Price')
plt.show()

    # c. Distribution Plot – All Numeric Variables
sns.distplot(DF['Quantity'])
plt.show()

sns.distplot(DF['UnitPrice'])
plt.show()

    # d. Aggregation for all numerical Columns
DF[['Quantity','UnitPrice']].describe()

    # e. Unique Values across all columns
unique_values={}
j=0
for i in list(DF):
     unique_values[j] = DF[i].unique()
     unique_values['Unique '+i] = unique_values.pop(j)
     j = j+1
    
    # f. Duplicate values across all columns
duplicated_values = {}
n=0
for m in list(DF):
    duplicated_values[n] = DF[m][DF[m].duplicated(keep='first')]
    duplicated_values['Duplicated '+m] = duplicated_values.pop(n)
    n+=1
    
    # g. Correlation – Heatmap - All Numeric Variables
sns.heatmap(pd.pivot_table(DF,values='UnitPrice',columns='Quantity',aggfunc=np.mean))

    # h. Regression Plot - All Numeric Variables
sns.regplot(x=DF['UnitPrice'],y=DF['Quantity'])

    # i. Bar Plot – Every Categorical Variable vs every Numerical Variable
DF.groupby(['InvoiceNo']).agg({'Quantity':'mean'}).reset_index().plot.bar(x='InvoiceNo',y='Quantity')
DF.groupby(['StockCode']).agg({'Quantity':'mean'}).reset_index().plot.bar(x='StockCode',y='Quantity')
DF.groupby(['Description']).agg({'Quantity':'mean'}).reset_index().plot.bar(x='Description',y='Quantity')
DF.groupby(['InvoiceDate']).agg({'Quantity':'mean'}).reset_index().plot.bar(x='InvoiceDate',y='Quantity')
DF.groupby(['CustomerID']).agg({'Quantity':'mean'}).reset_index().plot.bar(x='CustomerID',y='Quantity')
DF.groupby(['Country']).agg({'Quantity':'mean'}).reset_index().plot.bar(x='Country',y='Quantity')

DF.groupby(['InvoiceNo']).agg({'UnitPrice':'mean'}).reset_index().plot.bar(x='InvoiceNo',y='UnitPrice')
DF.groupby(['StockCode']).agg({'UnitPrice':'mean'}).reset_index().plot.bar(x='StockCode',y='UnitPrice')
DF.groupby(['Description']).agg({'UnitPrice':'mean'}).reset_index().plot.bar(x='Description',y='UnitPrice')
DF.groupby(['InvoiceDate']).agg({'UnitPrice':'mean'}).reset_index().plot.bar(x='InvoiceDate',y='UnitPrice')
DF.groupby(['CustomerID']).agg({'UnitPrice':'mean'}).reset_index().plot.bar(x='CustomerID',y='UnitPrice')
DF.groupby(['Country']).agg({'UnitPrice':'mean'}).reset_index().plot.bar(x='Country',y='UnitPrice')

    # j. Pair plot - All Numeric Variables
sns.pairplot(DF.head(10000)[['Quantity','UnitPrice']])
plt.show()
    # k. Line chart to show the trend of data - All Numeric/Date Variables
DF = DF.astype({'CustomerID':int})
sales = DF[['InvoiceDate','CustomerID','Quantity','UnitPrice','Country']]
sales['Sales'] = DF['Quantity']*DF['UnitPrice']
sales.plot.line(x='InvoiceDate',y='Quantity',rot=90,figsize=(10,10))
sales.plot.line(x='InvoiceDate',y='UnitPrice',rot=90,figsize=(10,10))
sales.plot.line(x='InvoiceDate',y='Sales',rot=90,figsize=(10,10))

    # l. Plot the skewness - All Numeric Variables
sns.distplot(DF['Quantity'])
sns.distplot(DF['UnitPrice'])

# 2. Check for missing values in all columns and replace them with the 
# appropriate metric (Mean/Median/Mode)
for a in list(DF):
    print('The total null values in column',a,'are', DF[a].isnull().sum()) #to check where do null values lie
for b in ['Description','CustomerID']:
    DF[b].fillna(DF[b].mode()[0],inplace=True)
    print('The total null values in column',b,'are', DF[b].isnull().sum()) #to check if there are any null values remained

# 3. Remove duplicate rows
DF = DF.drop_duplicates()

# 4. Remove rows which have negative values in Quantity column
DF.drop(DF[DF['Quantity']<0].index,inplace=True)

# 5. Add the columns - Month, Day and Hour for the invoice
DF['InvoiceDate'] = pd.to_datetime(DF['InvoiceDate'])
DF['Month'] = DF['InvoiceDate'].dt.strftime('%B')
DF['Day'] = DF['InvoiceDate'].dt.day_name()
DF['Hour'] = DF['InvoiceDate'].dt.strftime('%H')

# 6. How many orders made by the customers?
number_of_orders_by_customers = DF.groupby(['CustomerID']).agg({'InvoiceNo':'count'}).rename(columns={'InvoiceNo':'Total Orders'})

# 7. TOP 5 customers with higher number of orders
print('Top 5 customers with highest orders are:')
number_of_orders_by_customers.sort_values('Total Orders',ascending=False).head(5)

# 8. How much money spent by the customers?
money_spent_by_customers = sales.groupby(['CustomerID']).agg({'Sales':'sum'})

# 9. TOP 5 customers with highest money spent
print('Top 5 customers with highest money spent are:')
money_spent_by_customers.sort_values('Sales',ascending=False).head(5)

# 10. How many orders per month?
DF.groupby(['Month']).agg({'InvoiceNo':'count'})

# 11. How many orders per day?
print('There are',
int(np.size(DF['InvoiceNo'].unique())/(max(DF['InvoiceDate'])-min(DF['InvoiceDate'])).days),
'orders per day.')

# 12. How many orders per hour?
print('There are',
int(np.size(DF['InvoiceNo'].unique())/(((max(DF['InvoiceDate'])-min(DF['InvoiceDate'])).days)*24)),
'orders per hour.')

# 13. How many orders for each country?
DF.groupby(['Country']).agg({'InvoiceNo':'nunique'})

# 14. Orders trend across months
order_trend = DF.groupby(['Month']).agg({'InvoiceNo':'nunique'}).reset_index().rename(columns={'InvoiceNo':'Orders'})
order_trend['Month'] = pd.Categorical(order_trend['Month'],
['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
order_trend = order_trend.sort_values('Month')
order_trend.plot.line(x='Month',y='Orders',rot=90)

# 15. How much money spent by each country?
sales.groupby(['Country']).agg({'Sales':'sum'}).rename(columns={'Sales':'$ Sales'})


