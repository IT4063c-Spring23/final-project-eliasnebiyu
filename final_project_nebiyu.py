# -*- coding: utf-8 -*-
"""Final project Nebiyu.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Jv-LRhRJ91qiBlOlSZmExw_fLkZrCEvu

# **Exploratory Data Analysis**

# 1. Determine Business Objectives and Assess the Situation  <a class="anchor" id="Businessunderstanding"></a>

## 1.1 Assess the Current Situation<a class="anchor" id="Assessthecurrentsituation"></a>

### 1.1.1. Inventory of resources <a class="anchor" id="Inventory"></a>
List the resources available to the project including:
- Name: **Nebiyu Elias Tadesse**
- Data: **NHTSA for the State of Tennesse, Mississippi, Alabama, and Georgia**
- Computing resources: **Personal Computer**
- Software: **Python and associated libraries as needed**

### 1.1.2. Requirements, assumptions and constraints - <a class="anchor" id="Requirements"></a> 
- Requirements of the project including the schedule of completion
  **COMPLETE and PRESENT FINDINGS AS DIRECTED BY ASSIGNMENT**
- Data security concerns as well as any legal issues. 
  **PUBLIC INFORMATION WITH ANOMINIZATION**
- Assumptions made by the project. These may be assumptions about the data that can be verified during data mining, but may also include non-verifiable assumptions about the business related to the project. It is particularly important to list the latter if they will affect the validity of the results. 
  **My assumption is that the dataset will definitely be messy and unclear with the attributes. Especially the data value columns are not understandable so it's really hard to explore and understand the dataset**
  **For exploring the data, my first assumptions are the main reason caused by accidents and fatals is people use their motor vehicle. Second assumption is that these factors including DRUNK, WEATHER, people go out to travel, party in the weekend which are the main factors caused by accidents when using vehicle.**
- List the constraints on the project. 
  **It's a bit difficult understand the data, it took me a considerable amount of time to absorb it. The value attribute is not clear so it's also difficult to find put the metrics to identify the reasons of accidents and risks**

### 1.1.5.Costs and benefits  <a class="anchor" id="CostBenefit"></a>
- Construct a cost-benefit analysis for the project which compares the costs of the project with the potential benefits to the business if it is successful. This comparison should be as specific as possible. For example, you should use financial measures in a commercial situation. 

  **TRAFFIC ACCIDENT ANALYSIS WILL ALLOW EDUCATION OF THE PUBLIC, INFORM AUTHORITIES OF TRENDS, AND ALLOW FASTER FIRST RESPONDER INITIATION**

## 1.3 What Questions am I Trying To Answer? <a class="anchor" id="QA"></a>
 - How many people are involved in accidents?
 - Are there more accidents in cloudy or raining areas?
 - Which states have the highest number of accidents?
 - Among the top 100 cities in number of accidents, which states do they belong to most frequently?
 - What time of the day are accidents most frequent in?
 - Which days of the week have the most accidents?
 - Are more accidents prevalent when people get drunk?

**Business success criteria**
- PREVENTION AND AVOIDANCE OF FUTURE ACCIDENTS
- FASTER RESPONSE TIME TO ACCIDENTS
- ESTIMATE HOW MANY ACCIDENTS WITH THE RESULT OF DRUNK
- IMPROVE THE ARRIVAL TIME OF HOSPITAL



**Data mining success criteria**
- DATA CAN BE USED IN FURTHER MODELING TECHNIQUES TO CLASSIFY AND CLUSTER ACCIDENTS IN MULTIPLE PERSPECTIVES


**Produce project plan - **
- **LAYOUT YOUR BASIC PLAN FOR THIS ANALYSIS**
-  Understanding data
    
- Identifying the problems that we want to solve and metrics that we want to figure out.
- Data preparaion
- Visualizations
- Evaluation
- Deployment
- Classification Analysis
- Cluster Analysis

# 2. Data Understanding & Exploratory Data Analysis <a class="anchor" id="Dataunderstanding"></a>
The second stage of the CRISP-DM process requires you to acquire the data listed in the project resources. This initial collection includes data loading, if this is necessary for data understanding. For example, if you use a specific tool for data understanding, it makes perfect sense to load your data into this tool. If you acquire multiple data sources then you need to consider how and when you're going to integrate these.

## 2.1 Initial Data Report <a class="anchor" id="Datareport"></a>
Initial data collection report - 
List the data sources acquired together with their locations, the methods used to acquire them and any problems encountered. Record problems you encountered and any resolutions achieved. This will help both with future replication of this project and with the execution of similar future projects.
"""

# Commented out IPython magic to ensure Python compatibility.
# Import Libraries Required
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
import numpy as np
import seaborn as sns

