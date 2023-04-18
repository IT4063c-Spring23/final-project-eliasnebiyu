# -*- coding: utf-8 -*-
"""source.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Jv-LRhRJ91qiBlOlSZmExw_fLkZrCEvu
"""



"""# **FINAL PROJECT-NEBIYU TADESSE**

# {TRAFFIC ACCIDENT CAUSES AND GENERAL ANALYSIS}

- Name: **Nebiyu Elias Tadesse**

### *What problem are you (or your stakeholder) trying to address? - <a class="anchor" id="Requirements"></a> 
- One of the main problem that I am trying to answer is the cause for most of the traffic accidents and the cause so as to educate people that drive, inturn make roads safer. Laying out the most commin causes can be beneficial to drivers as they will avoid certain scenarios that would otherwise be dangerous for them.

## Data Source
- Data: **NHTSA for the State of Tennesse, Mississippi, Alabama, and Georgia**
**US Accidents (2016 - 2021)**
**Introduction to Traffic Crash Analysis**

https://www.nhtsa.gov/traffic-records/state-data-information-resources
https://doc.arcgis.com/en/arcgis-solutions/11.0/reference/introduction-to-traffic-crash-analysis.htm#:~:text=Traffic%20Crash%20Analysis%20can%20be,serious%20and%20fatal%20crashes%20occur.

https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents
## What Questions am I Trying To Answer? <a class="anchor" id="QA"></a>
 - How many people are involved in accidents?
 - Are there more accidents in cloudy or raining areas?
 - Which states have the highest number of accidents?
 - Among the top 100 cities in number of accidents, which states do they belong to most frequently?
 - What time of the day are accidents most frequent in?
 - Which days of the week have the most accidents?
 - Are more accidents prevalent when people get drunk?

**What would an answer look like? As well as the benefits of answering those questions.**
- MORE PEOPLE CAUSE ACCIDENTS WHEN THEY ARE INTOXICATED. 
- RAINY CONDITIONS OR BAD WEATHER ARE FACTORS IN CAR ACCIDENT FATALITY. 
- SOME OF THE BENEFITS OF ANSWERING TOSE QUESTIONS WOULD BE:
- PREVENTION AND AVOIDANCE OF FUTURE ACCIDENTS
- FASTER RESPONSE TIME TO ACCIDENTS
- ESTIMATE HOW MANY ACCIDENTS HAPPEN DUE TO ALCOHOL 
- IMPROVE THE ARRIVAL TIME OF HOSPITAL


- **LAYOUT OF MY BASIC PLAN FOR THIS ANALYSIS**
-  Understanding data
    
- Identifying the problems that I want to solve and metrics that I want to figure out.
- Data preparaion
- Visualizations
- Evaluation
- Deployment
- Classification Analysis
- Cluster Analysis
"""



"""# Data Understanding & Exploratory Data Analysis <a class="anchor" id="Dataunderstanding"></a>
The second stage of the process requires to acquire the data.

## IMPORTING NECESSARY LIBRARIES.  <a class="anchor" id="Datareport"></a>
"""

# Commented out IPython magic to ensure Python compatibility.
# Import Libraries Required
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
import numpy as np
import seaborn as sns
import folium
from folium.plugins import HeatMap
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
# %matplotlib inline
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
# %matplotlib inline

"""##  Describe Data <a class="anchor" id="Describedata"></a>
Data description report - I loaded the data and decribed the data to see what I will be working with. 
"""

from google.colab import files

uploaded = files.upload()

for fn in uploaded.keys():
  print('User uploaded file "{name}" with length {length} bytes'.format(
      name=fn, length=len(uploaded[fn])))

accident_data = pd.read_csv('accident.csv',encoding_errors='ignore')

df_region = accident_data.loc[(accident_data['STATENAME'] == "Tennesse")|
                       (accident_data['STATENAME'] == "Mississippi")|
                       (accident_data['STATENAME'] ==  "Alabama")|
                       (accident_data['STATENAME'] == "Georgia")]
