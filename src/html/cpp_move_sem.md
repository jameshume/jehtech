## Return Value Optimisation
RVO is a compiler strategy that helps avoid copying objects returned by value. It comes in two flavours, unnamed RVO (RVO) and named RVO (NRVO). The former concerns the return of temporary objects, i.e., objects that have no name and you can't take the address of. The latter concers the return of named objects who's lifespan ends with the function return.

For example, `return MyObj();`, returns a temporary object (RVO) and `MyObj a; return a` returns a named object (NRVO).

It is the only form of optimization that bypasses the [as-if](https://en.cppreference.com/w/cpp/language/as_if.html) rule - copy elision can be applied even if copying/moving the object has side-effects.

The [as-if](https://en.cppreference.com/w/cpp/language/as_if.html) rule means that a compiler may perform any transformation it likes, as long as the observable behaviour of the program is the same as if the program were executed exactly as written in the abstract machine defined by the standard.

Copy-elision is exempted from this rule and in C++17 certain cases are guaranteed.

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

## Wasted Allocations and Copies: Move Semantics To The Rescue

In the following example the Junk class is far from perfrect - its just demonstrating a point.

```cpp
#include <string>
#include <iostream>
#include <vector>

class Junk {
public:
    explicit Junk(const char *txt) : m_len(strlen(txt)), m_txt(new char[m_len + 1]) {
        std::cout << "Junk string constructor\n";
        strncpy(m_txt, txt, m_len);
    }

    explicit Junk(std::size_t chars) : m_txt(new char[chars + 1]) {
        std::cout << "Junk space alloc constructor\n";
        m_txt[0] = '\0';
    }

    Junk(const Junk &other) {
        std::cout << "Junk copy constructor\n";
        m_txt = new char[other.m_len +1];
        m_len = other.m_len;
        strncpy(m_txt, other.m_txt, other.m_len);
    }

    ~Junk() {
        std::cout << "Junk string destructor\n";
        delete[] m_txt;
    }

    Junk operator+(const Junk &other) {
        std::cout << "Junk + operator\n";
        Junk newobj{m_len + other.m_len};
        strncpy(newobj.m_txt, m_txt, m_len);
        strncpy(&newobj.m_txt[m_len], other.m_txt, other.m_len);
        return newobj;
    }

private:
    size_t m_len;
    char* m_txt;
};

int main() {
    std::vector<Junk> v;
    Junk s {"superjunk"};
    v.push_back(s+s); // Use V as we know container has value semantics so will copy value
                      // If we just use Juk ss = s + s, RVO occurs, even in C98.
    return 0;
}
```

Without move semantics the above code creates a new temporary object for `s+s`. The output is this (comments added):

```
Junk string constructor
Junk + operator
Junk space alloc constructor
Junk copy constructor
Junk string destructor
Junk string destructor
Junk string destructor
```

We can see that the copy constructor is called to copy it into the vector. The temporary gets created, copied and destroyed, which is wasteful: Two memory allocations occur for the temporary and the vector.

Now watch with move semantics turned on, we must add this function to the class:

```cpp
    Junk(Junk &&other) noexcept {
        std::cout << "Junk move constructor\n";
        m_txt = other.m_txt;
        m_len = other.m_len;
        
        other.m_txt = nullptr;
        other.m_len = 0;
    }
```

Where `Junk&&` is an rvalue reference. An rvalue reference is a reference type introduced in C plus plus 11 that can bind to temporary objects and to objects explicitly cast to an rvalue. It is written using `&&`.

It binds to rvalues, which are typically

* temporary objects
* the result of expressions
* objects marked with std::move

Unlike lvalue references, rvalue references do not bind to named lvalues unless those lvalues are explicitly converted to rvalues.

Rule of thumb is that rvalue references can only refer to temporary objects that:

* Do not have a name, and
* Cannot have their address taken

Or to objects marked with `std::move()`.

NOTE const objects cannot, therefore, be moved! This applies to return values too!! Thus *best not to return const objects since C11*.

NOTE the moved-from object is still a valid object and must be left is a valid state, even if that state is unspecified. So its reusable.

NOTE move operators should be `noexcept`.

Now the output is:

```
Junk string constructor
Junk + operator
Junk space alloc constructor
Junk move constructor
Junk string destructor
Junk string destructor
Junk string destructor
```

Woop, the copy constructor which has to do an allocation (system call overhead) and a copy, is replaced by the move constructor and just moves the pointer to the text string across - way more efficient!

If we extend the `main()` function like so:

```cpp
int main() {
    std::vector<Junk> v;
    Junk s {"superjunk"};
    v.push_back(s+s); 
    v.push_back(s); //< Added this
    return 0;
}
```

The output is now:

```
Junk string constructor
Junk + operator
Junk space alloc constructor
Junk move constructor
Junk string destructor
Junk copy constructor    # This last copy is v.push_back(s)
Junk copy constructor    # Err... whats this?! See below!
Junk string destructor
Junk string destructor
Junk string destructor
Junk string destructor
```

There is one more copy constructor than expected. Why is this? This is because the vector is re-sizing itself, which forces a reallocation and relocatation of the elements that are already inside the vector. Also it used a copy because when I first did this I didnt declare the move operator as `noexcept`!

Lets fix this:

```cpp
int main() {
    std::vector<Junk> v;
    Junk s {"superjunk"};
    v.reserve(2); // Allocate enough space so vector doesnt need to resize
    std::cout << "1\n";
    v.push_back(s+s); 
    std::cout << "2\n";
    v.push_back(s); //< Added this
    std::cout << "3\n";
    return 0;
}
```

Now the output is what I'd expect:

```
Junk string constructor
1
Junk + operator
Junk space alloc constructor
Junk move constructor
Junk string destructor
2
Junk copy constructor
3
Junk string destructor
Junk string destructor
Junk string destructor
```

The last copy is also a waste as in our silly little demo, `s` is not used anymore. We can tell the compiler that "we don't need `s` anymore" like this:

```cpp
int main() {
    std::vector<Junk> v;
    Junk s {"superjunk"};
    v.reserve(2);
    std::cout << "1\n";
    v.push_back(s+s); 
    std::cout << "2\n";
    v.push_back(std::move(s)); //< Added std::move!
    std::cout << "3\n";
    return 0;
}
```

The output is now:

```
Junk string constructor
1
Junk + operator
Junk space alloc constructor
Junk move constructor
Junk string destructor
2
Junk move constructor  ### Yay! no longer copied it!
3
Junk string destructor
Junk string destructor
Junk string destructor
```

Sweet, by using `std::move(s)` we told the compiler that we'd no longer use `s`, so the compiler could now move it rather than copy it.

## Automatic Move Semantic Generation
In many cases the compiler can automatically generate the move-related functions. It didn't in the previous section because automatic generation of move operations is disabled when ny of the following member functions are define:

* Copy constructor
* Copy assignment operator
* Another move operation
* Destructor (*even if it is emppy and does nothing!*)

## Special Member Functions
These are:

1. Default constructor
2. Copy constructor
3. Copy assignment operator
4. Move constructor
5. Move assignment operator
6. Destructor

When the user declares nothing:

* All 6 special member functions are defaulted

When any constructor is declared:

* Default constructor is not automatically created
* Everything else defaulted

When default constructor is declared:

* Everything else defaulted

When copy constructor is declared:

* Default constructor not generated
* Move operators not generated
* Everything else defaulted

When copy assignment operator is declared:

* Default constructor generated
* Move operators not generated
* Everything else defaulted

When move constructor is declared:

* Default constructor not generated
* Copy constructor and assignment operated deleted
* Move assignment undeclared  with *fallback disabled*
* Destructor defaulted

When move assignment is declared:

* Default constructor not generated
* Copy constructor and assignment operated deleted
* Move constructor undeclared with *fallback disabled*
* Destructor defaulted

When destructor declared:

* Moves undeclared but have fallback enabled
* Everything else defaulted

Unless stated fallback is enabled, which means that a move degrades to a copy when tried.


## Links / Quotes Not Yet Organised

From https://stackoverflow.com/a/14303116/1517244:

> Short answer: If a type is copyable, it should also be moveable. However, the reverse is not true: some types like std::unique_ptr are moveable yet it doesn't make sense to copy them; these are naturally move-only types.
> ...
> In C++11, generally you should think of move as an optimization of copy, and so all copyable types should naturally be moveable... moving is just an efficient way of doing a copy in the often-common case that you don't need the original object any more and are just going to destroy it anyway.




From https://stackoverflow.com/a/79336090/1517244
> "Move" just means you don't care what happens to the old object, right? So "it stays the same", which is what happens for a copy, is also perfectly valid for a move. Move isn't required to change it. So the immutable object can still very well have a move constructor (synthesized from copy). 

