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
	
	auto curmap = std::vector<std::vector<int>>();
	
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
			{
				maps.push_back(curmap);
				curmap = std::vector<std::vector<int>>();
				continue;
			}
			
			auto curline = std::vector<int>();
			
			auto nums = std::vector<std::string>();
			stringsplit(',',sLine,nums);
			
			for(int i=0;i<nums.size()-1;i++){
				curline.push_back(std::stoi(nums[i]));
			}
			curmap.push_back(curline);
		}
		else
		{
			if(sLine != "")
				itemsReturn += sLine + '\n';
		}
	}
	maps.push_back(curmap);
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
