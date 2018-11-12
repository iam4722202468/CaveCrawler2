#ifndef OBJECT_H
#define OBJECT_H

#include <iostream>
#include <vector>
#include <SFML/Graphics.hpp>

class GameController;
class GameObject;

struct GameObjectProps {
  std::string classType;
  sf::Texture *spriteSheet;
  int placeX;
  int placeY;
  bool movable;
  bool solid;
  bool animated;
  bool selfMoving;
  bool moveWithKeys;
  bool wander;
  int movingSpaceX;
  int movingSpaceY;
  int movingDirection;
  int currentSprite;
  int animatedSpeed;
  int sizeX;
  int sizeY;
  int spriteSheetSizeX;
  int spriteSheetSizeY;
  bool cameraFocus;
};

void getGameObjectProps(GameObject *gameObject, GameObjectProps gameObjectProps);

GameObjectProps setGameObjectProps(
  sf::Texture *spriteSheet,
  std::string classType,
  int placeX,
  int placeY,
  bool movable,
  bool solid,
  bool animated,
  bool selfMoving,
  bool moveWithKeys,
  bool wander,
  int movingSpaceX,
  int movingSpaceY,
  int movingDirection,
  int currentSprite,
  int animatedSpeed,
  int sizeX,
  int sizeY,
  int spriteSheetSizeX,
  int spriteSheetSizeY,
  bool cameraFocus);

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
  bool cameraFocus;
  GameController *game;
	
	public:
	
	sf::Vector2f directionCoord;
	sf::Vector2f directionCoordBuffer;
	
	MovingObject(GameController *game,
    sf::Sprite &sprite,
    int sizeX,
    int sizeY,
    int spriteSheetSizeX,
    int &currentSprite,
    int &addedX,
    int &addedY,
    int &placeX,
    int &placeY,
    std::vector<int> &spriteOrder,
    int &animatedSpeed,
    int animationNumber,
    bool cameraFocus);
	
	bool updateInfo(sf::Vector2f direction, sf::Vector2f directionBuffer);
	bool updateMoving();
};

class GameObject;

class GameObject
{
  GameController *game;
	sf::RenderWindow& window;
	sf::Sprite sprite;
	
	int mapTileX = 32;
	int mapTileY = 32;
	
	public:
	
  std::vector<int> internalVariablesInt;
  std::vector<std::string> internalVariablesString;

	int frameCounter = 0;
	int animationNumber = 0;
	
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

  sf::Texture *spriteSheet  ;

	bool wander;
	
	int movingSpaceX; //area it can move in the x direction when wandering (towards either side)
	int movingSpaceY;
	
	int movingDirection;
	int currentSprite;
	
	int animatedSpeed;
  bool cameraFocus;
	
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
	
	int thisID;
	std::string classType;
	
	virtual bool onContact(GameObject *contacted) = 0;
	
	GameObject(GameController *game,
    sf::RenderWindow& window,
    std::vector<GameObject*> &gameObjects,
    std::vector<std::vector<int>> &currentObjects,
    std::vector<int> spriteOrder,
    std::vector<int> path,
    std::vector<int> extraInfo,
    GameObjectProps gameObjectProps
  );

  bool drawObject(GameController *game);
  bool update(GameController *game);
	
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
	
	Wall(GameController *game,
    sf::RenderWindow& window,
    std::vector<GameObject*> &gameObjects,
    std::vector<std::vector<int>> &currentObjects,
    std::vector<int> spriteOrder,
    std::vector<int> path,
    std::vector<int> extraInfo,
    GameObjectProps gameObjectProps
  ) :
		GameObject(game,
      window,
      gameObjects,
      currentObjects,
      spriteOrder,
      path,
      extraInfo,
      gameObjectProps
    ) { getGameObjectProps(this, gameObjectProps); }
};

class Default : public GameObject
{
	public:
	bool onContact(GameObject *contacted) override;
	
	Default(GameController *game,
    sf::RenderWindow& window,
    std::vector<GameObject*> &gameObjects,
    std::vector<std::vector<int>> &currentObjects,
    std::vector<int> spriteOrder,
    std::vector<int> path,
    std::vector<int> extraInfo,
    GameObjectProps gameObjectProps
  ) :
		GameObject(game,
      window,
      gameObjects,
      currentObjects,
      spriteOrder,
      path,
      extraInfo,
      gameObjectProps
    ) { getGameObjectProps(this, gameObjectProps); }

};

#endif
