
#include <iostream>

void print(auto print_string);

void print(auto print_string){std::cout<<print_string<<std::endl;}

int fib(int index) {
return index <= 1 ? index : (fib((index - 1)) + fib((index - 2)));
}

int main() {
    /* Transpiled with ComPy */
    print(fib(30));
    return 0;
}