"""## 2.2 Describe Data <a class="anchor" id="Describedata"></a>
Data description report - Describe the data that has been acquired including its format, its quantity (for example, the number of records and fields in each table), the identities of the fields and any other surface features which have been discovered. Evaluate whether the data acquired satisfies your requirements.
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

"""**There are totally 2814 accident cases happened in 4 states in 2019.**"""

df_region.columns

df_region.describe()

df_region.info()

"""## 2.3 Verify Data Quality <a class="anchor" id="Verifydataquality"></a>
This step is to transform the data including find out any errors, missing data. As you can see there is no empty dataset as it was tidy data. So, dataset is good to continue exploring and doing visualizations.

### 2.3.1. Missing Data <a class="anchor" id="MissingData"></a>
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

import folium
from folium.plugins import HeatMap
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

"""**Less than 10% of cities have more 100 car accidents**

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

""" **A high percentage of accidents occur between 6 am to 8 am (probably people in a hurry to get to work).
Next higest percentage is 5 pm to 10 pm.**
"""

fig, ax = plt.subplots(figsize=(30, 5))
sns.countplot(df['ROUTENAME'],color="#0398fc", ax=ax)
plt.show()

"""**The number of accident mostly occurred in highway**"""

sns.countplot(df['DRUNK_DR'])

"""**I tried to figure out the causes by accident. One of the first factors I want to expose is DRUNK but this bar chart was surprising as it shows the number of 0 people got drunk when driving is highest.**

**Next factor is to consider about WEATHER, however, it doesn't matter because there are no more accidents in raining or cloudy day.**
"""

sns.countplot(df['RUR_URBNAME'])

"""**Both urban and rural areas has the same likelihood in the car accident cases.**"""

df.HARM_EVNAME.value_counts().nlargest(15).plot(kind='bar', figsize=(10,5))
plt.title("Number of fatal cases by different reasons")
plt.ylabel('FATALS')
plt.xlabel('HARM_EVNAME');

"""**As the same with our first assumptions, the causes of fatal is the fact that people use motor vehicle has the highest number of accidents rathan other reasons such as pedestrian, ditch, ect.**"""

plt.figure(figsize=[20,8])
sns.distplot(df.PERSONS, kde=True)
#sns.distplot(sales_data.PriceReg, kde=True)

"""**It helped us to answer abouhow many people are involved in an accident.**"""

sns.countplot(df['FATALS'])

"""**1 death occurred moslty in all the accident cases in 2019.**"""

#one_person_fatal = df_region['FATALS']
#one_person_fatal
#one_person_fatal[one_person_fatal == 1]

"""### 2.3 Correlations  <a class="anchor" id="Correlations"></a>

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

"""# **Classification Analysis**

#  Modelling <a class="anchor" id="Modelling"></a>

Classification Modeling focused on Fatalities model by:  PERSONS, Urban/Rural, TYPE/INTER

## 3. Build Model <a class="anchor" id="BuildModel"></a>
Run the modelling tool on the prepared dataset to create one or more models.

**Parameter settings** - With any modelling tool there are often a large number of parameters that can be adjusted. List the parameters and their chosen values, along with the rationale for the choice of parameter settings.

**Models** - These are the actual models produced by the modelling tool, not a report on the models.

**Model descriptions** - Describe the resulting models, report on the interpretation of the models and document any difficulties encountered with their meanings.
"""

Y=df_region['FATALS'].copy()
Y

X=df_region[['PERSONS','RUR_URB','TYP_INT']].copy()
X

plt.scatter(X['PERSONS'],Y)

"""This scatterplot shows the correlation between people involved in an accident and the fatalities that occurred. The data seems to be fairly evenly distributed """

plt.scatter(X['RUR_URB'],Y)

"""This scatterplot should the correlation between urban and rural accidents in which fatalities also occured. """

plt.scatter(X['TYP_INT'],Y)

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.16, random_state=1)

# Commented out IPython magic to ensure Python compatibility.
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
# %matplotlib inline

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

"""We compared thew type of intersection, the amount of people involved in an accident, and then whether the accident happened in an urban or rural area with the number of fatalities that occured during an accident. The graph came out unreliable as the test and training accuracies crossed which shows underfitting within the data. The graph is also overfit between 5 and 9 neighbors before leveling out at 9 neighbors. This may be caused by missing data or data that was input incorrectly. """

Y=df_region['FATALS'].copy()
Y

X=df_region[['PERSONS','RUR_URB','LGT_COND']].copy()
X

plt.scatter(X['PERSONS'],Y)

plt.scatter(X['RUR_URB'],Y)

plt.scatter(X['LGT_COND'],Y)

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.16, random_state=1)

# Commented out IPython magic to ensure Python compatibility.
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
# %matplotlib inline

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

