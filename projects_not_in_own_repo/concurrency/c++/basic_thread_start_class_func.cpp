// g++ -pthread basic_thread_start_class_func.cpp
#include <iostream>
#include <thread>

class MyThreadyThing
{
public:
    void MyThreadyFunction(int a, int b)
    {
        std::cout << "This is my thread running: " << a << " - " << b << "\n";
    }

};

int main(int argc, char *argv[])
{
    MyThreadyThing thing;
    std::thread my_thread(&MyThreadyThing::MyThreadyFunction, &thing, 99, 22);
    my_thread.join();
    return 0;
}