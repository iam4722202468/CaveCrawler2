#include <vector>
#include <SFML/Graphics.hpp>

#include "GameController.hpp"
#include "stringStuff.hpp" //for split string
#include "../gameClasses/object.hpp"

GameController::GameController(sf::RenderWindow &window):
	window(window)
{
  characterView.zoom(0.65f);
}

//(1,2,3,4) <- up left down right
bool GameController::getKeyPress(int keyValue)
{
	return true;
}

bool GameController::drawMap() {
  return true;
}

bool GameController::loadMap(
    std::string fileName,
    std::vector<std::vector<int>> &bgVector,
    std::vector<std::vector<int>> &fgVector,
    std::vector<std::vector<std::vector<GameObject*>>>
  ) {
  return true;
}

bool GameController::updateSprites() {
  return true;
}
