## Ubuntu 18.04.2 LTS (GNU/Linux 4.18.0-21-generic x86_64): PASS
#  Server with GUI or VM should modify source code to enable display module
mandelbrot_omp: mandelbrot_omp.c
	export DISPLAY=:0
	gcc mandelbrot_omp.c -o mandelbrot_omp -fopenmp -lGL -lGLU -lglut && ./mandelbrot_omp

# clean up
clean:
	rm -f mandelbrot_omp