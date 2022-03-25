
#include <iostream>

std::string str_cast(auto obj);
void print(auto print_string);

std::string str_cast(auto obj) {
return std::to_string(obj);
}
void print(auto print_string) {
std::cout<<print_string<<std::endl;
}



int main() {
    /* Transpiled with ComPy */
    int index = 0;
while (index < 100) {
print(("Index is: " + str_cast(index)));
index += 1;
if (index == 88) {
break;
};
};
    return 0;
}
