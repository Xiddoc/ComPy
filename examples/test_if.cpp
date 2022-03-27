
#include <iostream>

void print(auto print_string);
std::string str_cast(auto obj);

void print(auto print_string) {
std::cout<<print_string<<std::endl;
}
std::string str_cast(auto obj) {
return std::to_string(obj);
}

void conditional_print(int index = 0) {
if ((index == 0 && index != 2 && index != 3)) {
print((str_cast(index) + ": Equals to 0!"));
} else {
if (1 < 2 && 2 < index && index < 5) {
print((str_cast(index) + ": Larger than 2 and smaller than 5!"));
} else {
if (7 < index && index < 12) {
print((str_cast(index) + ": Larger than 7 and smaller than 12!"));
} else {
print((str_cast(index) + ": Other..."));
if (index == 4) {
print((str_cast(index) + ": Test, got 4..."));
};
};
};
};
if (index > 25) {
return;
};
conditional_print((index + 1));
}

int main() {
    /* Transpiled with ComPy */
    conditional_print();
    return 0;
}
