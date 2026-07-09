cmake_minimum_required(VERSION 3.8)
project(intercropping_gz)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY
    config
    models
    worlds
  DESTINATION share/${PROJECT_NAME}
)

install(
  PROGRAMS
    scripts/generate_world.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()