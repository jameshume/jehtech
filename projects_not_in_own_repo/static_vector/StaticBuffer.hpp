#pragma once

#include <cstddef>
#include <cstdint>
#include <cstring>

#include <type_traits>

void abort(void) {
    while(1);
}

template<typename T, std::size_t ELEMS>
class StaticVector final {
public:
    // Empty constructor - zeros the storage
    template <bool CompileTime>
    constexpr StaticVector() : m_next_free_index(0) {
        m_zero_data<std::is_constant_evaluated()>();
    }

    // Capacity is the maximum number of elements that can be added to the vector
    constexpr std::size_t capacity() const {
        return ELEMS;
    }

    // The array index operator overload - always checks bounds
    constexpr T& operator[](const std::size_t index) {
        if (index < ELEMS) {
            return static_cast<T*>(m_data)[index];
        }
        else {
            abort();
        }
    }

private:
    template <bool CompileTime>
    constexpr void m_zero_data() {
        if constexpr (CompileTime) {
            for (std::size_t i = 0; i < sizeof(m_data); ++i) {
                m_data[i] = 0;
            }
        } 
        else {
            std::memset(m_data, 0, sizeof(m_data));
        }
    }

    alignas(alignof(T)) std::uint8_t m_data[sizeof(T) * ELEMS];
    
    std::size_t m_next_free_index; 
};


