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

Starting a thread is pretty easy...

<div class="box_container">
<div class="warning">
You must <code>join()</code> or <code>detach()</code> from an <code>std::thread</code> before it is destroyed, otherwise your program
will be restarted!
</div>
</div>

<div class="box_container">
<div class="info">
<code>std::thread</code> is movable but <em>not</em> copyable.
</div>
</div>


As part of the above warning, when `join()`'ing a thread, you must _make sure no exceptions occur before you have done the `join()`_. Use RAII to combat this!

### Using A Function

[See it on Github](https://github.com/jameshume/jehtech/blob/master/projects_not_in_own_repo/concurrency/c++/basic_thread_start_func.cpp)

```
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
```

### Using A Function Pointer To A Class Member Function

[See it on Github](https://github.com/jameshume/jehtech/blob/master/projects_not_in_own_repo/concurrency/c++/basic_thread_start_class_func.cpp)

```
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
```

### Using A Callable

[See it on Github](https://github.com/jameshume/jehtech/blob/master/projects_not_in_own_repo/concurrency/c++/basic_thread_start_callable.cpp)

```
#include <iostream>
#include <thread>

class my_thread_callable
{
public:
    void operator() (int a, int b) const
    {
        std::cout << "This is my thread running: " << a << " - " << b << "\n";
    }
};

int main(int argc, char *argv[])
{
    constexpr bool use_temporary = true;

    if constexpr (use_temporary)
    {
        // For a temporary must use brace intialiser to avoid most vexing parse issue.
        std::thread my_thread{my_thread_callable(), 20, 21};
        my_thread.join();

    }
    else {        
        my_thread_callable my_thread_obj;
        std::thread my_thread(my_thread_obj, 19, 20);
        my_thread.join();
    }
    return 0;
}
```

### Thread Parameter Gotchas

The `std::thread` constructor _copies_ supplied values. Thus, if the thread function expects references it will
get a reference to the _copy_, not the original.

The solution is to wrap the argument using `std::ref()`. This will wrap the object with an appropriate
`std::reference_wrapper` type. This is an object that emulates a reference, internally holding a reference to
your object. Thus when `std::thread` _copies_ this object, the internal reference used will still reference
your original object and _not_ a copy.



## Semaphores
Interestingly C++ didn't get a semaphore class until C++20. Prior to that there were only mutexes
and condition variables [[Ref]](https://stackoverflow.com/questions/4792449/c0x-has-no-semaphores-how-to-synchronize-threads).


## Mutexes
* Create using `std::mutex`. Acquire/lock with `.lock()` and release/unlock with `.unlock()`, however
  to avoid forgetting to unlock, best to use RAII in the form of a `std::lock_guard<std::mutex>`.

```
std::mutex my_mutex;

void do_something(void) {
    std::lock_guard<std::mutex> guard(my_mutex);
    // Rest of function until `guard` goes out of scope is now protected by `my_mutex`
    // ....
}
```

### Deadlock
#### std::lock
* When locks cannot be reliably acquired in the same order use `std::lock()` - it can lock two or more
  mutexes at once without risk of deadlock.

#### std::unique_lock