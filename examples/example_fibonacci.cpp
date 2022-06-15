
#include <iostream>

void print(auto print_string);
std::string str_cast(auto obj);

void print(auto print_string) {
std::cout<<print_string<<std::endl;
};
std::string str_cast(auto obj) {
return std::to_string(obj);
};

int fib(int index) {
return index <= 1 ? index : (fib((index - 1)) + fib((index - 2)));
}

int main() {
    /* Transpiled with ComPy */
    int fib_index = 35;
print((("Calculating index " + str_cast(fib_index)) + " of fibonacci series..."));
print(fib(fib_index));
    return 0;
}
