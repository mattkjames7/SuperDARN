# CFLAGS for CC
CFLAGS=-lm

# Compiler
CCo=g++ -fPIC -c $(CFLAGS)
CC=g++ -fPIC $(CFLAGS)


all: obj lib

obj:
	$(CCo) fitacf.cc -o fitacf.o
	$(CCo) libfitacf.cc -o libfitacf.o
	
lib:
	$(CC) -shared *.o -o libfitacf.so
	rm -v *.o

clean:
	rm -v libfitacf.so
