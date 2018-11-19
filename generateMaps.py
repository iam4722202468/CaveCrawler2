import glob
import hashlib
import struct
import sys
import os.path

mapNames = []
pythonMaps = []
pythonLayers = []
pythonObjects = []

for fileName in glob.glob("./gamemaps/*.map"):
    print "found " + fileName
    
    mapNames.append(fileName.split('/')[2][:fileName.split('/')[2].find('.')])
    
    with open(fileName) as f:
        content = f.read().splitlines()
        pythonMaps.append([i.split(' ') for i in content])
    
    layerName = "./gamemaps/" + fileName.split('/')[2][:fileName.split('/')[2].find('.')] + '.layer'
    
    with open(layerName) as f:
        content = f.read().splitlines()
        pythonLayers.append([i.split(' ') for i in content])
    
    objectName = "./gamemaps/" + fileName.split('/')[2][:fileName.split('/')[2].find('.')] + '.objects'
    
    with open(objectName) as f:
        content = f.read().splitlines()
        pythonObjects.append([i.split(' ') for i in content])

def createSprite(spriteName):
    objectValues = ['movable', 'solid', 'animated', 'selfMoving', 'moveWithKeys', 'wander', 'movingSpaceX', 'movingSpaceY', 'movingDirection', 'currentSprite', 'animatedSpeed', 'sizeX', 'sizeY', 'spriteSheetSizeX', 'spriteSheetSizeY', 'cameraFocus']
    objectLines = ['spriteOrder', 'path', 'extraInfo']

    spriteFile = './gamemaps/' + spriteName + '.object'
    
    with open(spriteFile) as f:
        content = f.read()

        spriteF = open('./build/' + spriteName  + '.sprite', 'w+b')
        spriteID = hashlib.md5(spriteName.encode()).hexdigest()
        spriteF.write(spriteID);
        spriteF.write(spriteName + '\n');

        for value in objectValues:
            startPlace = content.find(value);
            endPlace = content.find('\n', startPlace)
            addToFile = int(content[startPlace + len(value) + 1:endPlace].strip())
            spriteF.write(struct.pack("i", addToFile))

        startPlace = content.find('spriteSheetPlace');
        endPlace = content.find('\n', startPlace)
        addToFile = content[startPlace + len('spriteSheetPlace') + 1:endPlace].strip()
        spriteF.write('\n' + addToFile + '\n')

        for value in objectLines:
            startPlace = content.find(value);
            endPlace = content.find('\n', startPlace)
            foundString = content[startPlace + len(value) + 1:endPlace].strip()

            if foundString != '-':
                addToFile = (foundString).split(',')
                for x in addToFile:
                    spriteF.write(struct.pack("i", int(x)))
            
            spriteF.write('\n')
        spriteF.close()

        return spriteID

for level in xrange(0, len(mapNames)):
    f = open('./build/' + mapNames[level] + '.level', 'w+b')
    sizeY = len(pythonMaps[level])
    sizeX = len(pythonMaps[level][0])
    
    f.write(struct.pack("H", sizeX))
    f.write(struct.pack("H", sizeY))
    f.write(mapNames[level] + '\n')

    objects = {'maps':{}, 'layers':{}, 'sprites':{}};

    for j in xrange(sizeX):
        for i in xrange(sizeY):
            if pythonMaps[level][i][j] != '0':
                objectVal = pythonMaps[level][i][j]
                if not (objectVal in objects['maps']):
                    objects['maps'][objectVal] = []
                objects['maps'][objectVal].append([i, j])
            
            if pythonLayers[level][i][j] != '0':
                objectVal = pythonLayers[level][i][j]
                if not (objectVal in objects['layers']):
                    objects['layers'][objectVal] = []
                objects['layers'][objectVal].append([i, j])

            if pythonObjects[level][i][j] != '0':
                objectVal = pythonObjects[level][i][j]
                if not (objectVal in objects['sprites']):
                    spriteID = createSprite(objectVal);
                    objects['sprites'][objectVal] = {'id': spriteID, 'coords': []}

                objects['sprites'][objectVal]['coords'].append([i, j])

    for id in objects['maps']:
        f.write(struct.pack("H", 0))
        f.write(struct.pack("I", int(id)))
        f.write(struct.pack("H", len(objects['maps'][id])))

        for coord in objects['maps'][id]:
            f.write(struct.pack("H", int(coord[0])))
            f.write(struct.pack("H", int(coord[1])))

    for id in objects['layers']:
        f.write(struct.pack("H", 1))
        f.write(struct.pack("I", int(id)))
        f.write(struct.pack("H", len(objects['layers'][id])))

        for coord in objects['layers'][id]:
            f.write(struct.pack("H", int(coord[0])))
            f.write(struct.pack("H", int(coord[1])))

    for id in objects['sprites']:
        f.write(struct.pack("H", 2))
        f.write(objects['sprites'][id]['id'])
        f.write(struct.pack("H", len(objects['sprites'][id]['coords'])))

        for coord in objects['sprites'][id]['coords']:
            f.write(struct.pack("H", int(coord[0])))
            f.write(struct.pack("H", int(coord[1])))

    f.close()
