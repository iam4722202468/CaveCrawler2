import pygame
import forms
import glob
from shutil import copyfile

def searchImageCache(imageName, imageCache):
	for x in imageCache:
		if x[1] == imageName:
			return x[0]
	
	#doesn't actually get called from what i can tell, no point in fixing
	imageCache.append([pygame.image.load(imageName).convert_alpha(), imageName]) #this doesn't actually add it...
	return imageCache[-1][0]

def getSpriteName(imageNumber):
	return glob.glob("./sprites/*")[imageNumber]

def getSpriteInfo(fileName):
	with open(fileName) as f:
		currentSpriteInfo = {}
		for x in f.read().splitlines():
			thisLine = x.split(": ")
			currentSpriteInfo[thisLine[0]] = thisLine[1]
	return currentSpriteInfo

def getViewTile(mainMaps, sprite, imageData, imageCache, panelSize, layerNumber):
	panelSize -= 2
	
	tileSurface = pygame.Surface((panelSize, panelSize), pygame.SRCALPHA, 32)
	tileSurface = tileSurface.convert_alpha()
	
	startLayer = 0
	endLayer = 0
	
	if layerNumber == 0:
		startLayer = 0
		endLayer = 1
	elif layerNumber == 1:
		startLayer = 1
		endLayer = 2
	elif layerNumber == 3: #show both
		startLayer = 0
		endLayer = 2
		
	for x in xrange(startLayer, endLayer):
		if mainMaps[x] != '0':
			tileInfo = mainMaps[x].split(":")
			spriteSheet = searchImageCache(tileInfo[0], imageCache)
			
			place = forms.getData(imageData, tileInfo[0])
			if place != -1:
				gameBlockX = int(imageData[place][1][0])
				gameBlockY = int(imageData[place][1][1])
			else:
				gameBlockX = 32
				gameBlockY = 32
			
			pictureRect = spriteSheet.get_rect()
			sheetX = pictureRect[2]
			
			tu = int(tileInfo[1]) % (sheetX / gameBlockX);
			tv = int(tileInfo[1]) / (sheetX / gameBlockX);
			
			tempSurface = pygame.Surface((gameBlockX, gameBlockY), pygame.SRCALPHA, 32).convert_alpha()
			
			tempSurface.blit(spriteSheet, (0,0), (tu*gameBlockX, tv*gameBlockY, gameBlockX, gameBlockY))
			tempSurface = pygame.transform.scale(tempSurface, (panelSize, int((gameBlockY/float(gameBlockX))*panelSize)))
			
			tileSurface.blit(tempSurface, (0,0), (0, 0, panelSize, panelSize))
	
	if sprite != '0' and (layerNumber == 2 or layerNumber == 3):
		spriteInfo = getSpriteInfo(sprite)
		tempSurface = getSpriteTile(spriteInfo, imageCache)
		tempSurface = pygame.transform.scale(tempSurface, (panelSize, int((int(spriteInfo['sizeY'])/float(int(spriteInfo['sizeX'])))*panelSize)))
		tileSurface.blit(tempSurface, (0,0), (0, 0, panelSize, panelSize))
		
	return tileSurface

def getTiles(spriteSize, spriteMapName, imageCache):
	tileArray = []
	
	spriteSize = [int(spriteSize[0]), int(spriteSize[1])]
	
	spriteSheet = searchImageCache(spriteMapName, imageCache)
	
	amountX = spriteSheet.get_rect().size[0] / spriteSize[0]
	amountY = spriteSheet.get_rect().size[1] / spriteSize[1]
	
	for y in xrange(0, amountY):
		for x in xrange(0, amountX):
			tileArray.append(pygame.Surface((spriteSize[0], spriteSize[1])))
			tileArray[-1].blit(spriteSheet, (0, 0), (x*spriteSize[0], y*spriteSize[1], spriteSize[0], spriteSize[1]))
			tileArray[-1] = pygame.transform.scale(tileArray[-1], (80, int(spriteSize[0]/float(spriteSize[1])*80)))
	
	return tileArray

def getSpriteTile(x, imageCache): #x is sprite info
	thisSurface = pygame.Surface((int(x['sizeX']), int(x['sizeY'])), pygame.SRCALPHA, 32).convert_alpha()
	spriteSheet = searchImageCache("../resources/" + x['spriteSheetPlace'], imageCache)
		
	placeInImage = x['spriteOrder'].split(",")[0]
	tu = int(placeInImage) % (int(x['spriteSheetSizeX']) / int(x['sizeX']));
	tv = int(placeInImage) / (int(x['spriteSheetSizeX']) / int(x['sizeX']));
	
	thisSurface.blit(spriteSheet, (0, 0), (tu*int(x['sizeX']), tv*int(x['sizeY']), int(x['sizeX']), int(x['sizeY'])))
	return thisSurface

