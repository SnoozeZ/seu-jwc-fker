# -*- coding: utf-8 -*-

########################################################################
#           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                   Version 2, December 2004
#
#       Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
#   Everyone is permitted to copy and distribute verbatim or modified
#   copies of this license document, and changing it is allowed as long
#   as the name is changed.
#
#           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#            0. You just DO WHAT THE FUCK YOU WANT TO.
########################################################################

import cv2
import Image
import numpy as np
import pytesser

def findPoints(img, xPos = 0):
	''' Input a ndarray binarized image and set the x coordinate.
		The function would return a list containing the y coordinate of 2 points on the line'''
	points = []
	for i in range(img.shape[0] - 1):
		if img[i,xPos] == 0:
			points.append(i+2)  #more likely to be the mid of the line
			break
	for i in range(img.shape[0] - 1, 0, -1):
		if img[i,xPos] == 0:
			points.append(i-2)
			break
	return points
	
	
def fillLine(img, k, leftPoint):
	''' A trick to process the annoying line.
		Try to change the values below if the result is unsatisfying'''
	for i in range(img.shape[1]):  #left to right
         y = int(leftPoint + k*i)  #along the line
         if img[y,i] == 0:  # is black
			if y+3 >= img.shape[0] or y-3 <= 0:
				img[y,i] = 255
				if y + 1 < img.shape[0]:
					img[y + 1, i] = 230
				if y - 1 >= 0:
					img[y - 1, i] = 230
				continue
			if img[y + 3, i] == 255 and img[y - 3, i] == 255:
#                img[y + 1, i] = 240
#                img[y - 1, i] = 240
				img[y + 2, i] = 250
				img[y - 2, i] = 250
				img[y, i] = 255
			else:
				img[y, i] = 230
#				img[y - 2, i] = 200
#				img[y + 2, i] = 150
				img[y - 1, i] = 200


def goodSlope(img, k, leftPoint, thickness = 0):
	''' Help to jugde whether the slope matches the leftpoint.
		The function returns how many points on the line are black.'''
	result = 0
	for i in range(img.shape[1]): #left to right
		y = int(leftPoint + k*i)
		for j in range(y-i, y+i):
			if j < img.shape[0] and j >= 0 and img[j,i] == 0:
				result += 1
	return result		

def imageFileToString(imgPath):
	'''input a valid path'''
	img = np.ndarray(0, dtype = 'uint8')
	try:
		img = cv2.imread(imgPath, 0)
	except Exception, e:
		print e
		return ('', img)
	return imageFileToString(img)

def processImage(img):
	'''please input a grayscale image(using cv2.imread(<filename>,0))'''
	(retval, img) = cv2.threshold(img, 210, 255, cv2.THRESH_BINARY)
	img = img[:,5:200]  #crop
#	cv2.imwrite('codes\\cropped.bmp', img)
	leftPoints = findPoints(img, 0)
	rightPoints = findPoints(img, img.shape[1] - 1)
	
	# two possible slope yet only one of them is desired
	k1 = float(rightPoints[0] - leftPoints[0]) / (img.shape[1] - 1)
	k2 = float(rightPoints[1] - leftPoints[0]) / (img.shape[1] - 1)
	
	# a quick yet rough way to determine which slope is better
	x = img.shape[1] / 2
	if img[int(x*k1) + leftPoints[0], x] == 0 and \
		img[int(x*k2) + leftPoints[0], x] != 0:  # k1 is desired
		k2 = float(rightPoints[1] - leftPoints[1]) / (img.shape[1] - 1)
	else:
		k1 = k2
		k2 = float(rightPoints[0] - leftPoints[1]) / (img.shape[1] - 1)
	
	# processing the lines
	fillLine(img, k1, leftPoints[0])
	fillLine(img, k2, leftPoints[1])
#	cv2.imwrite('codes\\filled.bmp', img)
	
	# image blurring, you may change the parameters below to obtain different result
	blurRange = 6
	kernel = np.ones((blurRange, blurRange), np.float32) / (blurRange*blurRange)
	img = cv2.filter2D(img, -1, kernel)
#	cv2.imwrite('codes\\blurred.bmp', img)
	
	# thresholding, you may change the threshold value below to obtain different result
	thresholdVal = 110
	(retval, img) = cv2.threshold(img, thresholdVal, 255, cv2.THRESH_BINARY)
#	cv2.imwrite('codes\\binarized.bmp', img)

	return img

def imageToString(img):
	'''please input a grayscale image(using cv2.imread(<filename>,0))'''

	img = processImage(img)
	cv2.imwrite('processed.bmp', img)
	new_img = Image.open('processed.bmp')
	rawCode = pytesser.image_to_string(new_img)
	code = ""
	for letter in rawCode:
		#handle possible mismatches
		if letter >= '0' and letter <= '9':
			code += letter
		elif letter == 'z' or letter == 'Z' or letter == 'L':
			code += '2'
		elif letter == 'o' or letter == 'O' or letter == 'Q':
			code += '0'
		elif letter == 'A':
			code += '4'
		elif letter == 'S' or letter == 's' or letter == '$':
			code += '5'
		elif letter == 'g':
			code += '9'
		elif letter == '&' or letter == 'R' or letter == '%' or letter == 'a':
			code += '8'
		elif letter == '>' or letter == '?' or letter == ')':
			code += '7'
		elif letter == 'I' or letter == 'l':
			code += '1'
		elif letter == 'G' or letter == 'U':
			code += '6'
#		else:
#			code += letter
	return (code, img)
	
if __name__ == '__main__':
	codeAddr = raw_input("input the address of the code image: ")
	img = cv2.imread(codeAddr, 0) #load the image in grayscale
	(code, img) = imageToString(img)
	print code
