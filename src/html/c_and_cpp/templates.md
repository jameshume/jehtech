## Type Traits
Type traits are small class templates that contain a constant value where the value represents the mswer to a question we ask about a type.

For example:

```
#include <iostream>

class MyClass {
};

template <typename T>
struct is_my_class
{
    static const bool value = false;
};


template <>
struct is_my_class<MyClass>
{
    static const bool value = true;
};


int main() {
    std::cout << "Int is MyClass? " << is_my_class<int>::value << "\n";
    std::cout << "MyClass is MyClass? " << is_my_class<MyClass>::value << "\n";
    return 1;
}

///
/// Outputs:
/// Int is MyClass? 0
/// MyClass is MyClass? 1
```
