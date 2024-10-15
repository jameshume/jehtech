// Use `g++ demo_no_move_sem.cpp -O0 -fno-elide-constructors && ./a.out`
// `-fno-elide-constructors` disable return value optimization.
#include <cstring>
#include <iostream>
#include <iterator>

struct MyObj {
    MyObj() {
        std::cout << "Constuctor\n";
    }

    ~MyObj() {
        std::cout << "Destructor\n";
    }

    MyObj(const MyObj& other) {
        std::cout << "Copy constructor\n";
    }
};

MyObj CreateObj_URVO() {
    return MyObj();
}

MyObj CreateObj_NRVO() {
    MyObj a;
    return a;
}

int main(void) {
    std::cout << "URVO\n";
    MyObj r1 = CreateObj_URVO();

    std::cout << "\n\nNRVO\n";
    MyObj r2 = CreateObj_NRVO();

    std::cout << "\n\nEND\n";
}
