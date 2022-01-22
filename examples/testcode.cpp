#include <iostream>
void print(/* print_string: str */ /* str */ str print_string){std::cout<<print_string<<std::endl;}
/* '\nTest comment.\n\nLots of escaped characters!\n\' " ` ; / % @ { } ' */ 
/* a: int = (1 + 2) * 3 */ int a = /* (1 + 2) * 3 */ (/* 1 + 2 */ (/* 1 */ 1+/* 2 */ 2)*/* 3 */ 3);
/* b: int = a + 4 */ int b = /* a + 4 */ (/* a */ a+/* 4 */ 4);
/* c: int = b */ int c = /* b */ b;
/* print('The answer is... ') */ /* print('The answer is... ') */ /* print */ print(/* 'The answer is... ' */ "The answer is... ");
/* print(c) */ /* print(c) */ /* print */ print(/* c */ c);
/* def mul(x: int, y: int) -> int:
    """
	Test function.
	"""
    return x * y */ /* int */ int mul(/* x: int */ /* int */ int x,/* y: int */ /* int */ int y){/* '\n\tTest function.\n\t' */ /* return x * y */ return /* x * y */ (/* x */ x*/* y */ y);}
/* mul(1, 2) */ /* mul(1, 2) */ /* mul */ mul(/* 1 */ 1,/* 2 */ 2);
/* mul(3, 4) */ /* mul(3, 4) */ /* mul */ mul(/* 3 */ 3,/* 4 */ 4);