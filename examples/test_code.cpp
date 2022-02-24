
#include <iostream>

void print(auto print_string){std::cout<<print_string<<std::endl;}
std::string str_cast(auto obj){return std::to_string(obj);}
int add(int number_one, int number_two){return number_one + number_two;}

int mul(int x, int y) {
int result = (x * y);
return result;
}

int main() {
	/* Transpiled with ComPy */
	int a = ((1 + 2) * 3);
int b = (a + 4);
int c = b;
c = add(c,b);
print(("The answer is... " + str_cast(c)));
print(mul(3,4));
print(mul(5,6));
	return 0;
}
