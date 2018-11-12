from Tkinter import *
import os.path

def getData(imageData, imageName):
	for i,x in enumerate(imageData):
		if x[0] == imageName:
			return i
	return -1

class getSheetInfo(Frame):
	def generateFile(self):
		self.fillOthers()
		
		if self.myPlace == -1:
			self.imageData.append([self.imageName, [self.spriteSizeXEntry.get(), self.spriteSizeYEntry.get(), str(self.mapX), str(self.mapY)]])
		else:
			self.imageData[self.myPlace] = [self.imageName, [self.spriteSizeXEntry.get(), self.spriteSizeYEntry.get(), str(self.mapX), str(self.mapY)]]
		
		stringToWrite = ""
		
		for x in self.imageData:
			stringToWrite += x[0] + "\n" + ",".join(x[1]) + '\n'
		
		f = open("./editorInfo/imageInfo", "w")
		f.write(stringToWrite)
		
		self.destroy()
		self.quit()
	
	def fillOthers(self):
		infoList = [0,0,0,0]
		
		if self.spriteSizeXEntry.get().isdigit():
			infoList[0] = int(self.spriteSizeXEntry.get())
		if self.spriteSizeYEntry.get().isdigit():
			infoList[1] = int(self.spriteSizeYEntry.get())
		
		if self.spriteAmountXEntry.get().isdigit():
			infoList[2] = int(self.spriteAmountXEntry.get())
		if self.spriteAmountYEntry.get().isdigit():
			infoList[3] = int(self.spriteAmountYEntry.get())
		
		for i,x in enumerate(infoList):
			if x == 0:
				if i == 0 and infoList[2] != 0:
					self.spriteSizeXEntry.insert(0, str(self.mapX/infoList[2]))
				if i == 1 and infoList[3] != 0:
					self.spriteSizeYEntry.insert(0, str(self.mapY/infoList[3]))
				if i == 2 and infoList[0] != 0:
					self.spriteAmountXEntry.insert(0, str(self.mapX/infoList[0]))
				if i == 3 and infoList[1] != 0:
					self.spriteAmountYEntry.insert(0, str(self.mapY/infoList[1]))
	
	def createWidgets(self):
		self.spriteSizeX = Label(self)
		self.spriteSizeX["text"] = "Sprite X Size"
		self.spriteSizeX.grid(column=0, row=0)
		
		self.spriteSizeXEntry = Entry(self)
		self.spriteSizeXEntry.grid(column=1, row=0)
		
		self.spriteSizeY = Label(self)
		self.spriteSizeY["text"] = "Sprite Y Size"
		self.spriteSizeY.grid(column=0, row=1)
		
		self.spriteSizeYEntry = Entry(self)
		self.spriteSizeYEntry.grid(column=1, row=1)
		
		self.spriteAmountX = Label(self)
		self.spriteAmountX["text"] = "Sprite X Amount"
		self.spriteAmountX.grid(column=0, row=2)
		
		self.spriteAmountXEntry = Entry(self)
		self.spriteAmountXEntry.grid(column=1, row=2)
		
		self.spriteAmountY = Label(self)
		self.spriteAmountY["text"] = "Sprite Y Amount"
		self.spriteAmountY.grid(column=0, row=3)
		
		self.spriteAmountYEntry = Entry(self)
		self.spriteAmountYEntry.grid(column=1, row=3)
		
		self.fillValues = Button(self)
		self.fillValues["text"] = "Fill Values"
		self.fillValues["fg"]   = "green"
		self.fillValues["command"] =  self.fillOthers
		
		self.fillValues.grid(row=4, column=0, columnspan=3, sticky=W+E)
		
		self.generate = Button(self)
		self.generate["text"] = "Generate File"
		self.generate["fg"]   = "blue"
		self.generate["command"] =  self.generateFile
		
		self.generate.grid(row=5, column=0, columnspan=3, sticky=W+E)
		
		self.QUIT = Button(self)
		self.QUIT["text"] = "QUIT"
		self.QUIT["fg"]   = "red"
		self.QUIT["command"] =  self.quit
		
		self.QUIT.grid(row=6, column=0, columnspan=3, sticky=W+E)
		
		if self.myPlace > -1:
			self.spriteSizeXEntry.insert(0, self.imageData[self.myPlace][1][0])
			self.spriteSizeYEntry.insert(0, self.imageData[self.myPlace][1][1])
			self.spriteAmountXEntry.insert(0, str(self.mapX/int(self.imageData[self.myPlace][1][0])))
			self.spriteAmountYEntry.insert(0, str(self.mapY/int(self.imageData[self.myPlace][1][1])))
	
	def __init__(self, master=None, mapSize=None, imageName=None, imageData=None):
		Frame.__init__(self, master)
		
		self.mapX = mapSize[0]
		self.mapY = mapSize[1]
		self.imageName = imageName
		self.imageData = imageData
		
		self.myPlace = getData(imageData, imageName)
		
		self.grid()
		self.createWidgets()

