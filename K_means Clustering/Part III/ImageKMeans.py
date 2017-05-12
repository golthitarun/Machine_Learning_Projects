
# coding: utf-8

# In[2]:

import numpy as np
import cv2
import sys


# In[3]:

K_value = int(sys.argv[1])
input_file = sys.argv[2]
output_file = sys.argv[3]
img = cv2.imread(input_file)
Z = img.reshape((-1,3))


# In[3]:

Z = np.float32(Z)


# In[4]:

#Here the criteria defines the argument we want to pass to the open_cv 
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

#Run open_cv kmeans method to cluster the given image.
ret,label,center=cv2.kmeans(Z,K_value,criteria,10,cv2.KMEANS_RANDOM_CENTERS)


# In[5]:

center = np.uint8(center)
res = center[label.flatten()]
img_out = res.reshape((img.shape))

#This will save the output to a file
cv2.imwrite(output_file,img)

#This will show the clustered image in a window
cv2.imshow('image',img_out)
cv2.waitKey(0)
cv2.destroyAllWindows()


# In[ ]:



