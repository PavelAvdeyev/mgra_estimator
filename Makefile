DIST_DIR := measures/cpp_impl
BIN_DIR := $(shell pwd)/lib

#setting compiler (if not set)
ifeq (${CXX},)
	IS_CLANG := $(shell which clang++ >/dev/null 2>&1; echo $$?)
	IS_GCC := $(shell which g++ >/dev/null 2>&1; echo $$?)

	ifeq (${IS_CLANG},0)
		CXX := clang++
		
	else ifeq (${IS_GCC},0)
		CXX := g++

	else
	err:
		$(error Neither gcc nor clang compilers were detected.)
	endif
endif

#adding necessary flags
CXXFLAGS += -std=c++11
UNAME := $(shell uname -s)
ifeq ($(UNAME),Darwin)
	CXXFLAGS += -stdlib=libc++
	LDFLAGS += -lc++
endif

export CXX
export CXXFLAGS
export LDFLAGS
export BIN_DIR

.PHONY: all distance clean

all: distance

distance:
	make -C ${DIST_DIR} all

clean:
	make -C ${DIST_DIR} clean
