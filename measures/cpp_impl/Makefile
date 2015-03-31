CXXFLAGS += -std=c++11
OUT_BIN := ${BIN_DIR}/distance

.PHONY: all clean debug

all: CXXFLAGS += -O2 
all: distance

debug: CXXFLAGS += -g -D_GLIBCXX_DEBUG -D_DEBUG
debug: distance

objects := ${patsubst %.cpp,%.o,${wildcard *.cpp}}

distance: ${objects}
	${CXX} ${LDFLAGS} ${objects} -o ${OUT_BIN}

%.o: %.cpp *.h
	${CXX} -c ${CXXFLAGS} $< -o $@

clean:
	rm *.o
	rm ${OUT_BIN}