"""This would be an example of a more reliable k nearest neighbors graph. For this, we compared persons involved in an accident with whether the accident occured in a rural vs. urban area and the light conditions involved in the accident. The accuracy stays constent after 6 neighbors.

## 4. Assess Model <a class="anchor" id="AssessModel"></a>
Interpret the models according to your domain knowledge, your data mining success criteria and your desired test design. Judge the success of the application of modelling and discovery techniques technically, then contact business analysts and domain experts later in order to discuss the data mining results in the business context. This task only considers models, whereas the evaluation phase also takes into account all other results that were produced in the course of the project.

At this stage you should rank the models and assess them according to the evaluation criteria. You should take the business objectives and business success criteria into account as far as you can here. In most data mining projects a single technique is applied more than once and data mining results are generated with several different techniques. 

**Model assessment** - Summarise the results of this task, list the qualities of your generated models (e.g.in terms of accuracy) and rank their quality in relation to each other.

**Revised parameter settings** - According to the model assessment, revise parameter settings and tune them for the next modelling run. Iterate model building and assessment until you strongly believe that you have found the best model(s). Document all such revisions and assessments.

#  Evaluation <a class="anchor" id="Modelling"></a>

**THIS STAGE SHOULD INCLUDE YOUR CONCLUSIONS WITH THE DATA EXPLORATION BOTH WRITTEN AND GRAPHICAL.  THE POINTS YOU MAKE HERE AND THE VISUALIZATIONS CREATED WILL BE PART OF FUTURE DEPLOYMENT OF THIS ACTION**

# **Cluster Analysis**
"""

# Commented out IPython magic to ensure Python compatibility.
#Import libraries for clustering
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
# %matplotlib inline
import numpy as np
import seaborn as sns
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.neighbors import NearestNeighbors
#https://www.reneshbedre.com/blog/dbscan-python.html

#Average cases per month
cases_month=pd.pivot_table(df,values='ST_CASE',index='MONTHNAME',aggfunc=pd.Series.nunique)
cases_month


#pd.pivot_table(df, values='col1', index='col2', columns='col3',aggfunc=pd.Series.nunique)

"""**Standardize the Latitude and Longitude data for analysis.**"""

df['LATITUDE_ZSCORE']=stats.zscore(df['LATITUDE'])
df['LATITUDE_ZSCORE']

df['LONGITUD_ZSCORE']=stats.zscore(df['LONGITUD'])
df['LONGITUD_ZSCORE']

"""**Plot the standardized locations of accidents.**"""

plt.figure(figsize=(10,10)) 
plt.scatter(df['LONGITUD_ZSCORE'],df['LATITUDE_ZSCORE'])
plt.xlabel('Longitude')
plt.ylabel('Latitiude')
plt.show()

"""**Create the Lat and Long Dataframe for use in clustering.**"""

sns.boxplot(y=df['LATITUDE_ZSCORE'])

sns.boxplot(y=df['LONGITUD_ZSCORE'])

df_lat_long=df[['LONGITUD_ZSCORE','LATITUDE_ZSCORE']].copy()
df_lat_long

plt.figure(figsize=(5,5))
p =sns.scatterplot(data=df_lat_long, x="LONGITUD_ZSCORE", y="LATITUDE_ZSCORE", hue=clusters.labels_, legend="full", palette="deep")
sns.move_legend(p, "upper right", bbox_to_anchor=(1.17, 1.2), title='Clusters')

plt.show()
plt.figure(figsize=(5,5))
plt.scatter(df_lat_long['LONGITUD_ZSCORE'],df_lat_long['LATITUDE_ZSCORE'])

"""The dataset has only 2 clusters, one of which represents an insignificant number of points and is located in a long distance with the rest of data set. Therefore, we will focus on analyzing the bigger cluster at this project. """

Q1 = df_lat_long.quantile(0.25)
Q3 = df_lat_long.quantile(0.75)
IQR = Q3 - Q1
print(IQR)

df_lat_long_out = df_lat_long[~((df_lat_long< (Q1 - 1.5 * IQR)) |(df_lat_long > (Q3 + 1.5 * IQR))).any(axis=1)]
df_lat_long_out.shape

"""**This section will use K-Nearest Negihbors for help define the parameters in the DBSCAN Clustering alogrithm. Vary the number of n_neighbors to discover the "elbow" value where the K-nn distance will be used.**"""

# n_neighbors = 2 as kneighbors function returns distance of point to itself (i.e. first column will be zeros) 
nbrs = NearestNeighbors(n_neighbors=2).fit(df_lat_long_out)
# Find the k-neighbors of a point
neigh_dist, neigh_ind = nbrs.kneighbors(df_lat_long_out)
# sort the neighbor d8stances (lengths to points) in ascending order
# axis = 0 represents sort along first axis i.e. sort along row
sort_neigh_dist = np.sort(neigh_dist, axis=0)

