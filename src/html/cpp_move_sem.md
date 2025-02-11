## Return Value Optimisation
RVO is a compiler strategy that helps avoid copying objects returned by value. It comes in two flavours, unnamed RVO (RVO) and named RVO (NRVO). The former concerns the return of temporary objects, i.e., objects that have no name and you can't take the address of. The latter concers the return of named objects who's lifespan ends with the function return.

For example, `return MyObj();`, returns a temporary object (RVO) and `MyObj a; return a` returns a named object (NRVO).

It iss the only form of optimization that bypasses the as-if rule - copy elision can be applied even if copying/moving the object has side-effects.

Take the following example:

```cpp
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
```

If you run it with and without the `-fno-elide-constructors` it gives a clue as to what RVO and copy elision is...

<table>
    <tr>
        <th>no-elide-constructors</th>
        <th>elide-constructors</th>
    </tr>
    <tr>
        <td><pre>URVO
Constuctor


NRVO
Constuctor
Copy constructor
Destructor


END
Destructor
Destructor</pre>
        </td>

        <td><pre>URVO
Constuctor


NRVO
Constuctor


END
Destructor
Destructor</pre>
        </td>
    </table>


When constructor elision is disabled using the `-fno-elide-constructors` GCC option NRVO is disabled:

```
NRVO
Constuctor        -- 1. `MyObj a;` in `CreateObj_NRVO() on stack`.
Copy constructor  -- 2. `CreateObj_NRVO()` returns. `MyObj a` copied into `r1`.
Destructor        -- 3. `MyObj a;` destroyed as function exit complete.
```

When constructor elision is permitted the following is seen:

```
NRVO
Constructor        -- 1. `MyObj a;` in `CreateObj_NRVO()` but uses the memory allocated to `r1`.
                         Therefore on return, `r1` is already valid so no copy-out-of-function
                         is required! Saves a copy and destruction!
```

Interestingly the URVO is not affected... it is always used. The reason is explained here:

<blockquote>
    <p>Return-value optimization is part of a category of optimizations enabled by "copy elision" (meaning "omitting copying"). C++17 requires copy elision when a function returns a temporary object (unnamed object), but does not require it when a function returns a named object.
    </p>
    <footer>-- <a href="https://sigcpp.github.io/2020/06/08/return-value-optimization#:~:text=Return%2Dvalue%20optimization%20is%20part,function%20returns%20a%20named%20object." target="_blank">Return value optimization (RVO), SigCPP</a>.</footer>
</blockquote>
<p></p>

One important thing to note is that, as explained in the article referenced above,
<q>the compiler generates code such that object copying is avoided if the return value is used as the initializer for a receiving variable</q>.

Thus, doing something like this, stops either type of RVO:

```cpp
MyObj r1;              // Default constructor used
r1 = CreateObj_URVO(); // No RVO possible.
```

## Links / Quotes Not Yet Organised

From https://stackoverflow.com/a/14303116/1517244:

> Short answer: If a type is copyable, it should also be moveable. However, the reverse is not true: some types like std::unique_ptr are moveable yet it doesn't make sense to copy them; these are naturally move-only types.
> ...
> In C++11, generally you should think of move as an optimization of copy, and so all copyable types should naturally be moveable... moving is just an efficient way of doing a copy in the often-common case that you don't need the original object any more and are just going to destroy it anyway.




From https://stackoverflow.com/a/79336090/1517244
> "Move" just means you don't care what happens to the old object, right? So "it stays the same", which is what happens for a copy, is also perfectly valid for a move. Move isn't required to change it. So the immutable object can still very well have a move constructor (synthesized from copy). 

