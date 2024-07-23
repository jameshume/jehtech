# My Motivation
I wanted to be able to construct a static string that was going to be placed into an ELF "section containing
zero-terminated strings" to be "used by things other than the program" (see [GNU Assembler manual describtions of `.section`](https://sourceware.org/binutils/docs/as/Section.html)).

Standard C would be:

```C
#define IN_STR_SECTION __attribute__ ((used, section (".myStringsSection,\"S\",@note #")))
static const char dummy_name[] IN_STR_SECTION = "Some string";
```

But, I also wanted to inject things into this string, like an integer identify that would map to the
string. Something of the form `1: "Some string"`, so that I could use the integer in the code,
instread of the string.

But, the problem is that there is no way to create a unique value for this identifier that is
global across all translaction units. GCC has `__COUNTER__`, but this is only unique within the
one translaction unit, so won't accomplish what I want.

I did not want to have to run a script that would modify the source code and then pass the
modified code to the compiler if possible.

As it happened, I was trying to leverage some C++, so my attention turned to how I could

1. Generate a unique ID for a string at compile time. Suggestion from a collegue was to hash
   the string.
2. Concatentate the unique ID with the rest of the string and store it as a `static const char[]`.


## Problem 1: Returning A Character Array?!
The initialiser for the `static const char[]` has to be a `constexpr`, otherwise the compiler
cannot initilise this at compile time. So, how can a `constexpr` function return an array?
The answer is it can't and the initialiser type is going to have to change. Read on...

A function can _not_ do the following:

```C++
constexpr auto num_digits(const unsigned int value) {
    ...
}

constexpr auto doesnt_work(const unsigned int value) {
    char string_value[num_digits(value)];
    ...
    return string_value;
}
```

This would never work because functions don't return arrays: the array decays into
a pointer, and a pointer is returned. Thus, a pointer to a local variable is returned
which is UB and couldn't be assigned to a `char[]` anyway!

The function also couldn't be modified to copy a string into a `char[]` argument because
thats not initialising the argument - its already been created!

So, after some digging around I found, first that `std::string` is not constexpr
capable/safe, and second that I would need to return a structure, who's first and only
member is a `char[]`.  

The key to returning a structure who's first and only member is a character array is that
it is the structure's data that is being stored in the strings section, and it just so
happens that the only data is a character array. This is important, because whatever
`constexpr` is used to construct a string that is a concatenation of strings and 
numbers will return a structure, so:

```C
#define IN_STR_SECTION __attribute__ ((used, section (".myStringsSection,\"S\",@note #")))
static const char dummy_name[] IN_STR_SECTION = "Some string";
```

Has to become:

```C
#define IN_STR_SECTION __attribute__ ((used, section (".myStringsSection,\"S\",@note #")))
static const struct XXX<N> __attribute__ IN_STR_SECTION = "..." + 1 + "..."; //< Do this somehow!
```

And we have to be comfortable that although instead of a `char[]` we are storing a `struct XXX<N>` to
our special section, we are still, in fact, just storing a null terminated character string!

Briefly, the "string" will look like this:

```C++
#include <cstddef>

template<size_t N>
struct constexpr_string {
    char value[N];

    // To be initialisabe a constructor is needed
    // `inital_value` is a pointer to a char array of size N, not a char pointer.
    constexpr_string(char (*initial_value)[N]) {
        for (size_t i = 0; i < N; ++i) { value[i] = initial_value[i]; } // Could use std::copy_n
    }
};
```

Having figured out a neaky way to return a character array from our `constexpr` function, the next
problem is how it should be constructed _at compile time_.

# Problem 2: Constructing Strings At Compile Time



