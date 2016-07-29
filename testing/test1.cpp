#include <iostream>
#include <vector>

class Parent
{
	protected:
	int moo = 0;
	
	public:
	Parent(int moo_) {moo = moo_;}
	virtual void setMooNumber() = 0;
	void setMoo(int newMoo) {moo = newMoo;}
	int getMoo() {return moo;}
};

class ChildFive : public Parent
{
	public:
	ChildFive(int moo_) :
		Parent(moo_) {}
	void setMooNumber() override {moo = 5;} //override makes sure it exists in the base class
};

class ChildSix : public Parent
{
	public:
	ChildSix(int moo_) :
		Parent(moo_) {}
	void setMooNumber() override {moo = 6;}
};

int main()
{
	std::vector<Parent*> container;
	
	container.push_back(new ChildFive(1));
	container.push_back(new ChildSix(2));
	container.push_back(new ChildSix(3));
	
	container[0]->setMooNumber();
	container[1]->setMooNumber();
	container[2]->setMoo(7);
	
	std::cout << container[0]->getMoo() << " " << container[1]->getMoo() << " " << container[2]->getMoo() << std::endl;
	
	return 0;
}
