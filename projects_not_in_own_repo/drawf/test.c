
//Verbatim from https://eli.thegreenplace.net/2011/02/07/how-debuggers-work-part-3-debugging-information
// compile using gcc -g  test.c

#include <stdio.h>

enum JAMES {
    J1,
    J2,
    J3
};

void do_stuff(int my_arg)
{
    int my_local = my_arg + 2;
    int i = J1;

    for (i = J1; i < my_local; ++i)
        printf("i = %d\n", i);
}


int main()
{
    do_stuff(2);
    return 0;
}