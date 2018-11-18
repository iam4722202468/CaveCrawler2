#include <SFML/Graphics.hpp>
#include <iostream>

#include "GameController.hpp"

int main(int argc, char *argv[])
{
    std::vector<std::vector<int>> maps; //for static background
    std::vector<std::vector<int>> layers; //for layered sprites
    std::vector<std::vector<std::vector<GameObject*>>> objects; //for layered sprites

    sf::RenderWindow window(sf::VideoMode(1200, 800), "SFML window");

    GameController game(window);
    game.loadMap("./build/Large_Map", maps, layers, objects);

    window.setFramerateLimit(60);

    // Start the game loop
    while (window.isOpen())
    {
        // Process events
        sf::Event event;
        
        if(sf::Keyboard::isKeyPressed(sf::Keyboard::Left)) {
            game.getKeyPress(71);
        } else if(sf::Keyboard::isKeyPressed(sf::Keyboard::Right)) {
            game.getKeyPress(72);
        } else if(sf::Keyboard::isKeyPressed(sf::Keyboard::Up)) {
            game.getKeyPress(73);
        } else if(sf::Keyboard::isKeyPressed(sf::Keyboard::Down)) {
            game.getKeyPress(74);
        } else {
            game.getKeyPress(0);
        }
        
        while(window.pollEvent(event))
        {
            if(event.type == sf::Event::Closed)
                window.close();
        }
        
        window.setView(game.characterView);
        window.clear(sf::Color::Black);
        game.drawMap();
        game.updateSprites();
        
        window.setView(window.getDefaultView());
        window.display();
    }
    
    return 0;
}
