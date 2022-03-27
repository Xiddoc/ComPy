
#include <utility>
#include <iostream>

void print(auto print_string);
std::string str_cast(auto obj);
int add(int number_one, int number_two);
std::string input(std::string print_string);

void print(auto print_string) {
std::cout<<print_string<<std::endl;
}
std::string str_cast(auto obj) {
return std::to_string(obj);
}
int add(int number_one, int number_two) {
return number_one + number_two;
}
std::string input(std::string print_string) {
print(std::move(print_string));std::string s;std::cin>>s;return s;
}

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
std::string user_input = input("Give me input: ");
print(("Testing input: " + user_input));
print(mul(3,4));
print(mul(5,6));
    return 0;
}
