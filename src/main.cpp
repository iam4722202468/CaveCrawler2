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
	
	sf::RenderWindow window(sf::VideoMode(700, 700), "SFML window");
	
	/*sf::View view;
	
	// Initialize the view to a rectangle located at (100, 100) and with a size of 400x200
	view.reset(sf::FloatRect(100, 100, 400, 200));
	// Rotate it by 45 degrees
	view.rotate(45);
	// Set its target viewport to be half of the window
	view.setViewport(sf::FloatRect(0.f, 0.f, 0.5f, 1.f));
	// Apply it
	window.setView(view);*/
	
	GameController game(window);
	game.setMap(maps[0]);
	game.setLayer(layers[0]);
	game.setObjects(objects[0]);
	game.generateObjects(objectInfo);
	
	sf::Clock clock;
	int frames = 0;
	
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
		
		while (window.pollEvent(event))
		{
			if(event.type == sf::Event::Closed)
				window.close();
			if(event.type == sf::Event::KeyPressed)
				game.getKeyPress(event.key.code);
		}
		game.drawCurrentMap();
		window.display();
	}
	
	return 0;
}