#  for each iteration ensure the distance are set to (n_neighbors-1) k_dist = sort_neigh_dist[:, (n_neighbors-1) ]
k_dist = sort_neigh_dist[:, 1]
plt.plot(k_dist)
plt.axhline(y=0.1, linewidth=1, linestyle='dashed', color='k')
plt.ylabel("k-NN distance")
plt.xlabel("Sorted observations (6th NN)")
plt.show()

"""As the number of clusters are 2 and the k-NN distance is low so it's a good number of neighbors. """

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

silhouette_score_arr = []
k = []

for i in range(2, 10):
  km = KMeans(n_clusters=i, random_state=42)
  km.fit_predict(df_lat_long_out)
  score = silhouette_score(df_lat_long_out, km.labels_, metric='euclidean')
  k.append(i)
  silhouette_score_arr.append(score)
max_score = max(silhouette_score_arr)
max_index = silhouette_score_arr.index(max_score) + 2
print("Maximum silhouetter score is {:.3f} with {} neighbors".format(max_score, max_index))

plt.plot(k, silhouette_score_arr)
plt.title('Silhouetter score by neighbors')
plt.xlabel('Number of neighbors')
plt.ylabel('Silhouetter score')
plt.show()

from collections import Counter
Counter(clusters.labels_)

from sklearn.metrics import silhouette_score
from sklearn.cluster import DBSCAN
# Defining the list of hyperparameters to try
#https://thinkingneuron.com/how-to-create-clusters-using-dbscan-in-python/#:~:text=Finding%20Best%20hyperparameters%20for%20DBSCAN%20using%20Silhouette%20Coefficient,is%20%28b%20%E2%80%93%20a%29%20%2F%20max%20%28a%2C%20b%29.
eps_list=np.arange(start=0.01, stop=0.9, step=0.01)
min_sample_list=np.arange(start=2, stop=5, step=1)
 
# Creating empty data frame to store the silhouette scores for each trials
silhouette_scores_data=pd.DataFrame()
 
for eps_trial in eps_list:
    for min_sample_trial in min_sample_list:
        
        # Generating DBSAN clusters
        db = DBSCAN(eps=eps_trial, min_samples=min_sample_trial)
        
        if(len(np.unique(db.fit_predict(df_lat_long)))>1):
            sil_score=silhouette_score(df_lat_long, db.fit_predict(df_lat_long))
            #print("sil_score", sil_score)
        else:
            continue
        trial_parameters="eps:" + str(eps_trial.round(1)) +" min_sample :" + str(min_sample_trial)
        
        silhouette_scores_data=silhouette_scores_data.append(pd.DataFrame(data=[[sil_score,trial_parameters]], columns=["score", "parameters"]))
print(silhouette_scores_data)
# Finding out the best hyperparameters with highest Score
silhouette_scores_data.sort_values(by='score', ascending=False).head(1)

# Commented out IPython magic to ensure Python compatibility.
clusters = DBSCAN(eps=0.4, min_samples=3).fit(df_lat_long)
# get cluster labels
clusters.labels_
# output
print(clusters.labels_)

#https://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html#sphx-glr-auto-examples-cluster-plot-dbscan-py

core_samples_mask = np.zeros_like(clusters.labels_, dtype=bool)
core_samples_mask[clusters.core_sample_indices_] = True
labels = clusters.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print("Estimated number of clusters: %d" % n_clusters_)
print("Estimated number of noise points: %d" % n_noise_)
print("Homogeneity: %0.3f" % metrics.homogeneity_score(clusters.labels_, labels))
print("Completeness: %0.3f" % metrics.completeness_score(clusters.labels_, labels))
print("V-measure: %0.3f" % metrics.v_measure_score(clusters.labels_, labels))
print("Adjusted Rand Index: %0.3f" % metrics.adjusted_rand_score(clusters.labels_, labels))
print(
    "Adjusted Mutual Information: %0.3f"
#     % metrics.adjusted_mutual_info_score(clusters.labels_, labels)
)
print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(df_lat_long, labels))

plt.figure(figsize=(5,5))
p =sns.scatterplot(data=df_lat_long_out, x="LONGITUD_ZSCORE", y="LATITUDE_ZSCORE", hue=clusters.labels_, legend="full", palette="deep")
sns.move_legend(p, "upper right", bbox_to_anchor=(1.17, 1.2), title='Clusters')

plt.show()
plt.figure(figsize=(5,5))
plt.scatter(df_lat_long_out['LONGITUD_ZSCORE'],df_lat_long_out['LATITUDE_ZSCORE'])