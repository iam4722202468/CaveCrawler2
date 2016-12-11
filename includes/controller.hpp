#ifndef CONTROLLER_H
#define CONTROLLER_H

#include <vector>
#include <SFML/Graphics.hpp>

#include "map.hpp"
#include "../gameClasses/object.hpp"

class GameMap;

class GameController
{
	public:
	
	std::vector<sf::Texture*> textureVector;
	std::vector<std::string> textureVectorString;
	
	GameMap *currentMapObject;
	std::vector<GameObject*> gameObjects;
	
	sf::RenderWindow &window;
	
	GameController(sf::RenderWindow &window);
	
	int findTexture(std::string textureName);
	bool setMap(std::vector<std::vector<int>> &mapVector);
	bool setLayer(std::vector<std::vector<int>> &layerVector);
	bool setObjects(std::vector<std::vector<int>> &objectVector);
	
	bool generateObjects(std::vector<std::vector<std::string>> &objectInfo);
	bool drawCurrentMap();
	
	bool getKeyPress(int keyValue);
};

#endif
