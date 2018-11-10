#include <SFML/Graphics.hpp>

#include "map.hpp"
#include "drawMap.hpp"
#include "../gameClasses/object.hpp"

bool GameMap::setMap(std::vector<std::vector<int>> &mapVector)
{
	mapSprites->loadMap(mapVector, false);
	currentMap = mapVector;
	return true;
}

bool GameMap::setLayer(std::vector<std::vector<int>> &layerVector)
{
	mapSprites->loadMap(layerVector, true);
	currentLayer = layerVector;
	return true;
}

bool GameMap::setObjects(std::vector<std::vector<int>> &objectVector)
{
	//mapSprites->loadMap(layerVector, true);
	currentObjects = objectVector;
	return true;
}

bool GameMap::drawCurrentMap(std::vector<GameObject*> &gameObjects)
{
	mapSprites->drawMap(game, gameObjects);
}

//create game map and mapSprites (which draws map)
GameMap::GameMap(GameController *game, sf::RenderWindow &window) :
	window(window),
  game(game)
{
	mapSprites = new MapSprites(window);
}
