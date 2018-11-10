#ifndef DRAWMAP_H
#define DRAWMAP_H

#include <vector>
#include <SFML/Graphics.hpp>

#include "../gameClasses/object.hpp"
#include "controller.hpp"

static std::vector<std::vector<int>> DEFAULT_VECTOR;

class GameController;

class MapSprites {
	sf::RenderWindow &window;
	sf::Texture mainSheet;
	
	public:
	
	sf::VertexArray mapTiles;
	sf::VertexArray layerTiles;
	
	MapSprites(sf::RenderWindow &window);
	
	bool drawMap(GameController *game, std::vector<GameObject*> &gameObjects);
	bool loadMap(std::vector<std::vector<int>> &toLoadMapVector, bool isLayer);
};

#endif
