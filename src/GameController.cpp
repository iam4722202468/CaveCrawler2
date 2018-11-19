#include <vector>
#include <SFML/Graphics.hpp>

#include <fstream>
#include <iostream>

#include "GameController.hpp"
#include "stringStuff.hpp" //for split string
#include "../gameObjects/object.hpp"

GameController::GameController(sf::RenderWindow &window):
	window(window)
{
  characterView.zoom(0.65f);
}

//(1,2,3,4) <- up left down right
bool GameController::getKeyPress(int keyValue)
{
	return true;
}

bool GameController::drawMap() {
  return true;
}

bool GameController::loadMap(
    std::string fileName,
    std::vector<std::vector<int>> &bgVector,
    std::vector<std::vector<int>> &fgVector,
    std::vector<std::vector<std::vector<GameObject*>>>
  ) {
  std::ifstream levelFile;
  levelFile.open(fileName + ".level", std::ios::binary | std::ios::in);

  levelFile.seekg(0, std::ios::end);
  int fileSize=(int) levelFile.tellg();
  levelFile.seekg(0, std::ios::beg);

  short sizeX, sizeY;
  std::string fileTitle;

  levelFile.read((char*)&sizeX, 2);
  levelFile.read((char*)&sizeY, 2);
  getline(levelFile, fileTitle, '\n');
  
  while (levelFile.tellg() < fileSize) {
    int fileID;
    short entryType;
    short coordLength;
    levelFile.read((char*)&entryType, 2);

    if (entryType == 2) {
      break;
    }

    levelFile.read((char*)&fileID, 4);
    levelFile.read((char*)&coordLength, 2);

    short coordX, coordY;
    for (int place = 0; place < coordLength; ++place) {
      levelFile.read((char*)&coordX, 2);
      levelFile.read((char*)&coordY, 2);
    }
  }
  return true;
}

bool GameController::updateSprites() {
  return true;
}
