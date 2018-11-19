#ifndef CONTROLLER_H
#define CONTROLLER_H

#include <vector>
#include <SFML/Graphics.hpp>

#include "../gameObjects/object.hpp"

class GameMap;

class GameController
{
	public:
	
	std::vector<sf::Texture*> textureVector;
	std::vector<std::string> textureVectorString;
	
	GameMap *currentMapObject;
	std::vector<GameObject*> gameObjects;
	
	sf::RenderWindow &window;
  sf::View characterView;
	
	GameController(sf::RenderWindow &window);
	
	int findTexture(std::string textureName);
	
  bool loadMap(
    std::string fileName,
    std::vector<std::vector<int>> &bgVector,
    std::vector<std::vector<int>> &fgVector,
    std::vector<std::vector<std::vector<GameObject*>>>
  );
  
	bool drawMap();
	bool updateSprites();
	
	bool getKeyPress(int keyValue);
};

#endif
