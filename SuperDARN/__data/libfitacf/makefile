all: fitacf.o libfitacf.so

fitacf.o:
	gcc -c -fpic fitacf.c

libfitacf.so:
	gcc -shared fitacf.o -o libfitacf.so -lm

clean:
	rm fitacf.o libfitacf.so
