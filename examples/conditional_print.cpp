#include <iostream>
void print(str print_string){std::cout<<print_string<<std::endl;}

void conditional_print(int index){print(index);if (((index==0&&index!=2)||index!=3)) {print("Equals to 0!");}else if (index<3) {print("Smaller than 3!");}else {print("Other...");print("(Did not match any other conditionals)");}conditional_print((index+1));}
conditional_print(0);