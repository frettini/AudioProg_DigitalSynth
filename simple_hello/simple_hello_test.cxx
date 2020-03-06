// File: simple_hello_test.cxx

#include <iostream>

#include "simple_hello.h"

using namespace std;

int main(int argc, char *argv[])
{
        cout << "Calling hw()\n";
        hw();
        cout << "Calling hw(argv[0])\n";
        hw(argv[0]);
	return 0;
}