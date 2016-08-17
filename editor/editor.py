# -*- coding: utf-8 -*-

import pygame
import glob
import sys
import os.path
import time

from Tkinter import *
import forms

import generatePreview

pygame.init()

display_width = 800
display_height = 700

fileMapInfo = []
imageCache = []

displayingOnLeft = 0

def generateImageData():
	imageData = []
	tempArray = []
	
	with open("./editorInfo/imageInfo") as f:
		counter = 0
		for x in f.read().splitlines():
			if x != "":
				if counter == 0:
					tempArray.append(x)
					counter = 1
				else:
					tempArray.append(x.split(","))
					imageData.append(tempArray)
					tempArray = []
					counter = 0
	return imageData

imageData = generateImageData()

fileList = []
originalSizes = []

for fileName in glob.glob("../resources/*.png"):
	fileList.append(fileName)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Map Editor')

imagePositions = []

sectionSelected = 0
selectedImage = 0
startAt = 0

imageCache = []
copiedInfo = '0'

showingLayer = 0

for x in fileList:
	imageCache.append([pygame.image.load(x), x])
	originalSizes.append((imageCache[-1][0].get_rect()[2], imageCache[-1][0].get_rect()[3]))

def createSheetDisplay(fileList, imageCache):
	thumbnails = []
	
	for x in fileList:
		thumbnails.append(generatePreview.searchImageCache(x, imageCache))
		
		pictureRect = thumbnails[-1].get_rect()
		originalSizes.append((pictureRect[2],pictureRect[3]))
		
		thumbnails[-1] = pygame.transform.scale(thumbnails[-1], (80, int((float(pictureRect[3]) / pictureRect[2]) * 80)))
	
	return thumbnails

def drawImages(gameDisplay, thumbnails, startAt, selected, imagePositions, imageData, fileList):
	addY = 15
	distanceBetween = 15
	
	pygame.draw.rect(gameDisplay, (0,0,0), (0, 0, 98, display_height))
	
	counter = 0
	imagePositions = []
	
	for x in xrange(0, startAt):
		imagePositions.append((0,0,0,0))
	
	for imagePlace in xrange(startAt, len(thumbnails)):
		pictureRect = thumbnails[imagePlace].get_rect().move((10, addY))
		imagePositions.append((pictureRect[0],pictureRect[1],pictureRect[2]+pictureRect[0],pictureRect[3]+pictureRect[1]))
		
		if fileList != []:
			myPlace = forms.getData(imageData, fileList[imagePlace])
		else:
			myPlace = -1
		
		if myPlace > -1:
			pygame.draw.rect(gameDisplay, (50,100,50), (pictureRect[0]-5, pictureRect[1]-5, pictureRect[2]+10, pictureRect[3]+10))
		
		if imagePlace == selected:
			if myPlace == -1:
				pygame.draw.rect(gameDisplay, (50,50,50), (pictureRect[0]-5, pictureRect[1]-5, pictureRect[2]+10, pictureRect[3]+10))
			else:
				pygame.draw.rect(gameDisplay, (50,200,50), (pictureRect[0]-5, pictureRect[1]-5, pictureRect[2]+10, pictureRect[3]+10))
		
		if addY+pictureRect[3] > display_height:
			break
		
		counter += 1
		
		gameDisplay.blit(thumbnails[imagePlace], pictureRect)
		
		addY += pictureRect[3] + distanceBetween
	
	myfont = pygame.font.SysFont("tahoma", 10)
	
	countUp = myfont.render(str(startAt), 1, (255,255,255))
	gameDisplay.blit(countUp, (90, 5))
	
	countDown = myfont.render(str(len(thumbnails) - (counter + startAt)), 1, (255,255,255))
	
	gameDisplay.blit(countDown, (90, display_height-15))
	
	return imagePositions

