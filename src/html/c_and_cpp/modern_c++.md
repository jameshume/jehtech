## Readable numbers - digit grouping
```
10'000; // Use apostrophe to group digits
```

## Vectors

```
using std::vector;
...
vector numbers {0, 1, 2, 3}; // Note do not need template arg in C++17 - compiler will deduce - Class template argument deduction (CTAD)

// Push back - will COPY without std::move - we use std::move if we like.
numbers.push_back(4);

// Access using array style bracket operator
numbers[0] = 42;

// Range based for loop
for (auto i : numbers)
{
    // Do something with i
}

// Vectors like to COPY on resize - but they also MOVE if the contents are moveable.
```


## Array
Does not grow.
May be on the stack.
Collection whose size is known at compile time.

```

```

## List


## Map

## Multimap

## Unordered Map / Multimap

## Stack

## Dequeue

## Priority Queue

## Lambdas

If assigning to a variable must declare that variable `auto` - there is no other option.

```
[] () -> return_type {}
^^ ^^ ^^ ^^^^^^^^^^^
^^ ^^ ^^ Return type is optional - compiler can try to deduce this
^^ ^^ Function body
^^ Function parameters
Capture clause
Makes variables from the calling scope usable in the the lambda
So when capture clause is empty the function will only work with the parameters passed into it.
If you capture by *value* ([foo, bar, ...]), they are *copied* into lambda.
    Use "mutable" to change the values of variables captures by value - note only changes the local copy though!
If you capture by *reference* ([&foo, &bar, ...]) no copies are made. Changes in the lambda to these variables will affect the originals.
    Beware *dangling reference dangers* here!
Capture by *alias* ([bar=foo+1, ...])
Capture by *move* ([x=std::move(bar), ...])
Capture everything in the calling scope that is specifically used by the lambda *by value* ([=])
Capture everything in the calling scope that is specifically used by the lambda *by reference* ([&])
```



Compiler will, behind the scenes, generate a function object using the code from the lambda. Usee C++ insights to see whats going on:

```
TODO show CPP insights tool use
```

## Move Semantics


## Chrono

## Value type?
`T::template value_type varname(..._)`???

## Movable stuff
[Clever chap answered my questions here](https://stackoverflow.com/a/79297267/1517244). Notes as I went along are:

Note: Deleting the move operators is not the same as as not defining them when a copy constructor/assignment is
defined. 

In the latter scenario the move functions are not implicitly defined by the compiler and because
they dont exist, will not be considered in overload resolution. However, the object is still considered
moveable by is_move_constructible_v et al because the copy constructor accepting a `const` reference can
accept an R-value.
   
However, in the former scenario, when the move functions are explicitly deleted, the move functions *can* 
be considered in the overload resolution because deleted members are still declared. Deleted members 
participate in overload resolution. Members not present don't. 
Reason is this: Deleting of normal member function or nonmember functions prevents problematic type 
promotions from causing an unintended function to be called. This works because deleted 
functions still participate in overload resolution and provide a better match than the 
function that could be called after the types are promoted.
See: https://learn.microsoft.com/en-us/cpp/cpp/explicitly-defaulted-and-deleted-functions

This leave me with the question, why was is_move_constructible defined this way? Why not make it only
be true when there is a default or explicitly defiend move constructor? The answer is that 
`is_move_constructible` is just defined as the object can be constructed from an rvalue: how it's
constructed doesn't matter. It's constructed by a copy constructor, or a move constructor, and how the
constructor is implemented, like if it's actually doing a "move", doesn't matter