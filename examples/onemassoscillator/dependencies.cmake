include(FetchContent)

FetchContent_Declare(tool-libs
	GIT_REPOSITORY https://github.com/umit-iace/tool-libs
	GIT_TAG master
	GIT_PROGRESS TRUE
)
FetchContent_MakeAvailable(tool-libs)
find_package(Eigen3 3.3 REQUIRED NO_MODULE)