def drawSelectedBar(gameDisplay, selectedSection):
	if selectedSection == 0:
		pygame.draw.rect(gameDisplay, (100,0,0), (98, 0, 2, display_height))
	elif selectedSection == 1:
		pygame.draw.rect(gameDisplay, (100,0,0), (102, 0, 2, display_height))

def mouseClickImages(pos, imagePositions, startAt):
	for i in xrange(startAt,len(imagePositions)):
		if imagePositions[i][1] > display_height: #only checks what is on screen
			return -1
		
		if pos[0] > imagePositions[i][0] and pos[0] < imagePositions[i][2] and pos[1] > imagePositions[i][1] and pos[1] < imagePositions[i][3]:
			return i
	return -1

def mouseClickTile(pos, currentMap, gridScale):
	panelSize = (display_width-104)/gridScale
	
	for y in xrange(0, gridScale):
		for x in xrange(0, gridScale):
			
			if x > len(currentMap[0][0]) or pos[0]-104 > len(currentMap[0][0])*panelSize:
				break
			
			if pos[1] > len(currentMap[0])*panelSize:
				break
			
			if pos[0]-104 > x*panelSize and pos[0]-104 < (x+1)*panelSize and pos[1] > y*panelSize and pos[1] < (y+1)*panelSize:
				return [x,y]
		
		if y > len(currentMap[0]):
			break
	
	return -1

def drawGrid(gameDisplay, gridScale, currentMap, gridStartAtX, gridStartAtY):
	panelSize = (display_width-104)/gridScale
	
	for x in xrange(0, gridScale):
		if x + gridStartAtX< len(currentMap[0][0]) + 1:
			pygame.draw.rect(gameDisplay, (160,160,160), ((x*panelSize)+104, 0, 2, (len(currentMap[0]) - gridStartAtY)*panelSize))
		if x + gridStartAtY< len(currentMap[0]) + 1:
			pygame.draw.rect(gameDisplay, (160,160,160), (104, x*panelSize, (len(currentMap[0][0]) - gridStartAtX)*panelSize, 2))
	
def drawSelectedGrid(gameDisplay, gridScale, gridPlaceX, gridPlaceY):
	panelSize = (display_width-104)/gridScale
	
	pygame.draw.rect(gameDisplay, (100,0,0), ((gridPlaceX*panelSize)+104, gridPlaceY*panelSize, panelSize+2, panelSize+2))
	pygame.draw.rect(gameDisplay, (0,0,0), ((gridPlaceX*panelSize)+106, gridPlaceY*panelSize+2, panelSize-2, panelSize-2))

def drawGridImages(gameDisplay, gridScale, gridPlaceX, gridPlaceY, gridStartAtX, gridStartAtY, currentMap, imageCache, imageData, layerNumber):
	panelSize = (display_width-104)/gridScale
	
	for y in xrange(gridStartAtX, len(currentMap[0][0])):
		for x in xrange(gridStartAtY, len(currentMap[0])):
			if not (currentMap[0][x][y] == '0' and currentMap[1][x][y] == '0' and currentMap[2][x][y] == '0'):
				currentTile = generatePreview.getViewTile([currentMap[0][x][y], currentMap[1][x][y]], currentMap[2][x][y], imageData, imageCache, panelSize, layerNumber)
				gameDisplay.blit(currentTile, (106+panelSize*(y-gridStartAtX),panelSize*(x-gridStartAtY)+2), (0, 0, panelSize, panelSize))

