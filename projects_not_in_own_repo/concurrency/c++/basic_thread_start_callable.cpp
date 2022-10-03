// g++ -std=c++1z -pthread basic_thread_start_callable.cpp 
#include <iostream>
#include <thread>

class my_thread_callable
{
public:
    void operator() () const
    {
        std::cout << "This is my thread running\n";
    }
};

int main(int argc, char *argv[])
{
    constexpr bool use_temporary = true;

    if constexpr (use_temporary)
    {
        // For a temporary must use brace intialiser to avoid most vexing parse issue.
        std::thread my_thread{my_thread_callable()};
        my_thread.join();

    }
    else {        
        my_thread_callable my_thread_obj;
        std::thread my_thread(my_thread_obj);
        my_thread.join();
    }
    return 0;
}