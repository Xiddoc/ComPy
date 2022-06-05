
#include <iostream>
#include <utility>

void print(auto print_string);
int int_cast(std::string obj);
std::string input(std::string print_string);
int add(int number_one, int number_two);
std::string str_cast(auto obj);

void print(auto print_string) {
std::cout<<print_string<<std::endl;
}
int int_cast(std::string obj) {
return std::stoi(obj);
}
std::string input(std::string print_string) {
print(std::move(print_string));std::string s;std::cin>>s;return s;
}
int add(int number_one, int number_two) {
return number_one + number_two;
}
std::string str_cast(auto obj) {
return std::to_string(obj);
}

void imported_function() {
print("Test import function called!");
}
int mul(int x, int y) {
int result = (x * y);
return result;
}

int main() {
    /* Transpiled with ComPy */
    print("Test imported!");
int a = ((1 + 2) * 3);
int b = (a + 4);
int c = b;
c = add(c,b);
print(("The answer is... " + str_cast(c)));
std::string user_input = input("Give me input: ");
print(("Testing input: " + user_input));
print(("More testing input: " + str_cast((int_cast(user_input) * 100))));
print(mul(3,4));
print(mul(5,6));
    return 0;
}
