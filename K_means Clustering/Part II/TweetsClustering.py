
# coding: utf-8

# In[82]:

import pandas as pd
import numpy as np
import sys


# In[83]:

# Method used to find the distance of each point from cluster points and assign the points to nearest cluster.
def jaccard_distance(row):
    txt = row['text']
    id1 = row['id']
    txt = set(txt.split())
    minimum = sys.float_info.max
    for ids in seeds2:
        text =  data['text'][np.where(data['id'] == int(ids))[0]]
        text = set(str(text).split())
        union  = txt.union(text)
        intersec = txt.intersection(text)
        jd = 1 -(float(len(intersec))/float(len(union)))
        if(jd < minimum):
            minimum = jd
            min_seed = ids
    seeds_dict[min_seed].append(id1)
        
        
        
    


# In[84]:

# Helper method used to find the avg distance to find the next best centroid for the cluster.
def get_avg(cluster,value):
    sum = 0
    txt = data['text'][np.where(data['id'] == int(value))[0]]
    txt = set(str(txt).split())
    for i in seeds_dict[cluster]:
        text = data['text'][np.where(data['id'] == int(i))[0]]
        text = set(str(text).split())
        union  = txt.union(text)
        intersec = txt.intersection(text)
        sum = sum + (1 -(float(len(intersec))/float(len(union))))
    return sum/len(seeds_dict[cluster])
        


# In[85]:

#Method used to update the centroids
def update_centroids():
    for i in range(0,len(seeds2)):
        min2 = sys.float_info.max
        for j in seeds_dict[seeds2[i]]:
            avg = get_avg(seeds2[i],j)
            if avg < min2:
                min2 = avg
                min_cluster = j
        seeds2[i]=min_cluster
        


# In[86]:

#Method used to find the Error.
def SSE():
    error = 0
    for i in seeds2:
        centroid_txt = data['text'][np.where(data['id'] == int(i))[0]]
        centroid_txt = set(str(centroid_txt).split())
        for j in seeds_dict[int(i)]:
            point_txt = data['text'][np.where(data['id'] == int(j))[0]]
            point_txt = set(str(point_txt).split())
            union  = centroid_txt.union(point_txt)
            intersec = centroid_txt.intersection(point_txt)
            error = error + (1 -(float(len(intersec))/float(len(union))))**2
    return error
    


# In[87]:

#Method used to display the output
def display():
    for i in seeds2:
        print "cluster_id:",i,"-> Tweet_ids:",
        for j in seeds_dict[i]:
            print j,',',
        print


# In[1]:

#Method used to write the output to a File.
def file_out(error,output_file):
    f = open(output_file,'w')
    for i in seeds2:
        print >>f
        print >>f,"cluster_id:",i,"-> Tweet_ids:",
        for j in seeds_dict[i]:
            print >>f, j,',',
        print >>f
    print >>f,'The SSE is =',error    
    
    


# In[89]:


input_file = sys.argv[2]
seed_file = sys.argv[1]
output_file = sys.argv[3]

data = pd.read_json(input_file,lines = True)
with open('Tweets.json', 'rb') as f:
    data2 = f.readlines()
data2 = map(lambda x : x.strip(), data2)
seeds_dict = {}
with open(seed_file,'rb') as f:
    seeds2 = f.readlines()
seeds2 = map(lambda x : x.strip(',\n'),seeds2)
seeds = pd.read_csv('InitialSeeds.txt',header = None)
del seeds[1]

#Loop to find the best possible clusters.
for i in range(0,25):
    Flag = True
    seeds_dict.clear()
    for i in seeds2:
        seeds_dict[i] = []
    prev_centroids = seeds2[:]
    data.apply(jaccard_distance, axis =1, raw=True)
    update_centroids()
    for j in range(0,len(seeds2)):
        if (seeds2[j] != prev_centroids[j]):
            Flag = False
            break
    if Flag == True:
        break
        
    


# In[90]:

display()
error = SSE()
print 'The SSE is =',error


# In[81]:

file_out(error,output_file)


# In[ ]:



