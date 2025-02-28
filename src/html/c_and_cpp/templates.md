## Good Vids Etc
<p></p>
<iframe 
    width="560"
    height="315"
    src="https://www.youtube.com/embed/Am2is2QCvxY?si=0xlCsJCRZGFdwD7B"
    title="YouTube video player"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    referrerpolicy="strict-origin-when-cross-origin"
    allowfullscreen>
</iframe>
<p></p>

## Credits
The follow section is very heavily based on ["Template Metaprogramming with C++" by Marious Bancila](https://www.packtpub.com/en-ph/product/template-metaprogramming-with-c-9781803243450).
I just changed some of the examples to encuorage my brain to mull it over more thoroughly and have tried to explain 
things to myself in more detaill (read bigger pictures smaller words).

## Type Traits
Two kinds:

1. The first kind of type trait is a small class template that contains a constant value, where the value represents the answer to a question we ask about a type.

For example:

```cpp
#include <iostream>

class MyClass {
};

template <typename T>
struct is_my_class
{
    static constexpr bool value = false;
};


template <>
struct is_my_class<MyClass>
{
    static constexpr bool value = true;
};

template <typename T>
inline constexpr bool is_my_class_v = is_my_class<T>::value;

int main() {  
    std::cout << "Int is MyClass? " << is_my_class_v<int> << "\n";
    //                                 ^^ Shorthand for `is_my_class<int>::value`

    std::cout << "MyClass is MyClass? " << is_my_class_v<MyClass> << "\n";
    //                                     ^^ shorthad for `is_my_class<MyClass>::value`
    
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

```cpp
#include <iostream>

template <typename T>
auto begin(T &c) { return c.begin(); }

template <typename T, size_t N>
T* begin(T (&arr)[N]) { return arr; }
```

If we do the following:

```cpp
int myArray[] {1,2,3,4};
int *iter = begin(myArray);
```

The compile first tries to subsitute `int [4]` into the fist template. This fails. But there is no error because of SFINAE. It is just treated as a deduction failure and the compiler moves on to trying to
instantiate `int[4]` into the second template, which works, so it is chosen and create the following instantiation:

```cpp
template<>
int* begin<int, 4>(int (&arr)[4])
{
  return arr;
}
```

So, to recap, rather than causing a hard error, this first candidate was removed from consideration. This is a key part of the SFINAE (Substitution Failure Is Not An Error) rule:

1. The compiler considers all viable template candidates.
2. It attempts to substitute the provided arguments into each template.
3. If substitution fails for a candidate, that candidate is removed from consideration (instead of causing a hard error).
4. The most specific remaining candidate is selected. If there is ambiguity or no valid candidate, compilation fails.



### Not SFINAE But Sets The Ground Work For How Its Useful
Contrived, but anyway... There is bank A and bank B, both of which support SWIFT transfers. We cannot modify their API.

```cpp
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

As neither Bank A nor bank B inherit from a common ancestor runtime polymorphism is not possible. We could write wrapper classes that derive from a common base, 
and this might be a good way of doing it. Some downsides might be incurring the cost of the VTable lookups, having to write a wrapper for every bank API provider,
etc. But, not considering that here... its just a contrived example to show some SFINAE... not saying this is how the problem should be solved.

So, continuing, the solution might be templates. Lets try:

```cpp
template <typename T>
bool transfer(T& account, double amount, SWIFT &destination) {
    return account.transfer(amount, destination) != -1;
}

template <typename T>
bool transfer(T& account, double amount, SWIFT &destination) {
    return account.sendMoney(amount, destination);
}
```

Nope. The compiler, unsuprisingly, gives us the following warning:

```
main.cpp:31:6: error: redefinition of 'transfer'
bool transfer(T& account, double amount, SWIFT &destination) {
     ^
main.cpp:26:6: note: previous definition is here
bool transfer(T& account, double amount, SWIFT &destination) {
```

[[See full example here]](https://cpp.sh/?source=%23include%20%3Ciostream%3E%0A%0Aclass%20SWIFT%20%7B%0A%7D%3B%0A%0Aclass%20BankA_Account%20%7B%0Apublic%3A%0A%20%20%20%20%2F%2F%20...%0A%20%20%20%20int%20transfer%28double%20amount%2C%20SWIFT%20%26destination%29%20%7B%0A%20%20%20%20%20%20%20%20%2F%2F%20...%0A%20%20%20%20%20%20%20%20return%200%3B%0A%20%20%20%20%7D%0A%7D%3B%0A%0Aclass%20BankB_Account%20%7B%0Apublic%3A%0A%20%20%20%20%2F%2F%20...%0A%20%20%20%20bool%20sendMoney%28double%20amount%2C%20SWIFT%20%26destination%29%20%7B%0A%20%20%20%20%20%20%20%20%2F%2F%20...%0A%20%20%20%20%20%20%20%20return%20true%3B%0A%20%20%20%20%7D%0A%7D%3B%0A%0A%0Atemplate%20%3Ctypename%20T%3E%0Abool%20transfer%28T%26%20account%2C%20double%20amount%2C%20SWIFT%20%26destination%29%20%7B%0A%20%20%20%20return%20account.transfer%28amount%2C%20destination%29%20%21%3D%20-1%3B%0A%7D%0A%0Atemplate%20%3Ctypename%20T%3E%0Abool%20transfer%28T%26%20account%2C%20double%20amount%2C%20SWIFT%20%26destination%29%20%7B%0A%20%20%20%20return%20account.sendMoney%28amount%2C%20destination%29%3B%0A%7D%0A%0Aint%20main%28%29%20%7B%0A%20%20%20%20return%200%3B%0A%7D)

So what can be done?! Template trickery to make sure the compiler only "sees" on of the definitions of `transfer` is the answer :o

First of all a type trait:
```cpp
template <typename T>
struct bank_account_uses_transfer_method {
    static constexpr bool value = false;
};

template <>
struct bank_account_uses_transfer_method<BankA_Account> {
    static constexpr bool value = true;
}

template <typename T>
inline constexpr bool bank_account_uses_transfer_method_v = bank_account_uses_transfer_method<T>::value;
```

Now we can determine at compile time whether a bank account has the transfer function.

Next we need to stop one of the `transfer` definitions from being considered at all. Do this
by adding a boolean switch as a non-type template parameter: 

```cpp
template <typename T, bool uses_transfer>
bool transfer(T& account, double amount, SWIFT &destination) {
    return account.sendMoney(amount, destination) != -1;
}

template <typename T, true>
bool transfer(T& account, double amount, SWIFT &destination) {
    return account.transfer(amount, destination);
}
```

Nope, we get this error:

```
error: function template partial specialization is not allowed
bool transfer<true>(T& account, double amount, SWIFT &destination) {
     ^       ~~~~~~
1 error generated.
```

In C++ **function template partial specialisation is not allowed**. The way round this is to wrap the functions in a class.

```cpp
template <bool> // Anonymous non-type parameter - not used in impl
struct transfer_wrapper {
    template <typename T>
    static bool transfer(T& account, double amount, SWIFT &destination) {
        return account.sendMoney(amount, destination) != -1;
    }
};

template<>
struct transfer_wrapper<true> {
    template <typename T>
    static bool transfer(T& account, double amount, SWIFT &destination) {
        return account.transfer(amount, destination);
    }
};
```

Now, is we have an object of either bank type we can do:

```cpp
transfer_wrapper<bank_account_uses_transfer_method_v<MY_BANK_OBJ>>::template transfer<MY_BANK_OBJ>(account, amount, destination);
```

As a side note, why did we need to use the `template` keyword in `...template transfer<MY_BANK_OBJ>(...` above? Without template, the compiler assumes transfer could be a normal static member (not a template) and the keyword disamiguates this.

We can tidy this up using another template function...

```cpp
template <typename T>
static bool transfer(T& account, double amount, SWIFT &destination) {
    return transfer_wrapper<bank_account_uses_transfer_method_v<T>>::template transfer<T>(account, amount, destination);
}
```

Which, in turn, can be further tidied because `transfer()`'s `T` can be inferred:

```cpp
template <typename T>
static bool transfer(T& account, double amount, SWIFT &destination) {
    return transfer_wrapper<bank_account_uses_transfer_method_v<T>>::template(account, amount, destination);
}
```

The whole thing becomes:

```cpp
#include <iostream>

class SWIFT {
};

class BankA_Account {
public:
    // ...
    int transfer(double amount, SWIFT &destination) {
        // ...
        std::cout<< "Bank A transfer " << amount << "\n";
        return 0;
    }
};

class BankB_Account {
public:
    // ...
    bool sendMoney(double amount, SWIFT &destination) {
        // ...
        std::cout<< "Bank B transfer " << amount << "\n";
        return true;
    }
};

template <typename T>
struct bank_account_uses_transfer_method {
    static constexpr bool value = false;
};

template <>
struct bank_account_uses_transfer_method<BankA_Account> {
    static constexpr bool value = true;
};

template <typename T>
inline constexpr bool bank_account_uses_transfer_method_v = bank_account_uses_transfer_method<T>::value;

template <bool> // Anonymous non-type parameter - not used in impl
struct transfer_wrapper {
    template <typename T>
    static bool transfer(T& account, double amount, SWIFT &destination) {
        return account.sendMoney(amount, destination) != -1;
    }
};

template<>
struct transfer_wrapper<true> {
    template <typename T>
    static bool transfer(T& account, double amount, SWIFT &destination) {
        return account.transfer(amount, destination);
    }
};

template <typename T>
static bool transfer(T& account, double amount, SWIFT &destination) {
    return transfer_wrapper<bank_account_uses_transfer_method_v<T>>::transfer(account, amount, destination);
}

int main() {
    SWIFT s;
    BankA_Account a;
    BankB_Account b;
    
    transfer(a, 11, s);
    transfer(b, 321, s);
    
    return 0;
}

// Outputs:
// Bank A transfer 11
// Bank B transfer 321
```
[[See full example here]](https://cpp.sh/?source=%23include+%3Ciostream%3E%0D%0A%0D%0Aclass+SWIFT+%7B%0D%0A%7D%3B%0D%0A%0D%0Aclass+BankA_Account+%7B%0D%0Apublic%3A%0D%0A++++%2F%2F+...%0D%0A++++int+transfer(double+amount%2C+SWIFT+%26destination)+%7B%0D%0A++++++++%2F%2F+...%0D%0A++++++++std%3A%3Acout%3C%3C+%22Bank+A+transfer+%22+%3C%3C+amount+%3C%3C+%22%5Cn%22%3B%0D%0A++++++++return+0%3B%0D%0A++++%7D%0D%0A%7D%3B%0D%0A%0D%0Aclass+BankB_Account+%7B%0D%0Apublic%3A%0D%0A++++%2F%2F+...%0D%0A++++bool+sendMoney(double+amount%2C+SWIFT+%26destination)+%7B%0D%0A++++++++%2F%2F+...%0D%0A++++++++std%3A%3Acout%3C%3C+%22Bank+B+transfer+%22+%3C%3C+amount+%3C%3C+%22%5Cn%22%3B%0D%0A++++++++return+true%3B%0D%0A++++%7D%0D%0A%7D%3B%0D%0A%0D%0Atemplate+%3Ctypename+T%3E%0D%0Astruct+bank_account_uses_transfer_method+%7B%0D%0A++++static+constexpr+bool+value+%3D+false%3B%0D%0A%7D%3B%0D%0A%0D%0Atemplate+%3C%3E%0D%0Astruct+bank_account_uses_transfer_method%3CBankA_Account%3E+%7B%0D%0A++++static+constexpr+bool+value+%3D+true%3B%0D%0A%7D%3B%0D%0A%0D%0Atemplate+%3Ctypename+T%3E%0D%0Ainline+constexpr+bool+bank_account_uses_transfer_method_v+%3D+bank_account_uses_transfer_method%3CT%3E%3A%3Avalue%3B%0D%0A%0D%0Atemplate+%3Cbool%3E+%2F%2F+Anonymous+non-type+parameter+-+not+used+in+impl%0D%0Astruct+transfer_wrapper+%7B%0D%0A++++template+%3Ctypename+T%3E%0D%0A++++static+bool+transfer(T%26+account%2C+double+amount%2C+SWIFT+%26destination)+%7B%0D%0A++++++++return+account.sendMoney(amount%2C+destination)+!%3D+-1%3B%0D%0A++++%7D%0D%0A%7D%3B%0D%0A%0D%0Atemplate%3C%3E%0D%0Astruct+transfer_wrapper%3Ctrue%3E+%7B%0D%0A++++template+%3Ctypename+T%3E%0D%0A++++static+bool+transfer(T%26+account%2C+double+amount%2C+SWIFT+%26destination)+%7B%0D%0A++++++++return+account.transfer(amount%2C+destination)%3B%0D%0A++++%7D%0D%0A%7D%3B%0D%0A%0D%0Atemplate+%3Ctypename+T%3E%0D%0Astatic+bool+transfer(T%26+account%2C+double+amount%2C+SWIFT+%26destination)+%7B%0D%0A++++return+transfer_wrapper%3Cbank_account_uses_transfer_method_v%3CT%3E%3E%3A%3Atransfer(account%2C+amount%2C+destination)%3B%0D%0A%7D%0D%0A%0D%0Aint+main()+%7B%0D%0A++++SWIFT+s%3B%0D%0A++++BankA_Account+a%3B%0D%0A++++BankB_Account+b%3B%0D%0A++++%0D%0A++++transfer(a%2C+11%2C+s)%3B%0D%0A++++transfer(b%2C+321%2C+s)%3B%0D%0A++++%0D%0A++++return+0%3B%0D%0A%7D)

Note, that SFINAE has not yet been used. In the above example there were no substitution failures. The following is an example of the type deduction suceeding:

```cpp
template <bool> 
struct transfer_wrapper {
    template <typename T> // [T == BankA_Account]
    static bool transfer(T /*[BankA_Account]*/ & account, double amount, SWIFT &destination) {
        return account.sendMoney(amount, destination) != -1; //< This does **NOT** cause a deduction failure because SFINAE only applies
                                                             //  to template params, function return type and params.
    }
};
```

Had the above deduction been *chosen*, it would have resulted in a compile time error: the compiler would have complained that the type `BankA_Account`
does not have a member function `sendMoney()`! The reason the compile time error did not arise is that this candidate would not be chosen (and therefore
realised), because the more specialised template would have been chosen. Thus, SFINAE is not in use here. Just the normal template deduction and
selection process.

And breath... There is a lot of complexity here and its quite hard to read. Next we see how enabling SFINAE help reduce this complexity and makes things easier to read.

### Making The Previous Example Neater Using SFINAE (Using `enable_if`)
The type trait `enable_if` is a metafunction. It will help do what we did above but this time by enabling SFINAE to remove candatates from a function's overload set.

A [possible implementation](https://en.cppreference.com/w/cpp/types/enable_if) is this:

```cpp
template<bool B, class T = void>
struct enable_if {};
 
template<class T>
struct enable_if<true, T> { typedef T type; };
```

Remember earlier, when we wanted to write the following, but couldn't because functions templates cannot be partially specialised?

```cpp
template <typename T, bool uses_transfer>
bool transfer(T& account, double amount, SWIFT &destination) {
    return account.sendMoney(amount, destination) != -1;
}

template <typename T, true>
bool transfer(T& account, double amount, SWIFT &destination) {
    return account.transfer(amount, destination);
}
```

Well, now, with a little fiddle, we can!

```cpp
template <typename T, 
          typename std::enable_if<!bank_account_uses_transfer_method_v<T>>::type* = nullptr
>
bool transfer(T& account, double amount, SWIFT &destination) {
    return account.sendMoney(amount, destination) != -1;
}

template <typename T,
          typename std::enable_if<bank_account_uses_transfer_method_v<T>>::type* = nullptr
>
bool transfer(T& account, double amount, SWIFT &destination) {
    return account.transfer(amount, destination) != -1;
}
```

And this is all we need. We don't need the wrapping structures or the generic function that hides the use of the structs etc. It also reads more easily. Each function is only enabled if the condition bank_account_uses_transfer_method_v is met or not.

How does it work? In the example before, we saw that the body of the function wasn't used during the deduction process, so
previously, when the compiler tried to substitute `BankA_Account` into the template that used `T.sendMoney`, this would
not influence the deduction, hence the trick with the wrapper class. However, using `enable_if` we have now forced that
substitution to happen in the template parameter list, and hence it will take part in the deduction!

Lets be the compiler and choose `T` as `BankA_Account`. The first of the template functions above becomes:

```cpp
template <BankA_Account, 
          typename std::enable_if<!bank_account_uses_transfer_method_v<BankA_Account>>::type* = nullptr
>
bool transfer(BankA_Account& account, double amount, SWIFT &destination) { ...account.sendMoney... }
```

Because `bank_account_uses_transfer_method_v<BankA_Account>` is `true` we get:

```cpp
template <BankA_Account, 
          typename std::enable_if<false>::type* = nullptr
>
bool transfer(BankA_Account& account, double amount, SWIFT &destination) { ...account.sendMoney... }
```

Expanding further:

```cpp
template <BankA_Account, 
          typename struct {}::type* = nullptr
>
bool transfer(BankA_Account& account, double amount, SWIFT &destination) { ...account.sendMoney... }
```

Oops substitution failure! `struct {}` has no static member `type`. Substitution fails, removing this function overload
from the set of viable candidates.

What happens with the other function, when `T` is `BankA_Account`?

```cpp
template <BankA_Account,
          typename std::enable_if<bank_account_uses_transfer_method_v<BankA_Account>>::type* = nullptr
>
bool transfer(T& account, double amount, SWIFT &destination) { ...account.transfer... }
```

This becomes:

```cpp
template <BankA_Account,
          typename std::enable_if<true>::type* = nullptr
>
bool transfer(T& account, double amount, SWIFT &destination) { ...account.transfer... }
```

And then:

```cpp
template <BankA_Account,
          struct { typedef BankA_Account type; }::type* = nullptr
>
bool transfer(T& account, double amount, SWIFT &destination) { ...account.transfer... }
```

Which is:

```cpp
template <BankA_Account,
          BankA_Account* = nullptr
>
bool transfer(T& account, double amount, SWIFT &destination) { ...account.transfer... }
```

Which works! The type is successfully deduces as `BankA_Account`. 

This `enable_if` has allowed us to select a function instatiation at compile time!