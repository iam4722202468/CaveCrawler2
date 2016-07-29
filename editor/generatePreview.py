import pygame
import forms

def searchImageCache(imageName, imageCache):
	for x in imageCache:
		if x[1] == imageName:
			return x[0]
	
	imageCache.append([pygame.image.load(imageName).convert_alpha(), imageName]) #this doesn't actually add it...
	return imageCache[-1][0]

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

def getSprites(imageMap, imageData):
	return

def getThumbnail(fileMap, imageData, imageCache):
	height = len(fileMap[0])
	width = len(fileMap[0][0])
	
	newThumb = pygame.Surface((width*32, height*32), pygame.SRCALPHA, 32).convert_alpha()
	
	for layerNum in xrange(0,2):
		for i, x in enumerate(fileMap[layerNum]):
			for j, y in enumerate(x):
				if fileMap[layerNum][i][j] != '0':
					
					place = forms.getData(imageData, fileMap[layerNum][i][j].split(":")[0])
					if place != -1:
						gameBlockX = int(imageData[place][1][0])
						gameBlockY = int(imageData[place][1][1])
					else:
						gameBlockX = 32
						gameBlockY = 32
					
					imageMap = searchImageCache(fileMap[layerNum][i][j].split(":")[0], imageCache)
					
					placeInImage = fileMap[layerNum][i][j].split(":")[1]
					
					pictureRect = imageMap.get_rect()
					sheetX = pictureRect[2]
					sheetY = pictureRect[3]
					
					tu = int(placeInImage) % (sheetX / gameBlockX);
					tv = int(placeInImage) / (sheetX / gameBlockX);
					
					tempSurface = pygame.Surface((gameBlockX, gameBlockY), pygame.SRCALPHA, 32).convert_alpha()
					
					tempSurface.blit(imageMap, (0,0), (tu*gameBlockX, tv*gameBlockY, gameBlockX, gameBlockY))
					tempSurface = pygame.transform.scale(tempSurface, (32, int((gameBlockY/float(gameBlockX))*32)))
					
					newThumb.blit(tempSurface, (j*32, i*32), (0, 0, 32, 32))
			
	return pygame.transform.scale(newThumb, (80, int((height/float(width))*80)))