def loadSpriteDisplay(imageCache):
	tileArray = []
	
	for fileName in glob.glob("./sprites/*"):
		x = getSpriteInfo(fileName)
		tileArray.append(getSpriteTile(x, imageCache))
		tileArray[-1] = pygame.transform.scale(tileArray[-1], (80, int(int(x['sizeX'])/float(int(x['sizeY']))*80)))
	
	return tileArray

def getResizedImage(place, imageData, imageMap, imageCache, placeInImage):
	if place != -1:
		gameBlockX = int(imageData[place][1][0])
		gameBlockY = int(imageData[place][1][1])
	else:
		gameBlockX = 32
		gameBlockY = 32
	
	pictureRect = imageMap.get_rect()
	sheetX = pictureRect[2]
	sheetY = pictureRect[3]
	
	tu = int(placeInImage) % (sheetX / gameBlockX);
	tv = int(placeInImage) / (sheetX / gameBlockX);
	
	tempSurface = pygame.Surface((gameBlockX, gameBlockY), pygame.SRCALPHA, 32).convert_alpha()
	
	tempSurface.blit(imageMap, (0,0), (tu*gameBlockX, tv*gameBlockY, gameBlockX, gameBlockY))
	tempSurface = pygame.transform.scale(tempSurface, (32, int((gameBlockY/float(gameBlockX))*32)))
	return tempSurface

def generateMap(allMaps, imageData, imageCache):
	print "generating map"
	
	fileTypes = ['.map', '.layer', '.objects']
	tileCache = [''] #needs to start at 1
	
	for currentMap in allMaps:
		for i, fileName in enumerate(fileTypes):
			finalArray = []
			for x in currentMap[i]:
				tempArray = []
				for y in x:
					if y != '0':
						if i == 0 or i == 1:
							try: #try to see if tile is already in tileCache, if not append to cache
								index = tileCache.index(y)
							
							except ValueError:
								index = len(tileCache)
								tileCache.append(y)
							
							tempArray.append(index)
						
						elif i == 2: #sprites don't need to be in cache
							tempArray.append(y.split("/")[-1])
					else:
						tempArray.append(0)
				
				finalArray.append(tempArray)
			
			fileString = ""
			for p in finalArray:
				fileString += " ".join(str(pString) for pString in p) + "\n"
			
			f = open("./generated/" + currentMap[-1] + fileName, "w")
			f.write(fileString)
			f.close()
			
	for spriteName in glob.glob("./sprites/*"):
		newPlace = "./generated/" + spriteName.split("/")[-1] + ".object"
		copyfile(spriteName,newPlace)
			
	
	finalImage = pygame.Surface((32*len(tileCache), 32), pygame.SRCALPHA, 32).convert_alpha()
	
	for i, x in enumerate(tileCache): #generate image
		if i > 0: #ignore first place
			place = forms.getData(imageData, x.split(":")[0])
			placeInImage = x.split(":")[1]
			imageMap = searchImageCache(x.split(":")[0], imageCache)
			
			tempSurface = getResizedImage(place, imageData, imageMap, imageCache, placeInImage)
			finalImage.blit(tempSurface, (i*32, 0), (0, 0, 32, 32))
	
	pygame.image.save(finalImage,"./generated/spritemap.png")

def getThumbnail(fileMap, imageData, imageCache):
	height = len(fileMap[0])
	width = len(fileMap[0][0])
	
	newThumb = pygame.Surface((width*32, height*32), pygame.SRCALPHA, 32).convert_alpha()
	
	for layerNum in xrange(0,2):
		for i, x in enumerate(fileMap[layerNum]):
			for j, y in enumerate(x):
				if fileMap[layerNum][i][j] != '0':
					
					imageMap = searchImageCache(fileMap[layerNum][i][j].split(":")[0], imageCache)
					place = forms.getData(imageData, fileMap[layerNum][i][j].split(":")[0]) #to get image data
					placeInImage = fileMap[layerNum][i][j].split(":")[1]
					
					tempSurface = getResizedImage(place, imageData, imageMap, imageCache, placeInImage)
					
					newThumb.blit(tempSurface, (j*32, i*32), (0, 0, 32, 32))
			
	return pygame.transform.scale(newThumb, (80, int((height/float(width))*80)))
