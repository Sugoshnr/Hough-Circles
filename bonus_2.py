import cv2
import numpy
from random import randint
import math
import sys

Tf = 1000000
Td = 2.5
Tr = 0.8
Ta = 2
Tmin = 50

def Dist(x1,y1,x2,y2):
	dist = (math.sqrt( (x1-x2)**2 + (y1-y2)**2 ))
	return dist


def Get4RandomPoints(edgesSet):
		
	p1 = randint(0,len(edgesSet[1])-1)
	x1 = edgesSet[0][p1]
	y1 = edgesSet[1][p1]
	del edgesSet[0][p1]
	del edgesSet[1][p1]

	p2 = randint(0,len(edgesSet[1])-1)
	x2 = edgesSet[0][p2]
	y2 = edgesSet[1][p2]
	del edgesSet[0][p2]
	del edgesSet[1][p2]

	p3 = randint(0,len(edgesSet[1])-1)
	x3 = edgesSet[0][p3]
	y3 = edgesSet[1][p3]
	del edgesSet[0][p3]
	del edgesSet[1][p3]

	p4 = randint(0,len(edgesSet[1])-1)
	x4 = edgesSet[0][p4]
	y4 = edgesSet[1][p4]
	del edgesSet[0][p4]
	del edgesSet[1][p4]

	t1 = (x2 - x1) * (y3 - y1)
	t2 = (x3 - x1) * (y2 - y1)

	t3 = (x3 - x2) * (y4 - y2)
	t4 = (x4 - x2) * (y3 - y2)

	d1 = Dist(x1,y1,x2,y2)
	d2 = Dist(x2,y2,x3,y3)
	d3 = Dist(x3,y3,x1,y1)
	


	if t1 == t2 or t3==t4 or d1 < Ta or d2 < Ta or d3 < Ta:
		
		edgesSet[0].append(x1)
		edgesSet[1].append(y1)

		edgesSet[0].append(x2)
		edgesSet[1].append(y2)

		edgesSet[0].append(x3)
		edgesSet[1].append(y3)

		edgesSet[0].append(x4)
		edgesSet[1].append(y4)

		return Get4RandomPoints(edgesSet)


	return edgesSet,x1,y1,x2,y2,x3,y3,x4,y4




def GetCircle(edgesSet,img):
		
	for i in range(Tf):


		edgesSet,x1,y1,x2,y2,x3,y3,x4,y4 = Get4RandomPoints(edgesSet) #Get Non Collinear Points p1,p2,p3,p4

		if len(edgesSet[0]) < Tmin:
			break
		a = x1**2 + y1**2
		b = x2**2 + y2**2
		c = x3**2 + y3**2

		term1X = (b-a) * 2 * (y3 - y1)
		term2X = (c-a) * 2 * (y2 - y1)

		term1Y = (c-a) * 2 * (x2-x1)
		term2Y = (b-a) * 2 * (x3-x1)

		den = 4 * ( ((x2 - x1) * (y3 - y1)) - ((x3 - x1) * (y2 - y1)) )


		cx = (term1X - term2X) / den
		cy = (term1Y - term2Y) / den
		print x1,cx,y1,cy
		r = math.sqrt((x1 - cx)**2 + (y1 - cy)**2)
		
		
		d4 = math.sqrt( (x4-cx)**2 + (y4-cy)**2 )

		diff = abs(d4 - r)
		
		pointsToRemove = []
		pointsToAdd = []
		if diff < Td:
			np = 0
			Tp = 2 * math.pi * r * Tr
			for j in range(len(edgesSet[0])):
				x = edgesSet[0][j]
				y = edgesSet[1][j]
				diff2 = abs(Dist(x,y,cx,cy) - r)
				if diff2 < Td:
					np += 1
					pointsToRemove.append(j)

			if(np > Tp and r > 20):
				
				for j in sorted(pointsToRemove, reverse=True):
					del edgesSet[0][j]
					del edgesSet[1][j] 
				
				cv2.circle(img,(cy,cx),int(r),(0,255,0),2)
				
				#cv2.imshow('Circle',img)
				c#v2.waitKey(0)
			else:
				edgesSet[0].append(x1)
				edgesSet[1].append(y1)

				edgesSet[0].append(x2)
				edgesSet[1].append(y2)

				edgesSet[0].append(x3)
				edgesSet[1].append(y3)

				edgesSet[0].append(x4)
				edgesSet[1].append(y4)
		else:
			edgesSet[0].append(x1)
			edgesSet[1].append(y1)

			edgesSet[0].append(x2)
			edgesSet[1].append(y2)

			edgesSet[0].append(x3)
			edgesSet[1].append(y3)

			edgesSet[0].append(x4)
			edgesSet[1].append(y4)



img = cv2.imread('HoughCircles.jpg',0)



show = True


if show:
	cv2.imshow('Original Image',img)
	cv2.waitKey()


img = cv2.GaussianBlur(img,(3,3),0)

if show:
	cv2.imshow('Gaussian Blur',img)
	cv2.waitKey()

edges = cv2.Canny(img,90,200)

if show:
	cv2.imshow('Edges Detected',edges)
	cv2.waitKey()

rows,cols = img.shape
minRadius = 10
maxRadius = min(rows,cols) / 2

edges = cv2.threshold(edges,200,1,cv2.THRESH_BINARY)[1]

edgesSet = list(numpy.where(edges == 1))

edgesSet[0] = list(edgesSet[0])
edgesSet[1] = list(edgesSet[1])	

print "It takes around 4-5 mins to see the results. Thanks for your patience"
GetCircle(edgesSet,img)
cv2.imshow('Circles Detected',img)
cv2.waitKey()















