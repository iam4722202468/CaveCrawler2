#ifndef OBJECT_H
#define OBJECT_H

#include <iostream>
#include <vector>
#include <SFML/Graphics.hpp>

class GameController;
class GameObject;

class GameObject
{
	virtual bool onContact(GameObject *contacted) = 0;

	GameObject(GameController *game, sf::RenderWindow& window);
};

#endif
