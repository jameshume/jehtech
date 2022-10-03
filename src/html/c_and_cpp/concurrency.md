## C++ Memory Model
Post C++11, the C++ memory model now officially supports threads.

C++ talks about its "world" in terms of a virtual machine, which works as an _abstraction_ of whatever physical
machine the program will be compiled to run on. As long as a C++ program is written to comply with the rules and
restrictions of this virtual machine, the compiler guarantees to produce a program that will run correctly on
the physical target it is compiling for.

Pre C++11 the memory model was single threaded, so by definition one couldn't talk about threads. Of course one
could still write threaded code using libraries such as `pthreads`, they just weren't officially supported by
the standard so one could not be completely guaranteed that a program written in C++ could work on two different
targets.

With C+11 and beyond, as the memory model is multi-threaded, threads, locks, etc., etc., are supported
natively by the standard library, although the implementation may indeed just be `pthreads`, or similar,
under the hood!

## Start A Thread

<div class="box_container">
<div class="warning">
CAUTION: You must `join()` or `detach()` from an `std::thread` before it is destroyed, otherwise your program
will be restarted!
</div>
</div>

As part of the above warning, when `join()`'ing a thread, you must _make sure no exceptions occur before you have done the join_. Use RAII to combat this!

### Using A Function

[See it on Github](https://github.com/jameshume/jehtech/blob/master/projects_not_in_own_repo/concurrency/c++/basic_thread_start_func.cpp)

```
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
```

### Using A Callable

[See it on Github](https://github.com/jameshume/jehtech/blob/master/projects_not_in_own_repo/concurrency/c++/basic_thread_start_callable.cpp)

```
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
```
