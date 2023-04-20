// g++ -pthread basic_thread_start_func.cpp
#include <iostream>
#include <thread>

void my_thread_function(int a, int b)
{
    std::cout << "This is my thread running: " << a << " - " << b << "\n";
}

int main(int argc, char *argv[])
{
    std::thread my_thread(my_thread_function, 9, 2);
    my_thread.join();
    return 0;
}