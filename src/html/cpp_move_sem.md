## A Silly Example

```cpp
// Use `g++ demo_no_move_sem.cpp -O0 -fno-elide-constructors && ./a.out`
// `-fno-elide-constructors` disable return value optimization.
#include <cstring>
#include <iostream>
#include <iterator>

class MyIntArray {
public:
    MyIntArray(unsigned int size) : m_name(nullptr) {
        std::cout << "\tNew empty array\n";
        m_array = new int[size];
        m_size = size;
        std::memset(m_array, 0, sizeof(int) * m_size);
    }
    
    ~MyIntArray() {
        if (m_name) {
            std::cout << "\tDead " << m_name << "\n";
        }
        else {
            std::cout << "\tDead annon\n";
        }
        delete[] m_array;
    }

    MyIntArray(int *array, unsigned int size) : m_name(nullptr) {
        std::cout << "\tNew initialised array\n";
        m_array = new int[size];
        m_size = size;
        std::memcpy(m_array, array, sizeof(int) * m_size);
    }

    MyIntArray(const MyIntArray &other) : m_name(nullptr) {
        std::cout << "\tNew copied array\n";
        m_array = new int[other.m_size];
        m_size = other.m_size;
        std::memcpy(m_array, other.m_array, sizeof(int) * m_size);
    }

    MyIntArray combine(const MyIntArray other) {     
        std::cout << "\tCombine\n";
        MyIntArray newArray(m_size + other.m_size);
        newArray.set_name("newArray");
        std::memcpy(newArray.m_array, m_array, sizeof(int) * m_size);
        std::memcpy(&newArray.m_array[m_size], other.m_array, sizeof(int) * other.m_size);
        std::cout << "\tNew array setup\n";
        return newArray;
    }

    int& operator[](int index) const {
        if (index < 0 || index >= m_size) {
            std::cout << "Index out of bounds\n";
            exit(1);
        }
        return m_array[index];
    }

    void set_name(const char *name) {
        m_name = name;
    }

    unsigned int get_size() const {
        return m_size;
    }

private:
    int *m_array;
    unsigned int m_size;
    const char *m_name;
};


std::ostream& operator<<(std::ostream& os, MyIntArray obj) {
    os << "[";
    for(unsigned int i = 0; i < obj.get_size(); ++i) {
        os << obj[i] << ", ";
    }
    os << "]\n";
    
    return os;
}

int main(void) {
    constexpr unsigned int ARRAYSIZE = 10;
    int data[10];
    for(unsigned int i = 0; i < ARRAYSIZE; ++i) {
        data[i] = (int) i;
    }

    std::cout << "a1\n";
    MyIntArray a1(data, ARRAYSIZE);
    a1.set_name("a1");

    std::cout << "a2\n";
    MyIntArray a2(data, ARRAYSIZE);
    a2.set_name("a2");

    std::cout << "Print combined array\n";
    std::cout << a1.combine(a2) << "\n";

    std::cout << "END\n";

    return 0;
}
```

When compiled using `-O0 -fno-elide-constructors` to disable optimisations *and* return value optimisation, the following is output:

```
a1
        New initialised array
a2
        New initialised array
Print combined array
        New copied array    //< [1] `a2` copied into `combine()` parameter `other` as anonymous array
        Combine
        New empty array     //< [2] Temp new array constructed to hold combination result
        New array setup
        New copied array    //< [3] Temp array copied into `std::cout` param as anonymous array
        Dead newArray       //< [4] As function exists temp new array destroyed
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ]

        Dead annon          //< [5] The `combine()` anonymous array param destroyed
        Dead annon          //< [6] The `std::cout` param destroyed 
END
        Dead a2
        Dead a1
```

If return value optimisations are allowed then the output is:

```
a1
        New initialised array
a2
        New initialised array
Print combined array
        New copied array    //< [1] `a2` copied into `combine()` parameter `other` as anonymous array
        Combine
        New empty array     //< [2] Temp new array constructed to hold combination result
        New array setup
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ]
                            //< [3] NOTE: No copy now
        Dead newArray       //< [4] As function exists temp new array destroyed
                            //< [5] NOTE: No extra anonmyous destoryed due to [3]
        Dead annon          //< [6] The `std::cout` param destroyed 
END
        Dead a2
        Dead a1
```

Next use const expression to extend the lifetime of temporary objects.

The `combine` function becomes:

```
 MyIntArray combine(const MyIntArray &other) { 
```

And the print function becomes:

```
std::ostream& operator<<(std::ostream& os, const MyIntArray &obj) {
```

Output is now:

```
a1
        New initialised array
a2
        New initialised array
Print combined array
        Combine
        New empty array
        New array setup
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ]

        Dead newArray
END
        Dead a2
        Dead a1
```