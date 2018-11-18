IDIR = ./includes
CC = g++

CPPFLAGS += -I$(IDIR) -std=c++11 -g -lsfml-graphics -lsfml-window -lsfml-system
DEPS = GameController.hpp stringStuff.hpp ../gameObjects/object.hpp

ODIR = ./build
CPPDIR = ./src

DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

_OBJ = main.o GameController.o object.o stringStuff.o
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))

$(ODIR)/%.o: $(CPPDIR)/%.cpp $(DEPS)
	$(CC) -c -o $@ $< $(CPPFLAGS)

all: main-objects

maps:
	python generateMaps.py

main-objects: maps
	cd gameClasses; make --no-print-directory
	@$(MAKE) --no-print-directory main

main: $(OBJ)
	$(CC) -o $@ $^ $(CPPFLAGS)

.PHONY: clean

clean:
	rm -f $(ODIR)/*.o rm main
