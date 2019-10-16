



#include <iostream>
#include "ClassTest.h"
#include "CExport.h"

int main()
{
	std::cout << add(10, 20) << std::endl;
	ClassTest t;
	std::cout << t.getString() << std::endl;
}