class createNewMap(Frame):
	def generateFile(self):
		tempArray = ['0']
		if self.mapSizeXEntry.get().isdigit() and self.mapSizeYEntry.get().isdigit():
			if not os.path.exists("./maps/" + self.mapNameEntry.get()):
				os.makedirs("./maps/" + self.mapNameEntry.get())
				tempArray = "\n".join([" ".join(tempArray*int(self.mapSizeXEntry.get()))] * int(self.mapSizeYEntry.get()))
				with open("./maps/" + self.mapNameEntry.get() + "/layer" ,"w+") as f:
					f.write(tempArray)
				with open("./maps/" + self.mapNameEntry.get() + "/objects" ,"w+") as f:
					f.write(tempArray)
				with open("./maps/" + self.mapNameEntry.get() + "/map" ,"w+") as f:
					f.write(tempArray)
				
				self.destroy()
				self.quit()
	
	def createWidgets(self):
		self.mapName = Label(self)
		self.mapName["text"] = "Map Name"
		self.mapName.grid(column=0, row=0)
		
		self.mapNameEntry = Entry(self)
		self.mapNameEntry.grid(column=1, row=0)
		
		self.mapSizeX = Label(self)
		self.mapSizeX["text"] = "Map X Size"
		self.mapSizeX.grid(column=0, row=1)
		
		self.mapSizeXEntry = Entry(self)
		self.mapSizeXEntry.grid(column=1, row=1)
		
		self.mapSizeY = Label(self)
		self.mapSizeY["text"] = "Map Y Size"
		self.mapSizeY.grid(column=0, row=2)
		
		self.mapSizeYEntry = Entry(self)
		self.mapSizeYEntry.grid(column=1, row=2)
		
		self.generate = Button(self)
		self.generate["text"] = "Generate File"
		self.generate["fg"]   = "blue"
		self.generate["command"] =  self.generateFile
		
		self.generate.grid(row=3, column=0, columnspan=2, sticky=W+E)
		
		self.QUIT = Button(self)
		self.QUIT["text"] = "QUIT"
		self.QUIT["fg"]   = "red"
		self.QUIT["command"] =  self.quit
		
		self.QUIT.grid(row=4, column=0, columnspan=3, sticky=W+E)
	
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.grid()
		self.createWidgets()

class createError(Frame):
	def createWidgets(self):
		self.mapName = Label(self)
		self.mapName["text"] = self.errMessage
		self.mapName.grid(column=0, row=0)
		
		self.QUIT = Button(self)
		self.QUIT["text"] = "QUIT"
		self.QUIT["fg"]   = "red"
		self.QUIT["command"] =  self.quit
		
		self.QUIT.grid(row=1, column=0, columnspan=1, sticky=W+E)
	
	def __init__(self, master=None, errMessage=None):
		Frame.__init__(self, master)
		
		self.errMessage = errMessage
		
		self.grid()
		self.createWidgets()

