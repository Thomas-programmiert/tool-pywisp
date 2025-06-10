cmake_minimum_required(VERSION 3.24)

option(SIM "build for host system instead of cross-compiling" TRUE)

## dependencies
include(local.cmake OPTIONAL)
include(dependencies.cmake)

## Project declaration
project(Pendulum C CXX ASM)

message("preparing build for host system")
add_subdirectory(sim)

add_custom_target(visu
    COMMAND uv run visu/main.py
    COMMENT "run Pendulum visualization"
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)

