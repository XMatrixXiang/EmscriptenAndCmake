#pragma once

#include <string>

class ClassTest
{
public:
	ClassTest() = default;
	virtual ~ClassTest() = default;

public:
	int getInt() const { return mInt; }
	float getFloat() const { return mFloat; }
	double getDouble() const { return mDouble; }
	const std::string & getString() const { return mString; }
protected:
	int mInt = 0;
	float mFloat = 0.0f;
	double mDouble = 0.0;
	std::string mString = "this is string!";
};

