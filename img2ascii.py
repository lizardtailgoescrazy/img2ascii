#!/usr/bin/env python

import Image
import os
import sys
import numpy
import math
import ImageEnhance

MAXDIMENSION = 1024

#asciis=' .,:;irXAs253hMHGS#9B&@';
asciis=' `\'.-,:"_!~/\;*|^<+7r?v=iJLlYc)T{(}tsIVCxF325]1[uU4nzAXjfoZSyPweaKEHkGOh0M$N9#dq6RmDW%bpQ8Bg@&';

def convertTo(num, numMax, scale):
	return int(math.floor((num*(scale-1))/numMax))


def printAsciiImage(asciiArray):
	for each in asciiArray:
		print each


def img2ascii(filepath):
	try:
		try:
			imageData = Image.open(filepath)
		except Exception, e:
			print(str(e))
			return False		
		
		try:
			imgWidth, imgHeight = imageData.size
			print("Image size: %d * %d" % (imgWidth, imgHeight))
			
			if imgWidth > MAXDIMENSION or imgHeight > MAXDIMENSION:
				if imgWidth >= imgHeight:
					imgHeight = (1024*imgHeight)/imgWidth
					imgWidth = MAXDIMENSION
					
				else:
					imgWidth = (1024*imgWidth)/imgHeight
					imgHeight = MAXDIMENSION
				
				imageData = imageData.resize((imgWidth, imgHeight), Image.ANTIALIAS)
				print("The image was too big, new size : %d %d" % (imgWidth, imgHeight))
				
		except Exception,e:
			print(str(e))
			print("ERROR: resizing image")
			return False
		
		try:
			print("Converting image to grayscale...")
			grayImgData = imageData.convert('L') # convert image to black and white

			#enhance image
			bright = ImageEnhance.Brightness(grayImgData)
			grayImgData = bright.enhance(1.6)
			contr = ImageEnhance.Contrast(grayImgData)
			grayImgData = contr.enhance(0.5)


			#grayImgData.save('gray.png')
		except Exception,e:
			print(str(e))
			print("ERROR: converting image to grayscale")
			return False

		try:
			cellWidth = 8
			cellHeight = 13
			imgArray = numpy.array(grayImgData)
			imgArray = 255 - imgArray

			#print imgArray.shape

			numCellsWidth = int(math.floor(imgWidth/cellWidth))
			numCellsHeight = int(math.floor(imgHeight/cellHeight))

			#print("[%d, %d]" % (numCellsWidth, numCellsHeight))
			
			#imgArray = numpy.reshape(imgArray, (-1, imgWidth))

			asciiArray = [[] for i in range(numCellsHeight)]

			for j in range(0, numCellsHeight):
				for i in range(0, numCellsWidth):
					total = 0
					for ii in range(i*cellWidth, (i+1)*cellWidth):
						for jj in range(j*cellHeight, (j+1)*cellHeight):
							#print("debug: %d %d - %d" % (ii, jj, imgArray.item(ii, jj)))
							total = total + int(imgArray[jj][ii])
					avg = total/(cellHeight*cellWidth)
					asciiArray[j].append(avg)
	
			#print (asciiArray)

			maxValue = -1
			minValue = 1000
			for eachRow in asciiArray:	
				for each in eachRow:
					if each > maxValue:
						maxValue = each
					if each < minValue:
						minValue = each
			
			print ("MAX: %d MIN: %d" % (maxValue, minValue))
			normalisedAsciiArray = [[] for i in range(numCellsHeight)]

			counter = 0
			asciiImg = []
			for eachRow in asciiArray:
				asciiImg.append([])
				asciiImg[counter] = ""
				for each in eachRow:

					if maxValue > 0 and not(maxValue == minValue):
						value = convertTo(each-minValue, maxValue-minValue , len(asciis))
					else:
						value = convertTo(each, maxValue, len(asciis))

					asciiImg[counter] = asciiImg[counter] + asciis[value]
					#debug
					#asciiImg[counter] = asciiImg[counter] + str(each) + "."
					normalisedAsciiArray[counter].append(value)
				counter = counter + 1
			
			#print (normalisedAsciiArray)
			printAsciiImage(asciiImg)

		except Exception,e:
			
			print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
			print "%d - %d " % (ii ,jj)
			print(str(e))
			print("ERROR: numpy stuffs")
			return False
			
		return True
		isBlank = True
		for scanline in imageArray:
			if (scanline == 255).all():
				#print "All 255."
				continue
			else:
				#print "Not all 255"
				isBlank = False
				pass
		return isBlank
	except Exception, e:
		print "***ERROR during function isBlank"
		print str(e)
#End of isBlank

def main():
	try:
		filepath = str(sys.argv[1])
		img2ascii(filepath)
	except Exception, e:
		print "***ERROR: In main."
		print str(e)
#End of main()


#Execution
if not len(sys.argv) == 2:
	print"ERROR: Usage : python "+str(sys.argv[0])+" <filepath>"
	exit(-1)
main()
