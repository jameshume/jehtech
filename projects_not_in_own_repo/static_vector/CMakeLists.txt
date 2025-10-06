cmake_minimum_required(VERSION 3.31)

# Project name and language
project(StaticBuffer LANGUAGES CXX)

# Specify C++ standard
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add the executable
add_executable(static_buffer
    main.cpp
)