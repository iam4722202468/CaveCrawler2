IDIR = .
CC = g++

CPPFLAGS += -I$(IDIR) -std=c++11 -g -lsfml-graphics -lsfml-window -lsfml-system

ODIR = ../build
CPPDIR = .

_DEPS = object.hpp
DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

_OBJ = object.o
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))

$(ODIR)/%.o: $(CPPDIR)/%.cpp
	$(CC) -c -o $@ $< $(CPPFLAGS)

all: main

main: $(OBJ)
	@echo Compiled game classes