As this all has to happen at compile time, so the size of the array holding the string has to be known 
at compile time. How can this be done? The answer is 
[non-type template parameters](https://www.learncpp.com/cpp-tutorial/non-type-template-parameters/).


Lets tackle converting an integer to a character array at compile time first.

We can represent the strings like so:

```C++
#include <cstddef>

template<size_t N>
struct constexpr_string {
    char value[N];

    constexpr_string() {
        for (size_t i = 0; i < N; ++i) { value[i] = '\0'; } // Could use std::...
    }

    constexpr_string(char (*initial_value)[N]) {
        for (size_t i = 0; i < N; ++i) { value[i] = initial_value[i]; } // Could use std::copy_n
    }
};

constexpr auto constexpr_unsigned_to_string(unsigned value) {
    constexpr size_t size = 0;
    const unsigned original_value = value;
    while(value) {
        size++;
        value /= 10;
    }

    constexpr_string<size> number;

    // ...
}
```

No we can't:

```
test.cpp: In function 'constexpr auto constexpr_unsigned_to_string(unsigned int)':
test.cpp:20:9: error: increment of read-only variable ‘size’
   20 |         size++;
      |         ^~~~
```

Facepalm! `constexpr` means `const`, but `const` does not mean `constexpr`, but they are both constant,
so `size` cannot be `constexpr`. But, if it is not, then it cannot be used as the template argument
when defining `number`. Thus, the number of bytes to hold the string plus NULL terminator has to be
calculated in a seperate `constexpr` function:

```C++
#include <cstddef>

template<size_t N>
struct constexpr_string {
    char value[N];

    constexpr_string() {
        for (size_t i = 0; i < N; ++i) { value[i] = '\0'; } // Could use std::...
    }

    constexpr_string(char (*initial_value)[N]) {
        for (size_t i = 0; i < N; ++i) { value[i] = initial_value[i]; } // Could use std::copy_n
    }
};

constexpr size_t constexpr_unsigned_bytes(unsigned value) {
    size_t size = 0;    
    while(value) {
        size++;
        value /= 10;
    }
    return size + 1; // +1 for NULL termination byte
}

constexpr auto constexpr_unsigned_to_string(unsigned value) {
    constexpr auto bytes = constexpr_unsigned_bytes(value); // ERROR! This will fail
    auto number_as_string = constexpr_string<bytes>();      // (See below...)

    // ...
}

int main() {
    return 0;
}
```

No, no, no... this won't work either! The following error occurs:

```
test.cpp: In function 'constexpr auto constexpr_unsigned_to_string(unsigned int)':
test.cpp:26:58: error: 'value' is not a constant expression
   26 |     constexpr auto bytes = constexpr_unsigned_bytes(value);
      |   
```

What surprised me was that `value` was not considered a constant expression. After all,
`constexpr_unsigned_bytes` was a `constexpr` function and I can do this:

```C++
#include <cstddef>

constexpr size_t constexpr_unsigned_bytes(unsigned value) {
    size_t size = 0;    
    while(value) {
        size++;
        value /= 10;
    }
    return size + 1; // +1 for NULL termination byte
}

int main() {
    char test[constexpr_unsigned_bytes(12)];
    static_assert(sizeof(test) == 3);
    return 0;
}
```

So clearly `constexpr_unsigned_bytes` can calculate the number of bytes required to hold the 
integer as a null terminated string at compile time. So what gives?

This can be boiled down to an even easier example. The following works:

```C++
constexpr auto dummy(unsigned a) {
    return  a * 2 + 1;
}

int main() {
    char c[dummy(3)];
    return 0;
}
```

But the following does not

```C++
constexpr auto dummy(unsigned a) {
    constexpr auto intermediate = a * 2;
    return  intermediate + 1;
}

int main() {
    char c[dummy(3)];
    return 0;
}
```

It fails with the same error message.

```
test.cpp: In function ‘constexpr auto dummy(unsigned int)’:
test.cpp:2:39: error: ‘a’ is not a constant expression
    2 |     constexpr auto intermediate = a * 2;
      |    
```

Why? The reason is this:

<p></p><blockquote>
    <p>
        One challenge with constant expressions is that <b>function calls to a normal function 
        are not allowed in constant expressions</b>. This means we cannot use such function calls
        anywhere a constant expression is required ... A <code>constexpr</code> function is
        a function that is allowed to be called in a constant expression.
    </p><p>
        ...
    </p><p>
        Allowing functions with a <code>constexpr</code> return type to be <b>evaluated at
        either compile-time or runtime</b> was allowed so that a single function can serve both cases.
    </p><p>
        Otherwise, you'd need to have separate functions (a function with a constexpr return type,
        and a function with a non-<code>constexpr</code> return type). This would not only require 
        duplicate code, the two functions would also need to have different names!
    </p><p>
        ...
    </p><p>
        Compile-time evaluation of <code>constexpr</code> functions is <b>only guaranteed when a
        constant expression is required</b>.
    </p><p>
        ...
    </p><p>
        <b>The parameters of a <code>constexpr</code> function are not implicitly 
        <code>constexpr</code>, nor may they be declared as <code>constexpr</code></b>
        ... A <code>constexpr</code> function parameter would imply the function
        could only be called with a <code>constexpr</code> argument. But this is 
        not the case -- <code>constexpr</code> functions can be called with 
        non-<code>constexpr</code> arguments when the function is evaluated at 
        runtime ... Because such <b>parameters are not <code>constexpr</code>, 
        they cannot be used in constant expressions within the function</b>.
    </p>
    <footer> --<a href="https://www.learncpp.com/cpp-tutorial/constexpr-and-consteval-functions/" target="_blank">5.8 - Constexpr and consteval function, Learn C++</a>, emphasis mine.
    </footer>
</blockquote><p></p>

Basically, because `constexpr` functions must be evaluable at run time, their
parameters cannot themselves be `constexpr`.

But it still feels like the `constexpr`-ness could be inferred in the broken
version of `dummy()`. The trouble is, the function must be callable at 
runtime - with values that are not known until runtime - so the value of the
parameter might not be known at compile time, which is a requirement of
`constexpr`. Hence, function parameters, even `constexpr` and `consteval`
function parameters, cannot be `constexpr`.

<p></p><blockquote>
    <ul>
        <li>    
            <code>const</code> means that the value of an object cannot be changed
            after initialization. The value of the initializer may be known at
            compile-time or runtime. The <code>const</code> object can be evaluated at runtime.
        </li>
        <li>
            <code>constexpr</code> means that the object can be used in a constant expression.
            The value of the initializer must be known at compile-time. The <code>constexpr</code>
            object can be evaluated at runtime or compile-time.
        </li>
    </ul>
    <p>
        Normal function calls are evaluated at runtime, with the supplied arguments being used
        to initialize the function's parameters. Because the initialization of function
        parameters happens at runtime, this leads to two consequences:
    </p>
    <ol>
        <li>
            const function parameters are treated as runtime constants (even when the supplied 
            argument is a compile-time constant).
        </li>
        <li>   
            Function parameters cannot be declared as constexpr, since their initialization 
            value isn’t determined until runtime.
        </li>
    </ol>
    <footer> --<a href="https://www.learncpp.com/cpp-tutorial/constexpr-and-consteval-functions/" target="_blank">5.8 - Constexpr and consteval function, Learn C++</a>, emphasis mine.
    </footer>
</blockquote><p></p>



