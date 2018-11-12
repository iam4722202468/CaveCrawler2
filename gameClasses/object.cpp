#include <SFML/Graphics.hpp>
#include "object.hpp"
#include "../includes/controller.hpp"

void getGameObjectProps(GameObject *gameObject, GameObjectProps gameObjectProps) {
  gameObject->classType = gameObjectProps.classType;
  gameObject->spriteSheet = gameObjectProps.spriteSheet;
  gameObject->placeX = gameObjectProps.placeX;
  gameObject->placeY = gameObjectProps.placeY;
  gameObject->movable = gameObjectProps.movable;
  gameObject->solid = gameObjectProps.solid;
  gameObject->animated = gameObjectProps.animated;
  gameObject->selfMoving = gameObjectProps.selfMoving;
  gameObject->moveWithKeys = gameObjectProps.moveWithKeys;
  gameObject->wander = gameObjectProps.wander;
  gameObject->movingSpaceX = gameObjectProps.movingSpaceX;
  gameObject->movingSpaceY = gameObjectProps.movingSpaceY;
  gameObject->movingDirection = gameObjectProps.movingDirection;
  gameObject->currentSprite = gameObjectProps.currentSprite;
  gameObject->animatedSpeed = gameObjectProps.animatedSpeed;
  gameObject->sizeX = gameObjectProps.sizeX;
  gameObject->sizeY = gameObjectProps.sizeY;
  gameObject->spriteSheetSizeX = gameObjectProps.spriteSheetSizeX;
  gameObject->spriteSheetSizeY = gameObjectProps.spriteSheetSizeY;
  gameObject->cameraFocus = gameObjectProps.cameraFocus;
}

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
  bool cameraFocus) {
    GameObjectProps toReturn;

    toReturn.classType = classType;
    toReturn.spriteSheet = spriteSheet;
    toReturn.placeX = placeX;
    toReturn.placeY = placeY;
    toReturn.movable = movable;
    toReturn.solid = solid;
    toReturn.animated = animated;
    toReturn.selfMoving = selfMoving;
    toReturn.moveWithKeys = moveWithKeys;
    toReturn.wander = wander;
    toReturn.movingSpaceX = movingSpaceX;
    toReturn.movingSpaceY = movingSpaceY;
    toReturn.movingDirection = movingDirection;
    toReturn.currentSprite = currentSprite;
    toReturn.animatedSpeed = animatedSpeed;
    toReturn.sizeX = sizeX;
    toReturn.sizeY = sizeY;
    toReturn.spriteSheetSizeX = spriteSheetSizeX;
    toReturn.spriteSheetSizeY = spriteSheetSizeY;
    toReturn.cameraFocus = cameraFocus;

    return toReturn;
}

//controls movement of sprits
MovingObject::MovingObject(GameController *game, sf::Sprite &sprite, int sizeX, int sizeY, int spriteSheetSizeX, int &currentSprite, int &addedX, int &addedY, int &placeX, int &placeY, std::vector<int> &spriteOrder, int &animatedSpeed, int animationNumber, bool cameraFocus) :
  sprite(sprite),
  sizeX(sizeX),
  sizeY(sizeY),
  spriteSheetSizeX(spriteSheetSizeX),
  currentSprite(currentSprite),
  addedX(addedX),
  addedY(addedY),
  placeX(placeX),
  placeY(placeY),
  spriteOrder(spriteOrder),
  animatedSpeed(animatedSpeed),
  animationNumber(animationNumber),
  cameraFocus(cameraFocus),
  game(game)
{
}

void convertTo2f(int toConvert, sf::Vector2f &moveVector)
{
  switch(toConvert)
  {
    case 1:
      moveVector.x = 0; moveVector.y = -1;
      break;
    case 2:
      moveVector.x = -1; moveVector.y = 0;
      break;
    case 3:
      moveVector.x = 0; moveVector.y = 1;
      break;
    case 4:
      moveVector.x = 1; moveVector.y = 0;
      break;
  }
}

bool MovingObject::updateInfo(sf::Vector2f direction, sf::Vector2f directionBuffer)
{
  directionCoordBuffer = directionBuffer;
  directionCoord = direction;
  frameCounter = 0;
  return true;
}

void drawSprite(GameController *game, sf::Sprite &sprite, int spriteSheetSizeX, int sizeX, std::vector<int> &spriteOrder, int currentSprite, int sizeY, bool cameraFocus)
{

  int tu = spriteOrder[currentSprite] % (spriteSheetSizeX / sizeX);
  int tv = spriteOrder[currentSprite] / (spriteSheetSizeX / sizeX);

  sprite.setTextureRect(sf::IntRect(tu*sizeX, tv*sizeY, sizeX, sizeY));
}

bool MovingObject::updateMoving()
{
  //std::cout << frameCounter << " " << animatedSpeed/animationNumber << " " << frameCounter % (animatedSpeed/animationNumber) << std::endl;
  
  if (cameraFocus) {
    game->characterView.setCenter(sprite.getPosition());
  }

  addedX = (frameCounter/(float)animatedSpeed)*mapTileY*directionCoord.x;
  addedY = (frameCounter/(float)animatedSpeed)*mapTileY*directionCoord.y;
  
  if(frameCounter % (animatedSpeed/(animationNumber-1)) == 0)
  {
    currentSprite++;
    
    if(currentSprite % animationNumber == 0 && frameCounter != 0)
    {
      currentSprite -= animationNumber;

      if (directionCoordBuffer.x == directionCoord.x
        && directionCoordBuffer.y == directionCoord.y) {
        directionCoordBuffer.x = 0;
        directionCoordBuffer.y = 0;
        currentSprite++;
      }
    }
    
    drawSprite(game, sprite, spriteSheetSizeX, sizeX, spriteOrder, currentSprite, sizeY, cameraFocus);
  }
  
  if(frameCounter == animatedSpeed)
  {
    addedX = 0; addedY = 0;
    return true;
  }
  
  frameCounter++;
  return false;
}

