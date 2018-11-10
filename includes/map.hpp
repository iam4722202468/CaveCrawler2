#ifndef MAP_H
#define MAP_H

#include <vector>
#include <SFML/Graphics.hpp>

#include "drawMap.hpp"
#include "../gameClasses/object.hpp"
#include "controller.hpp"

class MapSprites;
class GameController;

class GameMap
{
	sf::RenderWindow &window;
	GameController *game;
	
	public:
	
	MapSprites *mapSprites;
	
	std::vector<std::vector<int>> currentMap;
	std::vector<std::vector<int>> currentLayer;
	std::vector<std::vector<int>> currentObjects;
	
	bool setMap(std::vector<std::vector<int>> &mapVector);
	bool setLayer(std::vector<std::vector<int>> &layerVector);
	bool setObjects(std::vector<std::vector<int>> &objectVector);
	
	bool drawCurrentMap(std::vector<GameObject*> &gameObjects);
	
	GameMap(GameController *game, sf::RenderWindow &window);
};

#endif
