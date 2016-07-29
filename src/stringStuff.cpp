#include <vector>
#include <string>

void stringsplit(char splitat, std::string line, std::vector<std::string>& newtext)
{
	std::string word = "";
	
	newtext.clear();
	
	for(int z = 0; z < line.size(); z++)
	{
		if(line[z] == splitat)
		{
			newtext.push_back(word);
			word = "";
		}
		else
			word += line[z];
	}
	
	newtext.push_back(word);
}