def drawLayerName(gameDisplay, showingLayer):
	layerName = ""
	if showingLayer == 0:
		layerName = "background"
	elif showingLayer == 1:
		layerName = "layer"
	elif showingLayer == 2:
		layerName = "sprites"
	elif showingLayer == 3:
		layerName = "all"
	
	myfont = pygame.font.SysFont("tahoma", 10)
	layerLabel = myfont.render("Showing layer: " + layerName, 1, (255,255,255))
	gameDisplay.blit(layerLabel, (110, display_height - 33))
	
	copiedLabel = myfont.render("Currently copied: " + copiedInfo, 1, (255,255,255))
	gameDisplay.blit(copiedLabel, (110, display_height - 20))
	
	if showingLayer == 3:
		showingInfo = currentMap[0][gridPlaceY+gridStartAtY][gridPlaceX+gridStartAtX] + "," + currentMap[1][gridPlaceY+gridStartAtY][gridPlaceX+gridStartAtX] + "," + currentMap[2][gridPlaceY+gridStartAtY][gridPlaceX+gridStartAtX]
	else:
		showingInfo = currentMap[showingLayer][gridPlaceY+gridStartAtY][gridPlaceX+gridStartAtX]
	
	showingLabel = myfont.render("Currently showing: " + showingInfo, 1, (255,255,255))
	gameDisplay.blit(showingLabel, (110, display_height - 46))

def redrawScreen(gameDisplay, sectionSelected, selectedImage, startAt, imagePositions, imageData, fileList, thumbnails, displayingOnLeft, gridScale, gridPlaceX, gridPlaceY, currentMap, gridStartAtX, gridStartAtY, imageCache):
	pygame.draw.rect(gameDisplay, (0,0,0), (0, 0, display_width, display_height))
	drawSelectedBar(gameDisplay, sectionSelected)
	pygame.draw.rect(gameDisplay, (100,100,100), (100, 0, 2, display_height))
	
	if displayingOnLeft == 0:
		imagePositions = drawImages(gameDisplay, thumbnails, startAt, selectedImage, imagePositions, imageData, fileList)
	elif displayingOnLeft == 1 or displayingOnLeft == 2 or displayingOnLeft == 3:
		imagePositions = drawImages(gameDisplay, thumbnails, startAt, selectedImage, imagePositions, imageData, [])
	
	drawGrid(gameDisplay, gridScale, currentMap, gridStartAtX, gridStartAtY)
	drawSelectedGrid(gameDisplay, gridScale, gridPlaceX, gridPlaceY)
	drawGridImages(gameDisplay, gridScale, gridPlaceX, gridPlaceY, gridStartAtX, gridStartAtY, currentMap, imageCache, imageData, showingLayer)
	
	drawLayerName(gameDisplay, showingLayer)
	
	pygame.display.flip()
	pygame.display.update()
	
	return imagePositions

def loadFiles():
	fileMapInfo = []
	
	fileNames = ["/map", "/layer", "/objects"]
	
	for folder in os.listdir("./maps"):
		tempArray = []
		for currentFile in fileNames:
			with open("./maps/" + folder + currentFile) as f:
				tempArrayTwo = []
				for x in f.read().splitlines():
					tempArrayTwo.append(x.split(" "))
				tempArray.append(tempArrayTwo)
		
		tempArray.append(folder)
		fileMapInfo.append(tempArray)
	return fileMapInfo

def saveCurrentMap(currentMap):
	f = open("./maps/" + currentMap[3] + "/map", "w")
	f.write('\n'.join([' '.join(row) for row in currentMap[0]]))
	
	f = open("./maps/" + currentMap[3] + "/layer", "w")
	f.write('\n'.join([' '.join(row) for row in currentMap[1]]))
	
	f = open("./maps/" + currentMap[3] + "/objects", "w")
	f.write('\n'.join([' '.join(row) for row in currentMap[2]]))

def regenAllData():
	global fileMapInfo
	global imageData
	
	fileMapInfo = loadFiles()
	imageData = generateImageData()

thumbnails = []

def createSpriteDisplay(spriteMapName, imageData, imageCache):
	place = forms.getData(imageData, spriteMapName)
	
	if place != -1:
		spriteSize = imageData[place][1]
	else:
		spriteSize = ["32","32","32","32"]
	
	thumbnails = generatePreview.getTiles(spriteSize, spriteMapName, imageCache)
	return thumbnails

