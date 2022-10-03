// g++ -pthread basic_thread_start_func.cpp
#include <iostream>
#include <thread>

void my_thread_function(void)
{
    std::cout << "This is my thread running\n";
}

int main(int argc, char *argv[])
{
    std::thread my_thread(my_thread_function);
    my_thread.join();
    return 0;
}