//create game object
GameObject::GameObject(
  GameController *game,
  sf::RenderWindow& window,
  std::vector<GameObject*> &gameObjects,
  std::vector<std::vector<int>> &currentObjects,
  std::vector<int> spriteOrder_,
  std::vector<int> path,
  std::vector<int> extraInfo,
  GameObjectProps gameObjectProps) :
    game(game),
    window(window),
    gameObjects(gameObjects),
    currentObjects(currentObjects),
    spriteOrder(spriteOrder_),
    path(path),
    extraInfo(extraInfo)
{
  // Self moving counter
  internalVariablesInt.push_back(0);

  getGameObjectProps(this, gameObjectProps);

  int tu = spriteOrder[currentSprite] % (spriteSheet->getSize().x / sizeX);
  int tv = spriteOrder[currentSprite] / (spriteSheet->getSize().x / sizeX);
  
  sprite.setTextureRect(sf::IntRect(tu*sizeX, tv*sizeY, sizeX, sizeY));
  sprite.setPosition(sf::Vector2f(placeX*mapTileX, placeY*mapTileY));
  sprite.setScale((float)mapTileX/sizeX, (float)mapTileY/sizeY);
  
  sprite.setTexture(*spriteSheet);
  
  movingObject = new MovingObject(
    game,
    sprite,
    sizeX,
    sizeY,
    spriteSheetSizeX,
    currentSprite,
    addedX,
    addedY,
    placeX,
    placeY,
    spriteOrder,
    animatedSpeed,
    spriteSheet->getSize().x / sizeX,
    cameraFocus);
  
  thisID = currentObjects[placeY][placeX];
  
  if(movingDirection != 0)
  {
    isMoving = true;
    startMoving(movingDirection);
  }
}

void printVector(std::vector<std::vector<int>> &vectorPrint)
{
  for(int x = 0; x < vectorPrint.size(); x++)
  {
    for(int y = 0; y < vectorPrint[0].size(); y++)
      std::cout << vectorPrint[x][y];
    std::cout << std::endl;
  }
}

bool GameObject::update(GameController *game) {
  if (selfMoving && !isMoving) {
    if (internalVariablesInt.at(0) < 4) {
      startMoving(2);
    } else if (internalVariablesInt.at(0) < 8) {
      startMoving(3);
    } else if (internalVariablesInt.at(0) < 12) {
      startMoving(4);
    } else if (internalVariablesInt.at(0) < 16) {
      startMoving(1);
    } else {
      startMoving(2);
      internalVariablesInt.at(0) = 0;
    }

    internalVariablesInt.at(0)++;
  }

  return true;
}

bool GameObject::drawObject(GameController *game)
{
  if (cameraFocus) {
    game->characterView.setCenter(sprite.getPosition());
  }

  if(isMoving)
    if(movingObject->updateMoving())
    {
      isMoving = false;
      movingDirection = 0;
      
      thisID = currentObjects[placeY][placeX];
      
      currentObjects[placeY][placeX] = valueUnderThis;
      placeX += movingObject->directionCoord.x;
      placeY += movingObject->directionCoord.y;
      
      valueUnderThis = currentObjects[placeY][placeX];
      currentObjects[placeY][placeX] = thisID;
    }
  
  if(animated) {
    if(frameCounter % (animatedSpeed/(spriteOrder.size()-1)) == 0) {
      currentSprite++;
      
      if(currentSprite == spriteOrder.size()) {
        currentSprite -= spriteOrder.size();
      }
      
      drawSprite(game, sprite, spriteSheetSizeX, sizeX, spriteOrder, currentSprite, sizeY, cameraFocus);
    }
    
    if(frameCounter > animatedSpeed) {
      frameCounter = 0;
    }
      
    frameCounter++;
  }
  sprite.setPosition(sf::Vector2f(placeX*mapTileX + addedX, placeY*mapTileY + addedY));
  window.draw(sprite);
  return true;
}

bool Wall::onContact(GameObject *contacted) //takes object values for object that comes in contact with it
{
  //std::cout << "MOO" << std::endl;
  return false;
}

bool Default::onContact(GameObject *contacted)
{
  if(solid) {
    return false;
  }
  return true;
}

bool GameObject::checkConflict(sf::Vector2f directionCoord)
{
  int standingOn = currentObjects[placeY+directionCoord.y][placeX+directionCoord.x];
  
  if(standingOn != 0) {
    for(int x = 0; x < gameObjects.size(); x++) {
      if(standingOn == gameObjects[x]->thisID) {
        if(!gameObjects[x]->onContact(this)) {
          return true;
        }
      }
    }
  }
  
  return false;
}

bool GameObject::startMoving(int direction)
{
  currentSprite = (spriteSheetSizeX / sizeX) * (direction-1);
  drawSprite(game, sprite, spriteSheetSizeX, sizeX, spriteOrder, currentSprite, sizeY, cameraFocus);
  
  sf::Vector2f directionCoord;
  sf::Vector2f directionCoordBuffer;

  convertTo2f(direction, directionCoord);
  convertTo2f(direction, directionCoordBuffer);

  if(!checkConflict(directionCoord))
  {
    isMoving = true;
    movingDirection = direction;
    movingObject->updateInfo(directionCoord, directionCoordBuffer);
    return true;
  }
  return false;
}
