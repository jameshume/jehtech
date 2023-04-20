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