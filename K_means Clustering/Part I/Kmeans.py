
#author : Tharunn, Shiva

# In[1]:

import numpy as np
import pandas as pd
from random import uniform
import sys


# In[2]:

#Method used to assign the points to their clusters.
def find_closest_centroid():
    cluster.clear()
    cluster_id.clear()
    for j in range(0,k):
        cluster[j]=[]
        cluster_id[j]=[]
    for i in range(len(data)):
        b = np.array((data['x'][i],data['y'][i]))
        Id = data['id'][i]
        minimum = sys.float_info.max
        for j in range(0,k):
            a= np.array(centroids[j])
            dist = np.linalg.norm(a - b)
            if dist < minimum:
                dst = dist
                cluster_pt = j
                minimum = dist
        cluster[cluster_pt].append((data['x'][i],data['y'][i]))
        cluster_id[cluster_pt].append(Id)


# In[3]:

#Method used to update centroids
def update_centroid():
    for i in range(0,k):
        sum_x = 0
        sum_y = 0
        for pt in cluster[i]:
            sum_x +=pt[0]
            sum_y +=pt[1]
        try:
            centroids[i] = ((sum_x/len(cluster[i])),(sum_y/len(cluster[i])))
        except:
            continue


# In[4]:

#MEthod used to find the Error
def SSE():
    SSE = 0
    for i in range(0,k):
        c = np.array(centroids[i])
        for pt in cluster[i]:
            p = np.array(pt)
            dist = np.linalg.norm(c - p)
            SSE = SSE + dist*dist
    return SSE


# In[5]:

#Method used to display the output
def output():
    for i in range(0,k):
        print 'cluster =',i,'-> Points =',
        for Id in cluster_id[i]:
            print Id,',',
        print   


# In[6]:

#Method used to write the output to a file.
def file_out(error,output_file):
    f = open(output_file,'w')
    for i in range(0,k):
        print >>f,'cluster =',i,'-> Points =',
        for Id in cluster_id[i]:
            print >>f,Id,',',
        print >>f
    print >>f,'The SSE is =',error


# In[23]:

k = int(sys.argv[1])
input_file = sys.argv[2]
data = pd.read_csv(input_file,sep = '\t')

output_file = sys.argv[3]
centroids = []
for i in range(k):
    centroids.append((uniform(0,1),uniform(0,1)))
cluster = {}
cluster_id = {}

#Loop to find the best possible clusters.
for i in range(0,25):
    Flag = True
    prev_centroids = centroids[:]
    find_closest_centroid()
    update_centroid()
    
    for j in range(0,k):
        if (centroids[j][0] != prev_centroids[j][0]) or (centroids[j][1] != prev_centroids[j][1]):
            Flag = False
            break
            
    if Flag == True:
        break
Error = SSE()
output()
print 'The SSE is =',Error
file_out(Error,output_file)






