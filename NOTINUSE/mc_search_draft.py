#!/usr/bin/env python
# coding: utf-8

# In[28]:


import NYCT


# In[29]:


g = Graph()
g.generateTransfers()
g.generateStops('subway',0)
g.generateStopNames()
g.generateRoutes('subway',0)
g.mapStopTransfers()
g.connectStops() 


# In[44]:


#euclidean distance heuristic
from scipy.spatial import distance
def euclidean(origin,destination):
    return distance.euclidean(tuple(origin.geocode),tuple(destination.geocode))


#transfers heuristic
def transfers(test,dest):
    count=1
    if test.route_id in dest:
        count=0
    return count


# In[59]:


origin=g.getStop("2")
destination=g.getStop("0")
dest=[destination.stop_id]
trans=destination.transfers
if trans!=None:
    for t in trans:
        dest.append(t.stop_id)


# In[60]:


visited=set()
frontier=[]
test=origin
goal=dest
state='na'


# In[51]:


#uptown
while state!="goal":
    if test.stop_id in goal:
        state="goal"
        print(test)
        break
    else:
        visited.add(test)
        children=[test.child]
        if test.transfers!=None:
            for t in test.transfers:
                children.append(t)
    
        for i in children:
            if i not in visited and i!=None:
                frontier.append((i,euclidean(i,destination)+transfers(i,dest)))
        frontier.sort(key=lambda x:(x[1]),reverse=True)
        test=frontier.pop()[0]


# In[61]:


#downtown
while state!="goal":
    if test.stop_id in goal:
        state="goal"
        print(test)
    else:
        visited.add(test)
        children=[test.parent]
        if test.transfers!=None:
            for t in test.transfers:
                children.append(t)
    
        for i in children:
            if i not in visited and i!=None:
                frontier.append((i,euclidean(i,destination)+transfers(i,dest)))
        frontier.sort(key=lambda x:(x[1]),reverse=True)
        test=frontier.pop()[0]


# In[ ]:




