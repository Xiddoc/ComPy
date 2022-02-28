
#include <iostream>

void print(auto print_string);

void print(auto print_string){std::cout<<print_string<<std::endl;}

void conditional_print(int index) {
print(index);
if (((index == 0 && index != 2) || index != 3)) {
print("Equals to 0!")
} else if (1 < 2 < index < 5) {
print("Larger than 2 and smaller than 5!")
} else {
print("Other...")print("(Did not match any other conditionals)")
};
conditional_print((index + 1));
}

int main() {
    /* Transpiled with ComPy */
    conditional_print(0);
    return 0;
}
