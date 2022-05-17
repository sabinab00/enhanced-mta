#!/usr/bin/env python
# coding: utf-8

# In[23]:


import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
from sklearn.cluster import KMeans

data = pd.read_csv('NYPD dataset.csv')

data


# In[25]:


data = data[data.BORO_NM != 'BRONX']
data = data[data.BORO_NM != 'BROOKLYN']
data = data[data.BORO_NM != 'QUEENS']
data = data[data.BORO_NM != 'STATEN ISLAND']
data = data.dropna()

data


# In[30]:


column_long = data["Longitude"]
max_value = column_long.max() 
print("long max", max_value)


min_value = column_long.min() 
print("long min", min_value)


# In[31]:


column_lat = data["Latitude"]
max_val_lat = column_lat.max() 
print("lat max", max_val_lat)

min_val_lat = column_lat.min()
print("lat min", min_val_lat)


# In[41]:


plt.scatter(data['Longitude'],data['Latitude'])

plt.xlim(-74.04,-73.9)
plt.ylim(40.65,40.9)
plt.show()


# In[42]:


x = data.iloc[:,8:10] # 1t for rows and second for columns
x


# In[47]:


kmeans = KMeans(5)
kmeans.fit(x)


# In[48]:


clusters = kmeans.fit_predict(x)
clusters


# In[49]:


data_with_clusters = data.copy()
data_with_clusters['Clusters'] = clusters 
plt.scatter(data_with_clusters['Longitude'],data_with_clusters['Latitude'],c=data_with_clusters['Clusters'],cmap='rainbow')


# In[50]:


wcss=[]
for i in range(1,10):
    kmeans = KMeans(i)
    kmeans.fit(x)
    wcss_iter = kmeans.inertia_
    wcss.append(wcss_iter)

number_clusters = range(1,10)
plt.plot(number_clusters,wcss)
plt.title('The Elbow title')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')


# In[55]:


pip install kneed


# In[59]:


from kneed import KneeLocator
k1 = KneeLocator(range(1, 10), wcss, curve="convex", direction="decreasing")
k1.elbow


# In[66]:


kmeans = KMeans(3)
kmeans.fit(x)
clusters = kmeans.fit_predict(x)

data_with_clusters = data.copy()
data_with_clusters['Clusters'] = clusters 
plt.scatter(data_with_clusters['Longitude'],data_with_clusters['Latitude'],c=data_with_clusters['Clusters'],cmap='autumn')


# In[70]:


from collections import Counter

cluster_labels = kmeans.fit_predict(x)
cluster_counts = Counter(cluster_labels)

print(cluster_counts)


# In[90]:


from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters = 3)
kmeans.fit(x)
y_kmeans = kmeans.predict(x)

plt.scatter(data_with_clusters['Longitude'],data_with_clusters['Latitude'], c=y_kmeans, cmap='viridis')

centers = kmeans.cluster_centers_
print (centers)
#plt.scatter(centers[:, 0], centers[:, 1], c='black', alpha=0.5);
                


# In[ ]:




