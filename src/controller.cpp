#include <vector>
#include <SFML/Graphics.hpp>

#include "controller.hpp"
#include "map.hpp"
#include "stringStuff.hpp" //for split string
#include "../gameClasses/object.hpp"

//(1,2,3,4) <- up left down right

bool GameController::getKeyPress(int keyValue)
{
	for(int x = 0; x < gameObjects.size(); x++)
	{
		if(gameObjects[x]->moveWithKeys && !gameObjects[x]->isMoving)
		{
			if(keyValue == 73) //up
				gameObjects[x]->startMoving(1);
			else if(keyValue == 71) //left
				gameObjects[x]->startMoving(2);
			else if(keyValue == 74) //down
				gameObjects[x]->startMoving(3);
			else if(keyValue == 72) //right
				gameObjects[x]->startMoving(4);
		}
	}
	return true;
}

//pass map to map object
bool GameController::setMap(std::vector<std::vector<int>> &mapVector)
{
	currentMapObject->setMap(mapVector);
	return true;
}

void stringVectorToInt(std::vector<std::string> &stringVector, std::vector<int> &intVector)
{
	for(int x = 0; x < stringVector.size(); x++)
		intVector.push_back(std::stoi(stringVector[x]));
}

int GameController::findTexture(std::string textureName)
{
	for(int x = 0; x < textureVectorString.size(); x++)
		if(textureVectorString[x] == textureName)
			return x;
	return -1;
}

//parse object info and create object
bool GameController::generateObjects(std::vector<std::vector<std::string>> &objectInfo)
{
	for(int x = 0; x < currentMapObject->currentObjects.size(); x++)
	{
		for(int y = 0; y < currentMapObject->currentObjects[0].size(); y++)
		{
			if(currentMapObject->currentObjects[x][y] > 0)
			{
				int objectValue = currentMapObject->currentObjects[x][y] - 1;
				
				std::vector<std::string> tempSplit;
				std::vector<int> tempInt;
				
				std::vector<int> spriteOrder; //16
				std::vector<int> path; //17
				std::vector<int> extraInfo; //18
				bool cameraFocus; //19
				
				stringsplit(',', objectInfo[objectValue][16], tempSplit);
				stringVectorToInt(tempSplit, spriteOrder);
				
				if(objectInfo[objectValue][17] != "-")
				{
					stringsplit(',', objectInfo[objectValue][17], tempSplit);
					stringVectorToInt(tempSplit, path);
				}
				
				if(objectInfo[objectValue][18] != "-")
				{
					stringsplit(',', objectInfo[objectValue][18], tempSplit);
					stringVectorToInt(tempSplit, extraInfo);
				}

        cameraFocus = objectInfo[objectValue][19] == "1";

				std::string spriteSheetPlace = objectInfo[objectValue][15];
				
				objectInfo[objectValue].pop_back();
				objectInfo[objectValue].pop_back();
				objectInfo[objectValue].pop_back();
				objectInfo[objectValue].pop_back();
				objectInfo[objectValue].pop_back();
				
				stringVectorToInt(objectInfo[objectValue], tempInt);
				
				int textureAt = findTexture(spriteSheetPlace);
				
				if(textureAt == -1)
				{
					textureVector.push_back(new sf::Texture());
					textureVectorString.push_back(spriteSheetPlace);
					textureAt = textureVector.size()-1;
					
					if (!textureVector[textureAt]->loadFromFile("resources/" + spriteSheetPlace, sf::IntRect(0, 0, tempInt[13], tempInt[14])))
						std::cout << "Error " << EXIT_FAILURE << " loading sprite";
					std::cout << "sprite created" << std::endl;
				}
				
				if(extraInfo.size() > 0 && extraInfo[0] == 1) {
					gameObjects.push_back(
            new Wall(
              this,
              window,
              gameObjects,
              "Wall",
              currentMapObject->currentObjects,
              textureVector[textureAt],
              y, x,
              tempInt[0], tempInt[1], tempInt[2],
              tempInt[3], tempInt[4], tempInt[5],
              tempInt[6], tempInt[7], tempInt[8], 
              tempInt[9], tempInt[10], tempInt[11],
              tempInt[12], tempInt[13], tempInt[14],
              spriteOrder, path, extraInfo, cameraFocus
            ));
          } else {
            gameObjects.push_back(
              new Default(
                this,
                window,
                gameObjects,
                "GameObject",
                currentMapObject->currentObjects,
                textureVector[textureAt],
                y, x,
                tempInt[0], tempInt[1], tempInt[2],
                tempInt[3], tempInt[4], tempInt[5],
                tempInt[6], tempInt[7], tempInt[8],
                tempInt[9], tempInt[10], tempInt[11],
                tempInt[12], tempInt[13], tempInt[14],
                spriteOrder, path, extraInfo, cameraFocus
              ));
          }
      }
		}
	}
}

bool GameController::setLayer(std::vector<std::vector<int>> &layerVector)
{
	currentMapObject->setLayer(layerVector);
	return true;
}

bool GameController::setObjects(std::vector<std::vector<int>> &objectVector)
{
	currentMapObject->setObjects(objectVector);
	return true;
}

bool GameController::drawCurrentMap()
{
	currentMapObject->drawCurrentMap(gameObjects);
	return true;
}

GameController::GameController(sf::RenderWindow &window):
	window(window)
{
	currentMapObject = new GameMap(this, window);
}
