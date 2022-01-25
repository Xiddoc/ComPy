#include <iostream>
void print(str print_string){std::cout<<print_string<<std::endl;}

int a = ((1+2)*3);
int b = (a+4);
int c = b;
print("The answer is... ");
print(c);
c = 10;
int mul(int x,int y){int result = (x*y);return result;}
mul(1,2);
mul(3,4);