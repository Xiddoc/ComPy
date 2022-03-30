
#include <iostream>

void print(auto print_string);

void print(auto print_string) {
std::cout<<print_string<<std::endl;
}



int main() {
    /* Transpiled with ComPy */
    class TestClass {
private:


public:
int test_field;
TestClass() {
int a = 1;
print(a);
};

};
    return 0;
}