def createLoadDisplay(fileMapInfo, imageData, imageCache):
	thumbnails = []
	
	for fileMap in fileMapInfo:
		thumbnailSurface = generatePreview.getThumbnail(fileMap, imageData, imageCache)
		
		myfont = pygame.font.SysFont("tahoma", 14)
		folderName = myfont.render(fileMap[3], 1, (255,0,255))
		thumbnailSurface.blit(folderName, (0, 0))
		
		thumbnails.append(thumbnailSurface)
	
	return thumbnails

showingSpriteData = ""

gridScale = 20
gridPlaceX = 0		#relative to gridStartAtX
gridPlaceY = 0		#relative to gridStartAtY
gridStartAtX = 0
gridStartAtY = 0

# Init #
fileMapInfo = loadFiles()

try:
	currentMap = fileMapInfo[0]
except:
	currentMap = [[['0']],[['0']],[['0']], "nomaploaded"]

thumbnails = createSheetDisplay(fileList, imageCache)
imagePositions = redrawScreen(gameDisplay, sectionSelected, selectedImage, startAt, imagePositions, imageData, fileList, thumbnails, displayingOnLeft, gridScale, gridPlaceX, gridPlaceY, currentMap, gridStartAtX, gridStartAtY, imageCache)
running = True
frameCounter = 0 #count frames drawn. Used to tell if a tkinter window has been open
windowOpenedTime = 0
lastKeyPress = 0
########

mainStartAt = 0
mainselectedImage = 0

currentlyPressing = 0

keyPressTime = 10

hasSpriteSelected = False

