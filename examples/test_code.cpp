
#include <iostream>

int inc(int my_integer){return ++my_integer;}
void print(auto print_string){std::cout<<print_string<<std::endl;}
std::string str_cast(auto obj){return std::to_string(obj);}

int mul(int x, int y) {;
int result = (x * y);
return result;
}

int main() {
	/* Transpiled with ComPy */
	;
int a = ((1 + 2) * 3);
int b = (a + 4);
int c = b;
c = inc(c);
print(("The answer is... " + str_cast(c)));
mul(1,2);
mul(3,4);
	return 0;
}