df_region.head()

"""**I pulled out the raw data of 4 assingned states Tennesse, Mississippi, Alabama, and Georgia. Then, I started to transform and explore the data.**"""

df_region.shape

"""**There are totally 2814 accident cases happened in the 4 states in 2019.**"""

df_region.columns

df_region.describe()

df_region.info()

"""##  Verify Data Quality <a class="anchor" id="Verifydataquality"></a>
This step is to transform the data including find out any errors, missing data. As you can see there is no empty dataset as it was tidy data. So, dataset is good to continue exploring and doing visualizations.

###  Missing Data <a class="anchor" id="MissingData"></a>
"""

df_region.isnull().sum()

def missing_values_table(df):
        mis_val = df.isnull().sum()
        mis_val_percent = 100 * df.isnull().sum() / len(df)
        mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
        mis_val_table_ren_columns = mis_val_table.rename(
        columns = {0 : 'Missing Values', 1 : '% of Total Values'})
        mis_val_table_ren_columns = mis_val_table_ren_columns[
            mis_val_table_ren_columns.iloc[:,1] != 0].sort_values(
        '% of Total Values', ascending=False).round(1)
        print ("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"      
            "There are " + str(mis_val_table_ren_columns.shape[0]) +
              " columns that have missing values.")
        return mis_val_table_ren_columns

missing_values_table(df_region)

# Get the columns with > 50% missing
missing_df = missing_values_table(df_region);
missing_columns = list(missing_df[missing_df['% of Total Values'] > 50].index)
print('I will remove %d columns.' % len(missing_columns))

# Drop the columns
df = df_region.drop(list(missing_columns), axis = 1)

"""### 2.3.2. Outliers <a class="anchor" id="Outliers"></a>

"""

Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)
IQR = Q3 - Q1
print(IQR)

"""**The difference of Q3 and Q1 in each factor. For example, the IQR of HOUR is 12 which means that the middle half of data is 12p.m when the accident case mostly happened in the range of 24 hours.**"""

sns.boxplot(y=df['HOUR'])

"""**This boxplot graph shows about a specific period time that mostly happening the number of accident case which ranges from afternoon to night. I have also recognized the outliers do not matter as just a little amount of data showing the outlier, so the data is good to go.**

### Data Exploration & Visualization <a class="anchor" id="Exploredata"></a>

### Distributions  <a class="anchor" id="Distributions"></a>
"""

lat_lon_pairs = list(zip(list(df.LATITUDE), list(df.LONGITUD)))
map = folium.Map(location=[lat_lon_pairs[0][0], lat_lon_pairs[0][1]])
df_angle = df[df['MAN_COLL'] >= 6]
df_interasct = df[df['TYP_INT'] >= 2]
lat_lon_pairs_intersec = list(zip(list(df_interasct['LATITUDE']), list(df_interasct['LONGITUD'])))
lat_lon_angle = list(zip(list(df_angle['LATITUDE']), list(df_angle['LONGITUD'])))

HeatMap(lat_lon_pairs_intersec).add_to(map)

for i in range(len(lat_lon_angle)):
    folium.CircleMarker(location=lat_lon_angle[i],radius=2).add_to(map)

map

"""**When looking at the map,it is easily seen that Georgia has the most distribution in Georgia where already happened the most accident cases when comparing to other 3 states. Overall, the accident cases was distributed as the same as density in 4 states. That means the number of car accident usually happened in this region in 2019.**"""

states_by_accident = df_region['STATENAME'].value_counts()
states_by_accident

states_by_accident.plot(kind='barh')

cities_by_accident = df_region['COUNTYNAME'].value_counts()
cities_by_accident

"""**Here's the finding of the counties in 4 states which have the most accident cases in 4 states including Fulton, Jefferson, Dekalb, and Mobile are the top 4 places have the highest number of cases but they are in the same state Georgia, as we knew in the map distribution said that Georgia also shows the most dense of car accident.**"""

