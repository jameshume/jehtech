
//Verbatim from https://eli.thegreenplace.net/2011/02/07/how-debuggers-work-part-3-debugging-information
// compile using gcc -g  test.c

#include <stdio.h>

enum MY_FIRST_ENUM {
    FIRST_ONE,
    FIRST_TWO,
    FIRST_THREE
};

typedef enum MY_2_ENUM {
    SECOND_ONE,
    SECOND_TWO,
    SECOND_THREE
} MY_SECOND_t;


int main()
{
    enum MY_FIRST_ENUM test = FIRST_TWO;
    MY_SECOND_t ss = SECOND_THREE;
    return 0;
}