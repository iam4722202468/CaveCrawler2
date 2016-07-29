#ifndef OBJECT_H
#define OBJECT_H

#include <iostream>
#include <vector>
#include <SFML/Graphics.hpp>

class MovingObject
{
	int mapTileX = 32;
	int mapTileY = 32;
	
	int frameCounter = 0;
	
	int animationNumber;
	
	int &addedX, &addedY;
	int &placeX, &placeY; //set new place in this
	int &animatedSpeed;
	
	sf::Sprite &sprite;
	std::vector<int> &spriteOrder;
	
	int sizeX, sizeY;
	int spriteSheetSizeX;
	
	int &currentSprite;
	
	public:
	
	sf::Vector2f directionCoord;
	
	MovingObject(sf::Sprite &sprite, int sizeX, int sizeY, int spriteSheetSizeX, int &currentSprite, int &addedX, int &addedY, int &placeX, int &placeY, std::vector<int> &spriteOrder, int &animatedSpeed, int animationNumber);
	
	bool updateInfo(sf::Vector2f direction);
	bool updateMoving();
};

class GameObject;

class GameObject
{
	sf::RenderWindow& window;
	sf::Sprite sprite;
	
	int mapTileX = 32;
	int mapTileY = 32;
	
	protected:
	
	std::vector<std::vector<int>> &currentObjects; //2d vector of object map
	
	std::vector<GameObject*> chestObjects;
	std::vector<GameObject*> &gameObjects; //actual game object array
	
	int addedX = 0, addedY = 0;
	int placeX, placeY;
	
	int valueUnderThis = 0; //track other objects this passes over
	
	MovingObject *movingObject;
	
	bool movable; //player can push
	bool solid;
	bool animated;
	
	bool selfMoving;
	//bool moveWithKeys;
	bool wander;
	
	int movingSpaceX; //area it can move in the x direction when wandering (towards either side)
	int movingSpaceY;
	
	int movingDirection;
	int currentSprite;
	
	int animatedSpeed;
	
	int sizeX;				//size of sprite
	int sizeY;
	int spriteSheetSizeX;	//size of sprite sheet
	int spriteSheetSizeY;
	
	std::vector<int> spriteOrder; //when moveWithKeys, becomes walking spritemap
	/*	Up    : 0,1,2
	 *	Left  : 3,4,5
	 *	Down  : 6,7,8
	 *	Right : 9,10,11
	 */
	
	std::vector<int> path; //path to follow when walking (1,2,3,4) <- up left down right
	std::vector<int> extraInfo;
	
	bool checkConflict(sf::Vector2f directionCoord);
	
	public:
	int thisID;
	std::string classType;
	
	virtual bool onContact(GameObject *contacted) = 0;
	
	GameObject(sf::RenderWindow& window, std::vector<GameObject*> &gameObjects, std::string classType, std::vector<std::vector<int>> &currentObjects, sf::Texture *spriteSheet, int placeX, int placeY, bool movable, bool solid, bool animated, bool selfMoving, bool moveWithKeys, bool wander, int movingSpaceX, int movingSpaceY, int movingDirection, int currentSprite, int animatedSpeed, int sizeX, int sizeY, int spriteSheetSizeX, int spriteSheetSizeY, std::vector<int> spriteOrder, std::vector<int> path, std::vector<int> extraInfo);
	bool drawObject();
	
	//bool updateSprite();
	
	bool isMoving = false;
	bool moveWithKeys;
	
	bool startMoving(int direction);	//start moving in direction of travel
	
	//bool keyInput();
};

class Wall : public GameObject
{
	public:
	bool onContact(GameObject *contacted) override;
	
	Wall(sf::RenderWindow& window, std::vector<GameObject*> &gameObjects, std::string classType, std::vector<std::vector<int>> &currentObjects, sf::Texture *spriteSheet, int placeX, int placeY, bool movable, bool solid, bool animated, bool selfMoving, bool moveWithKeys, bool wander, int movingSpaceX, int movingSpaceY, int movingDirection, int currentSprite, int animatedSpeed, int sizeX, int sizeY, int spriteSheetSizeX, int spriteSheetSizeY, std::vector<int> spriteOrder, std::vector<int> path, std::vector<int> extraInfo) :
		GameObject(window, gameObjects, classType, currentObjects, spriteSheet, placeX, placeY, movable, solid, animated, selfMoving, moveWithKeys, wander, movingSpaceX, movingSpaceY,  movingDirection, currentSprite, animatedSpeed, sizeX, sizeY, spriteSheetSizeX, spriteSheetSizeY, spriteOrder, path, extraInfo) {}
};

class Default : public GameObject
{
	public:
	bool onContact(GameObject *contacted) override {return true;}
	
	Default(sf::RenderWindow& window, std::vector<GameObject*> &gameObjects, std::string classType, std::vector<std::vector<int>> &currentObjects, sf::Texture *spriteSheet, int placeX, int placeY, bool movable, bool solid, bool animated, bool selfMoving, bool moveWithKeys, bool wander, int movingSpaceX, int movingSpaceY, int movingDirection, int currentSprite, int animatedSpeed, int sizeX, int sizeY, int spriteSheetSizeX, int spriteSheetSizeY, std::vector<int> spriteOrder, std::vector<int> path, std::vector<int> extraInfo) :
		GameObject(window, gameObjects, classType, currentObjects, spriteSheet, placeX, placeY, movable, solid, animated, selfMoving, moveWithKeys, wander, movingSpaceX, movingSpaceY,  movingDirection, currentSprite, animatedSpeed, sizeX, sizeY, spriteSheetSizeX, spriteSheetSizeY, spriteOrder, path, extraInfo) {}

};

#endif