cities_by_accident[:20].plot(kind='barh')

"""**This is the bar chart shows clearly the top counties has the high number of accident case in Tennesse, Mississippi, Alabama, and Georgia.**"""

cities_by_accident[cities_by_accident == 1].value_counts()

"""**There are 24 cities that have repoted just one accident (need to investigate)**"""

high_accident_cities = cities_by_accident[cities_by_accident >= 100]
low_accident_cities = cities_by_accident[cities_by_accident < 100]

len(high_accident_cities) / len('COUNTYNAME')

"""**Less than 10% of cities have more than 100 car accidents**

# **Visualizations**
"""

df['MONTHNAME'].value_counts().nlargest(40).plot(kind='bar', figsize=(10,5))
plt.title("Number of accidents by month")
plt.ylabel('Number of accidents')
plt.xlabel('Month');

"""**The bar chart tells about the number of accidents by month, it is seen that May and August was highlighted. These two months in the summer may be a time for traveling.**"""

df['DAY_WEEKNAME'].value_counts().nlargest(40).plot(kind='bar', figsize=(10,5))
plt.title("Number of accidents by day of the week")
plt.ylabel('Number of accidents')
plt.xlabel('Day of the Week');

"""**We can obviously see Saturday and Friday are the highest accidents occur in weekday. Easily to understand these 2 weekend day is a spare time for people to relax, party, and travel after the work.**"""

df.HOUR

df.HOUR = pd.to_datetime(df.HOUR)

fig, ax = plt.subplots(figsize=(30, 5))
sns.distplot(df['HOUR'],color="#0398fc", ax=ax)
plt.show()

"""**A high percentage of accidents occur between 6 am to 8 am (probably people in a hurry to get to work).
Next higest percentage is 5 pm to 10 pm.**

**The number of accident mostly occurred in highway**
"""

sns.countplot(df['DRUNK_DR'])

"""**I tried to figure out the causes by accident. One of the first factors I want to expose is DRUNK but this bar chart was surprising as it shows the number of 0 people got drunk when driving is highest.**

**Next factor is to consider about WEATHER, however, it doesn't matter because there are no more accidents in raining or cloudy day.**

**Both urban and rural areas has the same likelihood in the car accident cases.**
"""

df.HARM_EVNAME.value_counts().nlargest(15).plot(kind='bar', figsize=(10,5))
plt.title("Number of fatal cases by different reasons")
plt.ylabel('FATALS')
plt.xlabel('HARM_EVNAME');

"""**As the same with my first assumptions, the causes of fatality is the fact that people use motor vehicle has the highest number of accidents rather other reasons such as pedestrian, ditch, ect.**

###  Correlations  <a class="anchor" id="Correlations"></a>
"""

#Finding missing colunm to fulfill the dataset
missing_columns = []
sample_df = df
for i in range(len(sample_df.dtypes)): 
  if sample_df.dtypes[i] != "int64":
    missing_columns.append(sample_df.columns[i])

sample_df = df.drop(columns = list(missing_columns))

for col in sample_df: 
  if len(sample_df[col].unique()) <= 1: 
    missing_columns.append(col)

missing_columns.append("ST_CASE")
missing_columns.append("STATE")
missing_columns.append("YEAR")

df_processed = df.drop(columns = list(missing_columns))

numerics = ['int16', 'int32', 'int64']
dfnums=df_processed.select_dtypes(include=numerics)
dfnums.corr()

sns.set (rc = {'figure.figsize':(30, 15)})
sns.heatmap(dfnums.corr(),vmin=.5)
plt.show()

"""##  Build Model <a class="anchor" id="BuildModel"></a>


Classification Modeling focused on Fatalities model by:  PERSONS, Urban/Rural, TYPE/INTER

**Model descriptions** - Interpretation of the model I have used. 
I used the K neighbour classifier:
The k-nearest neighbors classifier is a machine learning algorithm used for classification tasks. It works by comparing the features of a new data point to the features of its k nearest neighbors in a training dataset. The class label of the majority of the k neighbors is then assigned to the new data point. The value of k can be chosen by the user and determines the level of complexity of the classifier. The k-nearest neighbors classifier can be used for both binary and multi-class classification tasks, and is known for its simplicity and interpretability.
"""

