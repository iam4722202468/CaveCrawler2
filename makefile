IDIR = ./includes
CC = g++

compiled ?= 0
ifeq ($(compiled),1)
	CPPFLAGS += -I$(IDIR) -std=c++11 -g -lsfml-graphics -lsfml-window -lsfml-system -D COMPILED
	_DEPS = main.h map.hpp drawMap.hpp controller.hpp ../gameClasses/object.hpp generatedMaps.h stringStuff.hpp
else
	CPPFLAGS += -I$(IDIR) -std=c++11 -g -lsfml-graphics -lsfml-window -lsfml-system
	_DEPS = main.h map.hpp drawMap.hpp controller.hpp readMapDynamic.h stringStuff.hpp
endif

ODIR = ./build
CPPDIR = ./src

DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

_OBJ = main.o map.o drawMap.o controller.o object.o stringStuff.o
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))

$(ODIR)/%.o: $(CPPDIR)/%.cpp $(DEPS)
	$(CC) -c -o $@ $< $(CPPFLAGS)

all: main-build-seperate

seperate: main-build-seperate
compiled: main-build-compiled
maps: maps-only

maps-only:
	python generateMaps.py seperate

pre-build-compiled:
	python generateMaps.py compiled

pre-build-seperate:
	python generateMaps.py seperate

main-build-seperate: pre-build-seperate
	cd gameClasses; make --no-print-directory
	@$(MAKE) --no-print-directory main

main-build-compiled: pre-build-compiled
	cd gameClasses; make --no-print-directory
	@$(MAKE) --no-print-directory main

main: $(OBJ)
	$(CC) -o $@ $^ $(CPPFLAGS)

.PHONY: clean

clean:
	rm -f $(ODIR)/*.o rm main
