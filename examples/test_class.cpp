
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
int test_var = 1;
print(test_var);
};

};
TestClass test_instance = TestClass();
print(test_instance.test_field);
    return 0;
}