class createNewSprite(Frame):
	def generateFile(self):
		
		if self.mapNameEntry.get() != "":
			
			stringToWrite = ""
			
			for i,x in enumerate(self.widgetArray):
				if len(x) == 1:
					stringToWrite += x[0]["text"] + ": " + str(self.varArray[i].get()) + '\n'
				if len(x) == 2:
					stringToWrite += x[0]["text"] + ": " + x[1].get() + '\n'
			
			preset = ['path: -'] #don't forget spriteOrder
			
			for x in preset:
				stringToWrite += x + '\n'
			
			stringToWrite += "spriteSheetPlace: " + self.filePlace.split('/')[-1] + '\n'
			
			stringToWrite += "sizeX: " + self.spriteSize[0] + '\n'
			stringToWrite += "sizeY: " + self.spriteSize[1] + '\n'
			stringToWrite += "spriteSheetSizeX: " + self.spriteSize[2] + '\n'
			stringToWrite += "spriteSheetSizeY: " + self.spriteSize[3] + '\n'
			stringToWrite += "cameraFocus: 0"
			
			with open("./sprites/" + self.mapNameEntry.get(),"w+") as f:
				f.write(stringToWrite + '\n')
			
			self.destroy()
			self.quit()
	
	def createWidgets(self):
		self.mapName = Label(self)
		self.mapName["text"] = "Sprite Name"
		self.mapName.grid(column=0, row=0)
		
		columnSize = 3
		counter = 0
		
		self.widgetArray = []
		self.varArray = []
		self.entryArray = []
		
		self.mapNameEntry = Entry(self)
		self.mapNameEntry.grid(column=1, columnspan=columnSize-1, row=0)
		
		while counter*(columnSize-1) < len(self.objectValues):
			for x in xrange(0, columnSize):
				
				if counter*columnSize + x > len(self.objectValues)-1:
					break
				
				self.varArray.append(IntVar())
				self.widgetArray.append([Checkbutton(self, text=self.objectValues[counter*columnSize + x], variable=self.varArray[-1])])
				self.widgetArray[-1][0].grid(column=x, row=counter+1, sticky=W)
			
			counter += 1
		
		for x in self.objectValuesInt:
			self.widgetArray.append([Label(self, text=x), Entry(self)])
			self.widgetArray[-1][0].grid(column=0, row=counter+2, sticky=W)
			self.widgetArray[-1][1].grid(column=1, row=counter+2, sticky=W)
			
			if x == "spriteOrder":
				self.widgetArray[-1][1].insert(0, str(self.spriteImage))
			elif x == "extraInfo":
				self.widgetArray[-1][1].insert(0, "-")
			else:
				self.widgetArray[-1][1].insert(0, "0")
			
			counter += 1
		
		self.generate = Button(self)
		self.generate["text"] = "Generate File"
		self.generate["fg"]   = "blue"
		self.generate["command"] =  self.generateFile
		
		self.generate.grid(row=counter+2, column=0, columnspan=columnSize, sticky=W+E)
		
		self.QUIT = Button(self)
		self.QUIT["text"] = "QUIT"
		self.QUIT["fg"]   = "red"
		self.QUIT["command"] =  self.quit
		
		self.QUIT.grid(row=counter+3, column=0, columnspan=columnSize, sticky=W+E)
	
	def __init__(self, master=None, spriteSize=None, spriteImage=None, filePlace=None):
		Frame.__init__(self, master)
		
		self.spriteSize = spriteSize
		self.spriteImage = spriteImage
		self.filePlace = filePlace
		
		self.objectValues = ['movable', 'solid', 'animated', 'selfMoving', 'moveWithKeys', 'wander']
		self.objectValuesInt = ['movingSpaceX', 'movingSpaceY', 'movingDirection', 'currentSprite', 'animatedSpeed', 'spriteOrder', 'extraInfo']
		
		self.grid()
		self.createWidgets()
