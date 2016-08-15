#include <SFML/Graphics.hpp>
#include "object.hpp"

//controls movement of sprits
MovingObject::MovingObject(sf::Sprite &sprite, int sizeX, int sizeY, int spriteSheetSizeX, int &currentSprite, int &addedX, int &addedY, int &placeX, int &placeY, std::vector<int> &spriteOrder, int &animatedSpeed, int animationNumber) :
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
	animationNumber(animationNumber)
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

bool MovingObject::updateInfo(sf::Vector2f direction)
{
	directionCoord = direction;
	frameCounter = 0;
	return true;
}

void drawSprite(sf::Sprite &sprite, int spriteSheetSizeX, int sizeX, std::vector<int> &spriteOrder, int currentSprite, int sizeY)
{
	int tu = spriteOrder[currentSprite] % (spriteSheetSizeX / sizeX);
	int tv = spriteOrder[currentSprite] / (spriteSheetSizeX / sizeX);
	
	sprite.setTextureRect(sf::IntRect(tu*sizeX, tv*sizeY, sizeX, sizeY));
}

bool MovingObject::updateMoving()
{
	//std::cout << frameCounter << " " << animatedSpeed/animationNumber << " " << frameCounter % (animatedSpeed/animationNumber) << std::endl;
	
	addedX = (frameCounter/(float)animatedSpeed)*mapTileY*directionCoord.x;
	addedY = (frameCounter/(float)animatedSpeed)*mapTileY*directionCoord.y;
	
	if(frameCounter % (animatedSpeed/(animationNumber-1)) == 0)
	{
		currentSprite++;
		
		if(currentSprite % animationNumber == 0 && frameCounter != 0)
			currentSprite -= animationNumber;
		
		drawSprite(sprite, spriteSheetSizeX, sizeX, spriteOrder, currentSprite, sizeY);
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
GameObject::GameObject(sf::RenderWindow& window, std::vector<GameObject*> &gameObjects, std::string classType, std::vector<std::vector<int>> &currentObjects, sf::Texture *spriteSheet, int placeX_, int placeY_, bool movable, bool solid, bool animated, bool selfMoving, bool moveWithKeys, bool wander, int movingSpaceX, int movingSpaceY, int movingDirection, int currentSprite_, int animatedSpeed_, int sizeX, int sizeY, int spriteSheetSizeX, int spriteSheetSizeY, std::vector<int> spriteOrder_, std::vector<int> path, std::vector<int> extraInfo) :
	window(window),
	gameObjects(gameObjects),
	classType(classType),
	currentObjects(currentObjects),
	placeX(placeX_),
	placeY(placeY_),
	movable(movable),
	solid(solid),
	animated(animated),
	selfMoving(selfMoving),
	moveWithKeys(moveWithKeys),
	wander(wander),
	movingSpaceX(movingSpaceX),
	movingSpaceY(movingSpaceY),
	movingDirection(movingDirection),
	currentSprite(currentSprite_),
	animatedSpeed(animatedSpeed_),
	sizeX(sizeX),
	sizeY(sizeY),
	spriteSheetSizeX(spriteSheetSizeX),
	spriteSheetSizeY(spriteSheetSizeY),
	spriteOrder(spriteOrder_),
	path(path),
	extraInfo(extraInfo)
{
	int tu = spriteOrder[currentSprite] % (spriteSheet->getSize().x / sizeX);
	int tv = spriteOrder[currentSprite] / (spriteSheet->getSize().x / sizeX);
	
	sprite.setTextureRect(sf::IntRect(tu*sizeX, tv*sizeY, sizeX, sizeY));
	sprite.setPosition(sf::Vector2f(placeX*mapTileX, placeY*mapTileY));
	sprite.setScale((float)mapTileX/sizeX, (float)mapTileY/sizeY);
	
	sprite.setTexture(*spriteSheet);
	
	movingObject = new MovingObject(sprite, sizeX, sizeY, spriteSheetSizeX, currentSprite, addedX, addedY, placeX, placeY, spriteOrder, animatedSpeed, spriteSheet->getSize().x / sizeX);
	
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

bool GameObject::drawObject()
{
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
	
	if(animated)
	{
		if(frameCounter % (animatedSpeed/(spriteOrder.size()-1)) == 0)
		{
			currentSprite++;
			
			if(currentSprite == spriteOrder.size())
				currentSprite -= spriteOrder.size();
			
			drawSprite(sprite, spriteSheetSizeX, sizeX, spriteOrder, currentSprite, sizeY);
		}
		
		if(frameCounter > animatedSpeed)
			frameCounter = 0;
			
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
	if(solid)
		return false;
	return true;
}

bool GameObject::checkConflict(sf::Vector2f directionCoord)
{
	int standingOn = currentObjects[placeY+directionCoord.y][placeX+directionCoord.x];
	
	if(standingOn != 0)
		for(int x = 0; x < gameObjects.size(); x++)
		{
			if(standingOn == gameObjects[x]->thisID)
				if(!gameObjects[x]->onContact(this))
					return true;
		}
	
	return false;
}

bool GameObject::startMoving(int direction)
{
	currentSprite = (spriteSheetSizeX / sizeX) * (direction-1);
	drawSprite(sprite, spriteSheetSizeX, sizeX, spriteOrder, currentSprite, sizeY);
	
	sf::Vector2f directionCoord;
	convertTo2f(direction, directionCoord);
	
	if(!checkConflict(directionCoord))
	{
		isMoving = true;
		movingDirection = direction;
		movingObject->updateInfo(directionCoord);
		return true;
	}
	return false;
}