try:
	while running:
		frameCounter += 1
		
		pygame.time.Clock().tick(60)
		
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key <= 276:
					currentlyPressing = event.key
				if event.key == 306:
					keyPressTime = 3
				imagePositions = redrawScreen(gameDisplay, sectionSelected, selectedImage, startAt, imagePositions, imageData, fileList, thumbnails, displayingOnLeft, gridScale, gridPlaceX, gridPlaceY, currentMap, gridStartAtX, gridStartAtY, imageCache)
			
			if event.type == pygame.KEYUP:
				if event.key <= 276:
					currentlyPressing = 0
				if event.key == 306:
					keyPressTime = 10
				imagePositions = redrawScreen(gameDisplay, sectionSelected, selectedImage, startAt, imagePositions, imageData, fileList, thumbnails, displayingOnLeft, gridScale, gridPlaceX, gridPlaceY, currentMap, gridStartAtX, gridStartAtY, imageCache)
			
			if event.type == pygame.MOUSEBUTTONUP:
				pos = pygame.mouse.get_pos()
				
				if pos[0] < 100:
					sectionSelected = 0
					imageClicked = mouseClickImages(pos, imagePositions, startAt)
					
					if imageClicked > -1:
						selectedImage = imageClicked
				
				elif pos[0] > 100:
					sectionSelected = 1
					newTileSelected = mouseClickTile(pos, currentMap, gridScale)
					
					if newTileSelected != -1:
						gridPlaceX = newTileSelected[0]
						gridPlaceY = newTileSelected[1]
				imagePositions = redrawScreen(gameDisplay, sectionSelected, selectedImage, startAt, imagePositions, imageData, fileList, thumbnails, displayingOnLeft, gridScale, gridPlaceX, gridPlaceY, currentMap, gridStartAtX, gridStartAtY, imageCache)
			if event.type == pygame.QUIT:
				running = False
		
		if frameCounter - lastKeyPress > keyPressTime:
			if currentlyPressing != 0:
				lastKeyPress = frameCounter
			
			if currentlyPressing  == pygame.K_DELETE:
				if showingLayer == 0 or showingLayer == 1 or showingLayer == 2:
					currentMap[showingLayer][gridPlaceY+gridStartAtY][gridPlaceX+gridStartAtX] = '0'
					saveCurrentMap(currentMap)
					imagePositions = redrawScreen(gameDisplay, sectionSelected, selectedImage, startAt, imagePositions, imageData, fileList, thumbnails, displayingOnLeft, gridScale, gridPlaceX, gridPlaceY, currentMap, gridStartAtX, gridStartAtY, imageCache)

			elif currentlyPressing == pygame.K_v:
				if (((showingLayer == 0 or showingLayer == 1) and not hasSpriteSelected) or (showingLayer == 2 and hasSpriteSelected)):
					if copiedInfo != '0':
						currentMap[showingLayer][gridPlaceY+gridStartAtY][gridPlaceX+gridStartAtX] = copiedInfo
						saveCurrentMap(currentMap)
						imagePositions = redrawScreen(gameDisplay, sectionSelected, selectedImage, startAt, imagePositions, imageData, fileList, thumbnails, displayingOnLeft, gridScale, gridPlaceX, gridPlaceY, currentMap, gridStartAtX, gridStartAtY, imageCache)

			if sectionSelected == 1:
				if currentlyPressing == pygame.K_l:
					showingLayer += 1
					if showingLayer == 4:
						showingLayer = 0
					imagePositions = redrawScreen(gameDisplay, sectionSelected, selectedImage, startAt, imagePositions, imageData, fileList, thumbnails, displayingOnLeft, gridScale, gridPlaceX, gridPlaceY, currentMap, gridStartAtX, gridStartAtY, imageCache)

				elif currentlyPressing == pygame.K_c:
					if showingLayer == 0 or showingLayer == 1 or showingLayer == 2:
						if currentMap[showingLayer][gridPlaceY+gridStartAtY][gridPlaceX+gridStartAtX] != '0':
							copiedInfo = currentMap[showingLayer][gridPlaceY+gridStartAtY][gridPlaceX+gridStartAtX]
							if showingLayer == 2:
								hasSpriteSelected = True
							else:
								hasSpriteSelected = False
				
				elif currentlyPressing == pygame.K_g:
					generatePreview.generateMap(fileMapInfo, imageData, imageCache)
				
				elif currentlyPressing == pygame.K_KP_PLUS:
					if gridScale != 1:
						gridScale -= 1
					imagePositions = redrawScreen(gameDisplay, sectionSelected, selectedImage, startAt, imagePositions, imageData, fileList, thumbnails, displayingOnLeft, gridScale, gridPlaceX, gridPlaceY, currentMap, gridStartAtX, gridStartAtY, imageCache)

				elif currentlyPressing == pygame.K_KP_MINUS:
					gridScale += 1
					imagePositions = redrawScreen(gameDisplay, sectionSelected, selectedImage, startAt, imagePositions, imageData, fileList, thumbnails, displayingOnLeft, gridScale, gridPlaceX, gridPlaceY, currentMap, gridStartAtX, gridStartAtY, imageCache)

				elif currentlyPressing == pygame.K_UP:
					if gridPlaceY == 0 and gridStartAtY != 0:
						gridStartAtY -= 1
					elif gridPlaceY != 0:
						gridPlaceY -= 1
					imagePositions = redrawScreen(gameDisplay, sectionSelected, selectedImage, startAt, imagePositions, imageData, fileList, thumbnails, displayingOnLeft, gridScale, gridPlaceX, gridPlaceY, currentMap, gridStartAtX, gridStartAtY, imageCache)

				elif currentlyPressing == pygame.K_DOWN:
					if gridPlaceY == gridScale-1 and gridStartAtY < len(currentMap[0]) - gridScale:
						gridStartAtY += 1
					elif gridPlaceY + gridStartAtY < len(currentMap[0]) -1:
						gridPlaceY += 1
					imagePositions = redrawScreen(gameDisplay, sectionSelected, selectedImage, startAt, imagePositions, imageData, fileList, thumbnails, displayingOnLeft, gridScale, gridPlaceX, gridPlaceY, currentMap, gridStartAtX, gridStartAtY, imageCache)

				elif currentlyPressing == pygame.K_LEFT:
					if gridPlaceX == 0 and gridStartAtX != 0:
						gridStartAtX -= 1
					elif gridPlaceX != 0:
						gridPlaceX -= 1
					imagePositions = redrawScreen(gameDisplay, sectionSelected, selectedImage, startAt, imagePositions, imageData, fileList, thumbnails, displayingOnLeft, gridScale, gridPlaceX, gridPlaceY, currentMap, gridStartAtX, gridStartAtY, imageCache)

				elif currentlyPressing == pygame.K_RIGHT:
					if gridPlaceX == gridScale-1 and gridStartAtX < len(currentMap[0][0]) - gridScale:
						gridStartAtX += 1
					elif gridPlaceX + gridStartAtX < len(currentMap[0][0]) -1:
						gridPlaceX += 1
					imagePositions = redrawScreen(gameDisplay, sectionSelected, selectedImage, startAt, imagePositions, imageData, fileList, thumbnails, displayingOnLeft, gridScale, gridPlaceX, gridPlaceY, currentMap, gridStartAtX, gridStartAtY, imageCache)
				
			elif sectionSelected == 0: #check when left is selected, and on map load or sprite show
				if currentlyPressing == pygame.K_UP:
					if startAt != 0:
						startAt -= 1
					if selectedImage != 0:
						selectedImage -= 1
					imagePositions = redrawScreen(gameDisplay, sectionSelected, selectedImage, startAt, imagePositions, imageData, fileList, thumbnails, displayingOnLeft, gridScale, gridPlaceX, gridPlaceY, currentMap, gridStartAtX, gridStartAtY, imageCache)
				
				elif currentlyPressing == pygame.K_DOWN:
					if startAt != len(thumbnails)-1:
						startAt += 1
					if selectedImage != len(thumbnails)-1:
						selectedImage += 1
					imagePositions = redrawScreen(gameDisplay, sectionSelected, selectedImage, startAt, imagePositions, imageData, fileList, thumbnails, displayingOnLeft, gridScale, gridPlaceX, gridPlaceY, currentMap, gridStartAtX, gridStartAtY, imageCache)
				
				elif currentlyPressing == pygame.K_s:
					if displayingOnLeft == 0:
						mainStartAt = startAt
						mainSelectedImage = selectedImage
						startAt = 0
						selectedImage = 0
						thumbnails = generatePreview.loadSpriteDisplay(imageCache)
						
						displayingOnLeft = 3
					elif displayingOnLeft == 3:
						displayingOnLeft = 0
						startAt = mainStartAt
						selectedImage = mainSelectedImage
						thumbnails = createSheetDisplay(fileList, imageCache)
					imagePositions = redrawScreen(gameDisplay, sectionSelected, selectedImage, startAt, imagePositions, imageData, fileList, thumbnails, displayingOnLeft, gridScale, gridPlaceX, gridPlaceY, currentMap, gridStartAtX, gridStartAtY, imageCache)
				
				elif currentlyPressing == pygame.K_l:
					if displayingOnLeft == 0:
						mainStartAt = startAt
						mainSelectedImage = selectedImage
						startAt = 0
						selectedImage = 0
						
						thumbnails = createLoadDisplay(fileMapInfo, imageData, imageCache)
						
						displayingOnLeft = 1
					elif displayingOnLeft == 1:
						
						displayingOnLeft = 0
						startAt = mainStartAt
						selectedImage = mainSelectedImage
						thumbnails = createSheetDisplay(fileList, imageCache)
					imagePositions = redrawScreen(gameDisplay, sectionSelected, selectedImage, startAt, imagePositions, imageData, fileList, thumbnails, displayingOnLeft, gridScale, gridPlaceX, gridPlaceY, currentMap, gridStartAtX, gridStartAtY, imageCache)

				if displayingOnLeft == 0:
					if currentlyPressing == pygame.K_RIGHT:
						displayingOnLeft = 2
						thumbnails = createSpriteDisplay(fileList[selectedImage], imageData, imageCache)
						showingSpriteData = fileList[selectedImage]
						
						mainStartAt = startAt
						mainSelectedImage = selectedImage
						startAt = 0
						selectedImage = 0
						imagePositions = redrawScreen(gameDisplay, sectionSelected, selectedImage, startAt, imagePositions, imageData, fileList, thumbnails, displayingOnLeft, gridScale, gridPlaceX, gridPlaceY, currentMap, gridStartAtX, gridStartAtY, imageCache)

				elif displayingOnLeft == 1:
					if currentlyPressing == pygame.K_RETURN:
						currentMap = fileMapInfo[selectedImage]
						
						gridScale = 20
						gridPlaceX = 0
						gridPlaceY = 0
						gridStartAtX = 0
						gridStartAtY = 0
						displayingOnLeft = 0
						sectionSelected = 1
						
						startAt = mainStartAt
						selectedImage = mainSelectedImage
						thumbnails = createSheetDisplay(fileList, imageCache)
						imagePositions = redrawScreen(gameDisplay, sectionSelected, selectedImage, startAt, imagePositions, imageData, fileList, thumbnails, displayingOnLeft, gridScale, gridPlaceX, gridPlaceY, currentMap, gridStartAtX, gridStartAtY, imageCache)

				elif displayingOnLeft == 2:
					if currentlyPressing == pygame.K_LEFT:
						startAt = mainStartAt
						selectedImage = mainSelectedImage
						displayingOnLeft = 0
						thumbnails = createSheetDisplay(fileList, imageCache)
						imagePositions = redrawScreen(gameDisplay, sectionSelected, selectedImage, startAt, imagePositions, imageData, fileList, thumbnails, displayingOnLeft, gridScale, gridPlaceX, gridPlaceY, currentMap, gridStartAtX, gridStartAtY, imageCache)
						
					elif currentlyPressing == pygame.K_c:
						copiedInfo = fileList[mainSelectedImage] + ":" + str(selectedImage)
						hasSpriteSelected = False
				elif displayingOnLeft == 3:
					if currentlyPressing == pygame.K_c:
						copiedInfo = generatePreview.getSpriteName(selectedImage)
						hasSpriteSelected = True
					
			if frameCounter - windowOpenedTime > 5 and (currentlyPressing == pygame.K_o or currentlyPressing == pygame.K_n or (currentlyPressing == pygame.K_s and displayingOnLeft == 2)):
				#main frame
				
				windowOpenedTime = frameCounter
				
				root = Tk()
				screen_width = root.winfo_screenwidth()
				screen_height = root.winfo_screenheight()
				
				#individual keys
				if currentlyPressing == pygame.K_s:
					sizeX = 460
					sizeY = 400
					
					root.wm_title("New Sprite")
					
					place = forms.getData(imageData, showingSpriteData)
					
					if place == -1:
						sizeX = 260
						sizeY = 100
						app = forms.createError(master=root, errMessage="Error: No image data found")
					else:
						app = forms.createNewSprite(master=root, spriteSize = imageData[place][1], spriteImage = selectedImage, filePlace = showingSpriteData)
				
				if currentlyPressing == pygame.K_n:
					sizeX = 260
					sizeY = 200
					
					root.wm_title("New Map")
					app = forms.createNewMap(master=root)
				
				if currentlyPressing == pygame.K_o:
					sizeX = 280
					sizeY = 200
					
					root.wm_title(fileList[selectedImage])
					app = forms.getSheetInfo(master=root, mapSize=originalSizes[selectedImage], imageName=fileList[selectedImage], imageData=imageData)
				
				#main frame
				placeX = screen_width/2 - sizeX/2
				placeY = screen_height/2 - sizeY/2
				
				root.geometry('%dx%d+%d+%d' % (sizeX, sizeY, placeX, placeY))
				app.mainloop()
					#app.value
				
				try:
					root.protocol("WM_DELETE_WINDOW", regenAllData())
					root.destroy()
				except:
					regenAllData()
							
	pygame.quit()
except SystemExit:
	pygame.quit()
