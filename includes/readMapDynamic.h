#ifndef READMAPDYNAMIC_H
#define READMAPDYNAMIC_H

#include <fstream>
#include <string>
#include <iostream>

#include "stringStuff.hpp"

std::string getMaps(std::string fileName, std::vector<std::vector<std::vector<int>>> &maps)
{
	std::string sLine = "";
	std::ifstream infile;
	
	infile.open(fileName);
	
	maps.push_back(std::vector<std::vector<int>>());
	
	bool isAtItems = false;
	
	std::string itemsReturn = "";
	
	while (!infile.eof())
	{
		getline(infile, sLine);
		
		if(sLine == "-")
			isAtItems = true;
		else if(!isAtItems)
		{
			if(sLine == "_")
				maps.push_back(std::vector<std::vector<int>>());
			
			maps[maps.size()-1].push_back(std::vector<int>());
			
			std::string currentNumber = "";
			
			for(int x = 0; x < sLine.length(); x++)
			{
				if(sLine[x] != ',')
					currentNumber += sLine[x];
				else
				{
					maps[maps.size()-1][maps[maps.size()-1].size()-1].push_back(std::stoi(currentNumber));
					currentNumber = "";
				}
			}
			
			if(sLine != "_" && sLine != "")
				maps[maps.size()-1][maps[maps.size()-1].size()-1].push_back(std::stoi(currentNumber));
		}
		else
		{
			if(sLine != "")
				itemsReturn += sLine + '\n';
		}
	}
	return itemsReturn;
}

void getObjects(std::string fileName, std::vector<std::vector<std::vector<int>>> &maps, std::vector<std::vector<std::string>> &objects)
{
	std::string objectInfoString = getMaps(fileName, maps);
	std::vector<std::string> itemsSplit;
	stringsplit('\n', objectInfoString, itemsSplit);
	
	std::vector<std::string> tempString;
	
	for(int x = 0; x < itemsSplit.size()-1; x++)
	{
		objects.push_back(std::vector<std::string>());
		
		stringsplit(' ', itemsSplit[x], tempString);
		
		for(int y = 0; y < tempString.size()-1; y++)
			objects[objects.size()-1].push_back(tempString[y]);
	}
}

#endif
