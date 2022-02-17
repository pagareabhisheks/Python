import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DF = pd.read_csv(r'C:\Users\pagar\Desktop\Data Science\Python\python11onlinesessionplanboardinfinity\Assignment 2/playstore-analysis (2) (1).csv')

# 1. Data clean up – Missing value treatment
# a. Drop records where rating is missing since rating is our target/study variable
DF = DF.dropna(axis=0,how='any',subset=['Rating'])

# b. Check the null values for the Android Ver column.
# i. Are all 3 records having the same problem?
result_DF = DF[DF['Android Ver'].isnull()]
'''
All the three applications have no data of android versions.
Content rating for app Life Made WI-Fi Touchscreen Photo Frame is unavailable
Also, ratings which should ideally between 10 to 5, this app has rating of 19
Category of the app is also in different format than other apps.
'''
# ii. Drop the 3rd record i.e. record for “Life Made WIFI …”

DF =DF[~DF['App'].isin(['Life Made WI-Fi Touchscreen Photo Frame'])]

# iii. Replace remaining missing values with the mode
DF['Android Ver'].fillna(DF['Android Ver'].mode()[0],inplace=True)


# c. Current ver – replace with most common value
DF['Current Ver'].fillna(DF['Current Ver'].mode()[0],inplace=True)

# 2. Data clean up – correcting the data types
# a. Which all variables need to be brought to numeric types?
DF.dtypes
'''
Variables to convert to numeric types:
    1. Reviews
    2. Price
'''

# b. Price variable – remove $ sign and convert to float
DF = DF[DF.Price!='Everyone']
DF['Price'] = DF['Price'].replace('\$','',regex=True).astype(float)

# c. Installs – remove ‘,’ and ‘+’ sign, convert to integer
DF['Installs'] = DF['Installs'].replace('\+','',regex=True).replace('\,','',regex=True)
DF['Installs'] = pd.to_numeric(DF['Installs'])

# d. Convert all other identified columns to numeric
DF['Reviews'] = DF['Reviews'].astype(int)

#3 Sanity checks – check for the following and handle accordingly
# a. Avg. rating should be between 1 and 5, as only these values are allowed on the play
# store.
# i. Are there any such records? Drop if so.
DF.loc[DF.Rating<1] & DF.loc[DF.Rating>5]
# no such records as the resultant dataframe is empty

# b. Reviews should not be more than installs as only those who installed can review the
# app.
# i. Are there any such records? Drop if so.
DF = DF[~(DF['Reviews']>DF['Installs'])]

# 4. Identify and handle outliers –
# a. Price column
# i. Make suitable plot to identify outliers in price
plt.boxplot(DF['Price'])
plt.show()

# ii. Do you expect apps on the play store to cost $200? Check out these cases
if any(DF['Price'] > 200):
    print('Yes, we can expect apps costing $200 on playstore.')
DF.loc[DF.Price>200]

# iii. After dropping the useless records, make the suitable plot again to identify
# outliers
DF.drop(DF[DF['Price']>30].index,inplace=True)
plt.boxplot(DF['Price'])
plt.show()

# b. Reviews column
# i. Make suitable plot
reviews_plot = DF.groupby(['Category']).agg({'Reviews':'sum'})
reviews_plot = reviews_plot.reset_index()
plt.figure(figsize=(10,5))
plt.bar(reviews_plot['Category'],reviews_plot['Reviews'])
plt.xticks(rotation='vertical')
plt.xlabel('Application Category')
plt.ylabel('Reviews in billions')
plt.show()

# ii. Limit data to apps with < 1 Million reviews
DF.drop(DF[DF['Reviews']>1000000].index, inplace=True)

# c. Installs
# i. What is the 95th percentile of the installs?
print('The 95th percentile of Installs is', int(np.percentile(DF['Installs'],95)))

# ii. Drop records having a value more than the 95th percentile
DF.drop(DF[DF['Installs']>np.percentile(DF['Installs'],95)].index,inplace=True)

# 5. What is the distribution of ratings like? (use Seaborn) More skewed towards higher/lower
# values?
# a. How do you explain this?
sns.distplot(DF['Rating'],hist=True)
plt.show()
'''
Ratings are higher towards higher rating values.
This implies that the mean of the ratings is towards higher rating.
Hence, the distribution is negatively skewed
Majority of the applications have received the ratings between 3.5/5 and 4.5/5.
'''

# b. What is the implication of this on your analysis?
print('The mean of the ratings is',DF['Rating'].mean(),', mode is',DF['Rating'].mode()[0],
      ', and median is',DF['Rating'].median())
print('Due to mean>median=mode, the distribution is skewed towards lower ratings.')

# 6. What are the top Content Rating values?
# a. Are there any values with very few records?
DF.groupby(['Content Rating']).agg({'App':'count'})
# b. If yes, drop those as they won’t help in the analysis
DF.drop(DF[DF['Content Rating']=='Adults only 18+'].index,inplace=True)
DF.drop(DF[DF['Content Rating']=='Unrated'].index,inplace=True)


# 7. Effect of size on rating
# a. Make a joinplot to understand the effect of size on rating
sns.jointplot(data=DF,x=DF['Size'],y=DF['Rating'],marker="+")
plt.show()

# b. Do you see any patterns?
'''
There are certain patterns visible in the jointplot.
The most numbers of ratings are received for the app size of around 20000 bytes
or 20 MB.
App size of 70 MB to 90 MB have received lower-than-average ratings.
General trend of lowest and least ratings for the higher application sizes
can be seen from the jointplot.
'''

