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
[[Run code here]](https://cpp.sh/?source=%23include+%3Ciostream%3E%0A%0Aclass+MyClass+%7B%0A%7D%3B%0A%0Atemplate+%3Ctypename+T%3E%0Astruct+is_my_class%0A%7B%0A++++static+const+bool+value+%3D+false%3B%0A%7D%3B%0A%0A%0Atemplate+%3C%3E%0Astruct+is_my_class%3CMyClass%3E%0A%7B%0A++++static+const+bool+value+%3D+true%3B%0A%7D%3B%0A%0A%0Aint+main()+%7B%0A++++std%3A%3Acout+%3C%3C+%22Int+is+MyClass%3F+%22+%3C%3C+is_my_class%3Cint%3E%3A%3Avalue+%3C%3C+%22%5Cn%22%3B%0A++++std%3A%3Acout+%3C%3C+%22MyClass+is+MyClass%3F+%22+%3C%3C+is_my_class%3CMyClass%3E%3A%3Avalue+%3C%3C+%22%5Cn%22%3B%0A%7D)

