
#include <iostream>

void print(auto print_string);

void print(auto print_string) {
std::cout<<print_string<<std::endl;
};



int main() {
    /* Transpiled with ComPy */
    class TestClass {
public:
int test_field = 0;
TestClass() {
int test_var = 123;
print(test_var);
};
void increment_test() {
test_field += 1;
};
};
TestClass test_instance = TestClass();
print(test_instance.test_field);
test_instance.increment_test();
print(test_instance.test_field);
    return 0;
}