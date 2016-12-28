from cv2 import *
import numpy as np
from matplotlib import pyplot as plt
import math
import time


threshold=0.6
input_img="coins.jpg"



img=imread(input_img,0)
shape=img.shape
if max(shape[0],shape[1])[0]>400:
        shape=(img.shape[0]/2,img.shape[1]/2)
img1=imread(input_img)
img2=imread(input_img)
img=resize(img,(shape[1],shape[0]))
img1=resize(img1,(shape[1],shape[0]))
img2=resize(img2,(shape[1],shape[0]))

gauss=GaussianBlur(img,(9,9),0)
canny=Canny(gauss,75,150)
radius=int(max(shape[0],shape[1])[0])/2
image=canny
rows=img.shape[0]
cols=img.shape[1]
max_val=0
accumulator=np.zeros((radius,rows,cols))


for r in range(10,radius):
	for m in range(rows):
		for n in range(cols):
			if image[m][n]==255:
				theta=0
				for theta in range(0,360,10):
					x0=int(m-r*math.cos(theta*math.pi/180))
					y0=int(n-r*math.sin(theta*math.pi/180))
					if x0>0 and x0<rows and y0>0 and y0<cols:
						#print (x0),(y0)
						accumulator[r][x0][y0]+=1
	print "Radius="+str(r)


csize=30

max_pool=np.zeros((radius,csize,csize))
max_val=np.amax(accumulator)

for r in range(10,radius):
        accumulator[r]=accumulator[r]/max_val


for i in range(0,rows-csize,csize):
        for j in range(0,cols-csize,csize):
                max_pool[:,:,:]=1
                max_pool=accumulator[:,i:i+csize,j:j+csize]*max_pool
                max_val=np.where(max_pool==max_pool.max())
                r = max_val[0][0]
                x = max_val[1][0]       
                y = max_val[2][0]
                if max_pool.max()>threshold:
                        accumulator[:,i:i+csize,j:j+csize]=accumulator[:,i:i+csize,j:j+csize]/accumulator[r][x+i][y+j]
                        for r in range(10,radius):
                                for q in range(i,i+csize):
                                        for w in range(j,j+csize):
                                                if accumulator[r][q][w]>0.9:
                                                        circle(img1,(w,q),r,(0,255,0),2)



imshow("Original image",img2)
imshow("Gaussian Image",gauss)
imshow("Canny Edge detected image",canny)
imshow("Circle Detected Image",img1)

waitKey(0)
destroyAllWindows()