# c. How do you explain the pattern?
'''
The downloads for the application are greatly dependent on the size.
Lower the size, more are the downloads, mainly because many factors like mobile
data usage, memory restrictions and how fast the application is ready to be used.
When the application size is huge,they are often discarded by the users mainly
because the amount of memory space it will occupy and also time required to get
it on the mobile phone. Owing to this, the downloads of apps with huge sizes are
comparatively lower, which automatically reduces the number of reviews it gets.

On the other hand, it can be seen that most of the applications on the play 
store have length between 0 to 30 MB. Also, being easy to download and as apps 
consume less amount of memory on the smartphone, these apps are downloaded more 
and evidently, the number of reviews received by these apps is greater. The 
ratings received by these apps are also higher.
'''

# 8. Effect of price on rating
# a. Make a jointplot (with regression line)
sns.jointplot(data=DF,x=DF['Price'],y=DF['Rating'],marker="+",kind='reg')
plt.show()

# b. What pattern do you see?
'''
From the trendline, it can be seen that there is a very slight positive
relationship between ratings and price. As the price of the app goes up, the 
rating also climbs at a very low slope. Most of the applications are free.

The cluttering of datapoints at the upper left corner of the plot can be seen.
Overall, the left-hand side of the plot area is having more observations than
the other areas.

Lower right corner of the plot area is having almost no observations. Also, 
there is a smaller number of higher paid applications which have received 
higher ratings.
'''

# c. How do you explain the pattern?
'''
Majority of the applications can be seen to be free. For an open source system 
like android, it is quite natural to see this trend. There are plenty of the 
applications carrying out the same task, so users can easily find another free 
app with similar functionality.

Spending some money on the applications is still looked at as a privilege, as 
buying the application does not give any tangible output. Also as said earlier,
it is possible to find for another app which provides the same functionality for
free. This is why we can see cluttering of the datapoints in left side as it
represents free or paid apps with a very low cost price.

We can see most of the applications with price range between $0 to $5 have 
received ratings between 4 to 5 out of 5. Users who pay nothing or a very low
fee for having an application naturally have lower expectations than from a 
paid app with significantly higher cost price. 

Also, we can see the datapoints on the plot getting thinner and lesser as the 
application price increases. This supports the last analysis, higher price 
makes the application less appealing for downloads.
'''

# d. Replot the data, this time with only records with price > 0
sns.jointplot(data=DF[DF['Price']>0],x=DF[DF['Price']>0]['Price'],
              y=DF[DF['Price']>0]['Rating'],marker="+",kind='reg')
plt.show()

# e. Does the pattern change?
'''
If we compare the plot before removing the free applications from our dataset 
with the one plotted after removing them, the obvious change that can be seen
is the direction of the trendline in both the plots. 

It is obvious for a user who has paid some amount for using an application in
the overall ecosystem of android system where there are plenty of free apps 
available to be more vocal about his/her views about the apps. Even if the app
fails at the functionality which is not generally used by the user, there would
be a negative feedback on the playstore for that application. In short, the 
expectations from paid apps are higher than that are from free apps. Hence,
we can see that there is a negative slop in the trendline of the later plot,
which shows as the price goes up, app ratings are falling down.

The rating pattern seems to be the same, most of the applications have received 
ratings between 4 to 5 out of 5 for both free and paid applications.
'''

# f. What is your overall inference on the effect of price on the rating
'''
1. Price has a bearing on the rating of an application, but not up to a great
extent as it can be seen that regression line slope is very low.
2. Increased application prices lead to a slight fall in the app ratings.
'''


# 9. Look at all the numeric interactions together –
# a. Make a pairplort with the colulmns - 'Reviews', 'Size', 'Rating', 'Price'
sns.pairplot(DF[['Reviews','Size','Rating','Price']])
plt.show()


# 10. Rating vs. content rating
# a. Make a bar plot displaying the rating for each content rating
DF.groupby(['Content Rating']).agg({'Rating':'count'}).plot.bar()
plt.ylabel('Number of Ratings')
plt.show()

# b. Which metric would you use? Mean? Median? Some other quantile?
'''
If we take a look at the distribution of the content rating over the whole
dataset, we can see it is skewed. For skewed distributions, the extremeties have
a big effect on the mean. Such biased central tendencies can cause errors in 
analysis. 
In the cases of skewed data, we can use median as central tendancy. The main 
reason is median is not affected by the extremeties of the data. This prevents
the central tendancy from giving an inaccurate picture about the data.
'''
# c. Choose the right metric and plot
DF.groupby(['Content Rating']).agg({'Rating':'median'}).plot.bar()




# 11. Content rating vs. size vs. rating – 3 variables at a time
# a. Create 5 buckets (20% records in each) based on Size
bins = [*range(0,100001,20000)]
DF['Buckets'] = pd.cut(DF['Size'],bins,labels=['0-20000 KB','20001-40000 KB',
'40001-60000 KB','60001-80000 KB','80001-100000 KB'])
bucketed_data = pd.pivot_table(DF,values='Rating',index='Buckets',columns='Content Rating')

# b. By Content Rating vs. Size buckets, get the rating (20th percentile) for each
# combination
twenty_percentile = pd.pivot_table(DF,values='Rating',index='Buckets',
columns='Content Rating',aggfunc=lambda x:np.quantile(x,0.2))

# c. Make a heatmap of this
# i. Annotated
sns.heatmap(twenty_percentile,annot=True)
plt.show()

# ii. Greens color map
sns.heatmap(twenty_percentile,annot=True,cmap='Greens')
plt.show()

# d. What’s your inference? Are lighter apps preferred in all categories? Heavier? Some?
'''
From the heatmap. we can clearly see that lighter applications are not preferred.
As the size of the application increases, ratings are increasing.
In third and fifth bucket, we can see the highest ratings. So it can be said
that heavier applications in all categories are preferred.
'''

