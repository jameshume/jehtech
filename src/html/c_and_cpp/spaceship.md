## C++20 Spaceship Operator (`<=>`)
* Pre C++20 requires 6 oeprators for your class to support all kinds of comparisons
    * `==`, `!=`, `<`, `<=`, `>`, `=>`
    * Although mostly all just based on `==` or `>`, a hassle!
* In C++20
    * `==` implies `!=`, so now only have to define `==`. `a != b` now tries `a != b`, `!(a == b)` and `!(b == a)`
    * No equivalent for the other operators, but now have `<=>`, which is the *only operator you now need to define*! Don't even need to define `==`!
        * `x <=> y == 0` when `x` and `y` are equal.
        * `x <=> y < 0` when `x < y`.
        * `x <=> y > 0` when `x > y`.
        * Thus, `x <= y`, can for example, be re-written as `(x <=> y) <= 0`, because if `x == y`, `(x <=> y)` will be `0`, and if `x < y`, `(x <=> y)` will be less than zero.
    * Comparison categories/ordering
        * *Strong (or total) ordering*. For every value of type T, that value can compared with every other value of type T as being less than, equal to or greater than.
        * *Weak ordering*. Same as strong except equality is replace with equivalence. Equivalent types do not have to be equal. E.g. "JEHTECH" is equivalent to
          "jehtech" but not equal.
        * *Patial ordering*. It may not be possible to to specify an order between any two values.
    * The return value of `<=>` should sepcify the comparison category/ordering. For example
        ```
        std::strong_ordering operator<=>(Type x, OtherType y) {...} // OR...
        std::weak_ordering operator<=>(Type x, OtherType y) {...}   // OR...
        std::partial_ordering operator<=>(Type x, OtherType y) {...}
        ```
    * The return value is `std::ORDERING_TYPE::less`, `std::ORDERING_TYPE::equal`, or `std::ORDERING_TYPE::greater`.
    * May find it useful, in your implementation to use `if constexpr (requires { some-func-or-property <=> other.some-func-or-property(); }) {` when trying
      to determine, at compile time, whether the types contained in your class/container themselves support the spaceship operator.

      
