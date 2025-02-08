## Type Traits
Two kinds:

1. The first kind of type trait is a small class template that contains a constant value, where the value represents the answer to a question we ask about a type.

For example:

```c++
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

2. The second kind enables type transformation at compile time. E.g. adding or removing `const` qualifier,
or pointer/reference from a type. These are **metafunctions**.

## Substitution Failure Is Not An Error (SFINAE)
Used to restrict template types. For example creating a function template that only works with certain types.

SFINAE is now "old". The new kid on the block is C++20 concepts. This sections discusses SFINAE, however.

SFINAE means that when the compiler substitures arguments into a template (instanitation), if the substituation is invalid, it does *not* result in an error, just a deduction failure. It is only an error if no deduction succeeds, but if even one does, there is no error.

E.g.

```c++
#include <iostream>

template <typename T>
auto begin(T &c) { return c.begin(); }

template <typename T, size_t N>
T* begin(T (&arr)[N]) { return arr; }
```

If we do the following:

```c++
int myArray[] {1,2,3,4};
int *iter = begin(myArray);
```

The compile first tries to subsitute `int [4]` into the fist template. This fails. But there is no error because of SFINAE. It is just treated as a deduction failure and the compiler moves on to trying to
instantiate `int[4]` into the second template, which works, so it is chosen and create the following instantiation:

```c++
template<>
int* begin<int, 4>(int (&arr)[4])
{
  return arr;
}
```

## Use SFINAE To Eliminate Function Collision
Contrived, but ayway... There is bank A and bank B, both of which support SWIFT transfers. We cannot modify their API.

```
class BankA_Account {
public:
    // ...
    int transfer(double amount, SWIFT &destination) {
        // ...
        return 0;
    }
};

class BankB_Account {
public:
    // ...
    bool sendMoney(double amount, SWIFT &destination) {
        // ...
        return true;
    }
};
```

I want to be able to have a generic function `bool transfer(??? BankAccount, double amount, SWIFT &destination)` that can accept a bank A or bank B account.

As neither Bank A nor bank B inherit from a common ancestor runtime polymorphism is not possible. So the
solution might be templates. Lets try:

```
template <typename T>
bool transfer(T& account, double amount, SWIFT &destination) {
    return account.transfer(amount, destination) != -1;
}

template <typename T>
bool transfer(T& account, double amount, SWIFT &destination) {
    return account.sendMoney(amount, destination);
}
```

Nope. The compiler gives us the following warning:

```
main.cpp:31:6: error: redefinition of 'transfer'
bool transfer(T& account, double amount, SWIFT &destination) {
     ^
main.cpp:26:6: note: previous definition is here
bool transfer(T& account, double amount, SWIFT &destination) {
```

[[See full example here]](https://cpp.sh/?source=%23include%20%3Ciostream%3E%0A%0Aclass%20SWIFT%20%7B%0A%7D%3B%0A%0Aclass%20BankA_Account%20%7B%0Apublic%3A%0A%20%20%20%20%2F%2F%20...%0A%20%20%20%20int%20transfer%28double%20amount%2C%20SWIFT%20%26destination%29%20%7B%0A%20%20%20%20%20%20%20%20%2F%2F%20...%0A%20%20%20%20%20%20%20%20return%200%3B%0A%20%20%20%20%7D%0A%7D%3B%0A%0Aclass%20BankB_Account%20%7B%0Apublic%3A%0A%20%20%20%20%2F%2F%20...%0A%20%20%20%20bool%20sendMoney%28double%20amount%2C%20SWIFT%20%26destination%29%20%7B%0A%20%20%20%20%20%20%20%20%2F%2F%20...%0A%20%20%20%20%20%20%20%20return%20true%3B%0A%20%20%20%20%7D%0A%7D%3B%0A%0A%0Atemplate%20%3Ctypename%20T%3E%0Abool%20transfer%28T%26%20account%2C%20double%20amount%2C%20SWIFT%20%26destination%29%20%7B%0A%20%20%20%20return%20account.transfer%28amount%2C%20destination%29%20%21%3D%20-1%3B%0A%7D%0A%0Atemplate%20%3Ctypename%20T%3E%0Abool%20transfer%28T%26%20account%2C%20double%20amount%2C%20SWIFT%20%26destination%29%20%7B%0A%20%20%20%20return%20account.sendMoney%28amount%2C%20destination%29%3B%0A%7D%0A%0Aint%20main%28%29%20%7B%0A%20%20%20%20return%200%3B%0A%7D)

