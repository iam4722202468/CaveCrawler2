import glob
import sys
import os.path

biggestX = -1
biggestY = -1

pythonMaps = []
pythonLayers = []
pythonObjects = []

def getFileInfo(fileList):
	currentMap = []
	global biggestX
	global biggestY
	
	for x in fileList:
		if x == "same":
			currentMap.append(currentMap[-1])
		else:
			currentMap.append(x.split(" "))
	
	if biggestX < len(fileList[0].split(" ")):
		biggestX = len(fileList[0].split(" "))
	
	if biggestY < len(fileList):
		biggestY = len(fileList)
	
	return currentMap

mapNames = []

for fileName in glob.glob("./gamemaps/*.map"):
	print "found " + fileName
	
	mapNames.append(fileName)
	
	with open(fileName) as f:
		content = f.read().splitlines()
		pythonMaps.append(getFileInfo(content))
	
	layerName = "./gamemaps/" + fileName.split('/')[2][:fileName.split('/')[2].find('.')] + '.layer'
	
	with open(layerName) as f:
		content = f.read().splitlines()
		pythonLayers.append(getFileInfo(content))
	
	objectName = "./gamemaps/" + fileName.split('/')[2][:fileName.split('/')[2].find('.')] + '.objects'
	
	with open(objectName) as f:
		content = f.read().splitlines()
		pythonObjects.append(getFileInfo(content))

cppStringMap = "std::vector<std::vector<std::vector<int>>> maps{"
cppFileMap = ""

cppStringLayer = "std::vector<std::vector<std::vector<int>>> layers{"
cppFileLayer = ""

cppStringObject = "std::vector<std::vector<std::vector<int>>> objects{"
cppFileObject = ""

for pythonMap in pythonMaps:
	cppStringMap += "{"
	
	for x in pythonMap:
		lineString = ""
		for y in x:
			if y != "":
				lineString += y + ','
		
		cppFileMap += lineString[:-1] + '\n'
		cppStringMap += "{" + lineString[:-1] + "},"
	
	cppFileMap += "_\n"
	cppStringMap = cppStringMap[:-1]
	cppStringMap += "},"

cppStringMap = cppStringMap[:-1] + "};"

for pythonLayer in pythonLayers:
	cppStringLayer += "{"
	
	for x in pythonLayer:
		lineString = ""
		for y in x:
			if y != "":
				lineString += y + ','
		
		cppFileLayer += lineString[:-1] + '\n'
		cppStringLayer += "{" + lineString[:-1] + "},"
	
	cppFileLayer += "_\n"
	cppStringLayer = cppStringLayer[:-1]
	cppStringLayer += "},"

cppStringLayer = cppStringLayer[:-1] + "};"

##
# bool
#	movable							0
#	solid							1
#	animated						2
#	selfMoving						3
#	moveWithKeys					4
#	wander							5
#
# int
#	movingSpaceX					6
#	movingSpaceY					7
#	
#	movingDirection					8
#	currentSprite					9
#		
#	animatedSpeed					10
#
#	sizeX							11
#	sizeY							12
#	spriteSheetSizeX				13
#	spriteSheetSizeY				14
#
# string
#	spriteSheetPlace				15
#
# array seperated by ','
#	std::vector<int> spriteOrder	16
#	std::vector<int> path			17
#	std::vector<int> extraInfo		18
##

objectValues = ['movable', 'solid', 'animated', 'selfMoving', 'moveWithKeys', 'wander', 'movingSpaceX', 'movingSpaceY', 'movingDirection', 'currentSprite', 'animatedSpeed', 'sizeX', 'sizeY', 'spriteSheetSizeX', 'spriteSheetSizeY', 'spriteSheetPlace', 'spriteOrder', 'path', 'extraInfo']

objectCounter = 1
objectAttributes = [] #list of attribute strings

for pythonObject in pythonObjects:
	cppStringObject += "{"
	for x in pythonObject:
		lineString = ""
		for y in x:
			if y != "":
				if y == '0':
					lineString += y + ','
				else:
					lineString += str(objectCounter) + ','
					objectCounter += 1
					with open("./gamemaps/" + y + '.object') as f:
						content = f.read()
						
						tempString = ""
						
						for attr in objectValues:
							tempString += content[content.find(attr) + len(attr) + 1:content.find('\n', content.find(attr))].replace(" ", "").replace("	","") + " "
						
						objectAttributes.append(tempString)
		cppFileObject += lineString[:-1] + '\n'
		cppStringObject += "{" + lineString[:-1] + "},"

	cppFileObject += "_\n"
	cppStringObject = cppStringObject[:-1]
	cppStringObject += "},"

cppStringObject = cppStringObject[:-1] + "};"

objectBottomCpp = 'std::vector<std::vector<std::string>> objectInfo{'  #data containing individual item info
objectBottomFile = ""

for x in objectAttributes:
	lineString = "{"
	for y in x.split(" "):
		if y != "":
			lineString += '"' + y + '",'

	objectBottomCpp += lineString[:-1] + "},"
	objectBottomFile += x + '\n'

objectBottomCpp = objectBottomCpp[:-1] + "};"

if sys.argv[1] == "compiled":
	f = open('./includes/generatedMaps.h','w')
	f.write("#ifndef GENERATEDMAPS_H\n#define GENERATEDMAPS_H\n#include <vector>\n/*File generated by generateMaps.py*/\n" + cppStringMap + "\n" + cppStringLayer + "\n" + cppStringObject + "\n" + objectBottomCpp + "\n#endif")
else:
	f = open('./includes/generatedMaps.txt','w')
	f.write(cppFileMap)
	f.close()
	f = open('./includes/generatedLayers.txt','w')
	f.write(cppFileLayer)
	f.close()
	f = open('./includes/generatedObjects.txt','w')
	f.write(cppFileObject + "-\n" + objectBottomFile)