Y=df_region['FATALS'].copy()
Y

X=df_region[['PERSONS','RUR_URB','TYP_INT']].copy()
X

plt.scatter(X['PERSONS'],Y)

"""This scatterplot shows the correlation between people involved in an accident and the fatalities that occurred. The data seems to be fairly evenly distributed """

plt.scatter(X['RUR_URB'],Y)

"""This scatterplot should the correlation between urban and rural accidents in which fatalities also occured. """

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.16, random_state=1)



numNeighbors = [1,2,3,4,5,6,7,8,9,10]
trainAcc = []
testAcc = []

for k in numNeighbors:
    clf = KNeighborsClassifier(n_neighbors=k, metric='minkowski', p=2)
    clf.fit(X_train, Y_train)
    Y_predTrain = clf.predict(X_train)
    Y_predTest = clf.predict(X_test)
    trainAcc.append(accuracy_score(Y_train, Y_predTrain))
    testAcc.append(accuracy_score(Y_test, Y_predTest))

plt.plot(numNeighbors, trainAcc, 'ro-', numNeighbors, testAcc,'bv--')
plt.legend(['Training Accuracy','Test Accuracy'])
plt.xlabel('Number of neighbors')
plt.ylabel('Accuracy')

"""I compared the type of intersection, the amount of people involved in an accident, and then whether the accident happened in an urban or rural area with the number of fatalities that occured during an accident. The graph came out unreliable as the test and training accuracies crossed which shows underfitting within the data. The graph is also overfit between 5 and 9 neighbors before leveling out at 9 neighbors. 

"""

Y=df_region['FATALS'].copy()
Y

X=df_region[['PERSONS','RUR_URB','LGT_COND']].copy()
X

plt.scatter(X['PERSONS'],Y)

plt.scatter(X['RUR_URB'],Y)

plt.scatter(X['LGT_COND'],Y)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.16, random_state=1)

numNeighbors = [1,2,3,4,5,6,7,8,9,10]
trainAcc = []
testAcc = []

for k in numNeighbors:
    clf = KNeighborsClassifier(n_neighbors=k, metric='minkowski', p=2)
    clf.fit(X_train, Y_train)
    Y_predTrain = clf.predict(X_train)
    Y_predTest = clf.predict(X_test)
    trainAcc.append(accuracy_score(Y_train, Y_predTrain))
    testAcc.append(accuracy_score(Y_test, Y_predTest))

plt.plot(numNeighbors, trainAcc, 'ro-', numNeighbors, testAcc,'bv--')
plt.legend(['Training Accuracy','Test Accuracy'])
plt.xlabel('Number of neighbors')
plt.ylabel('Accuracy')

"""This would be an example of a more reliable k nearest neighbors graph. For this, I compared people involved in an accident with whether the accident occured in a rural vs. urban area and the light conditions involved in the accident. The accuracy stays constent after 6 neighbors. 



## Resources and References
*What resources and references have you used for this project?*
📝
 https://www.nhtsa.gov/traffic-records/state-data-information-resources
https://stackoverflow.com/questions/56686420/kotlin-kclass-from-ktype
https://docs.w3cub.com/kotlin/api/latest/jvm/stdlib/kotlin.reflect/-k-classifier
https://doc.arcgis.com/en/arcgis-solutions/11.0/reference/introduction-to-traffic-crash-analysis.htm#:~:text=Traffic%20Crash%20Analysis%20can%20be,serious%20and%20fatal%20crashes%20occur.
"""



# ⚠️ Make sure you run this cell at the end of your notebook before every submission!
!jupyter nbconvert --to python source.ipynb