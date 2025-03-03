cmake_minimum_required(VERSION 3.10)

# Указываем имя проекта
project(GraphProject)

# Указываем минимальную версию C++
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Добавляем путь к заголовочным файлам
include_directories(${CMAKE_SOURCE_DIR}/include)

# Собираем все .cpp файлы из папки src
file(GLOB SOURCES ${CMAKE_SOURCE_DIR}/src/*.cpp)

# Добавляем исполняемый файл
add_executable(GraphProject ${CMAKE_SOURCE_DIR}/main.cpp ${SOURCES})