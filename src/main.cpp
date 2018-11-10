#include <SFML/Graphics.hpp>

#include <iostream>

#include "controller.hpp"

#ifdef COMPILED
    #include "generatedMaps.h"
#else
    #include "readMapDynamic.h"
    std::vector<std::vector<std::vector<int>>> maps; //for static background
    std::vector<std::vector<std::vector<int>>> layers; //for layered sprites
    std::vector<std::vector<std::vector<int>>> objects; //for layered sprites
    std::vector<std::vector<std::string>> objectInfo; //info for objects; gets read in later
#endif

int main(int argc, char *argv[])
{
    #ifndef COMPILED
        getMaps("./includes/generatedMaps.txt", maps);
        getMaps("./includes/generatedLayers.txt", layers);
        getObjects("./includes/generatedObjects.txt", objects, objectInfo);
    #endif
    
    sf::RenderWindow window(sf::VideoMode(1400, 1400), "SFML window");
    
    sf::View view;
    
    // Initialize the view to a rectangle located at (100, 100) and with a size of 400x200
    
    // Rotate it by 45 degrees
    //view.rotate(45);
    
    // Set its target viewport to be half of the window
    view.setViewport(sf::FloatRect(0.f, 0.f, 2.f, 2.f));
    
    GameController game(window);
    game.setMap(maps[1]);
    game.setLayer(layers[1]);
    game.setObjects(objects[1]);
    game.generateObjects(objectInfo);
    
    sf::Clock clock;
    int frames = 0;
    
    window.setFramerateLimit(60);
    
    // Start the game loop
    while (window.isOpen())
    {
        // Process events
        sf::Event event;
        //sf::Mouse mouse;
        if(int(clock.getElapsedTime().asSeconds()) == 1)
        {
            clock.restart();
            //std::cout << frames << std::endl;
            frames = 0;
        }
        
        frames++;
        
        if(sf::Keyboard::isKeyPressed(sf::Keyboard::Left)) {
            game.getKeyPress(71);
        } else if(sf::Keyboard::isKeyPressed(sf::Keyboard::Right)) {
            game.getKeyPress(72);
        } else if(sf::Keyboard::isKeyPressed(sf::Keyboard::Up)) {
            game.getKeyPress(73);
        } else if(sf::Keyboard::isKeyPressed(sf::Keyboard::Down)) {
            game.getKeyPress(74);
        }
                
        while(window.pollEvent(event))
        {
            if(event.type == sf::Event::Closed)
                window.close();
        }
        
        window.setView(view);
        window.setView(game.characterView);
        window.clear(sf::Color::Green);
        game.drawCurrentMap();
        
        window.setView(window.getDefaultView());
        
        sf::RectangleShape rectangle;
        rectangle.setSize(sf::Vector2f(100, 50));
        rectangle.setOutlineColor(sf::Color::Red);
        rectangle.setOutlineThickness(5);
        rectangle.setPosition(10, 20);
        
        window.draw(rectangle);
    
        window.display();
    }
    
    return 0;
}
