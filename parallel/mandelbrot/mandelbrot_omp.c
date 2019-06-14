#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <omp.h>
#ifdef __APPLE__
/* Defined before OpenGL and GLUT includes to avoid deprecation messages */
#define GL_SILENCE_DEPRECATION
#include <OpenGL/gl.h>
#include <GLUT/glut.h>
#else
#include <GL/gl.h>
#include <GL/glut.h>
#endif

/* Defaut data via command line */
/* Can enter other values via command line arguments */

#define CENTERX -0.5
#define CENTERY 0.5
#define HEIGHT 0.5
#define WIDTH 0.5
#define MAX_ITER 100

/* N x M array to be generated */

#define N 500
#define M 500
#define NUM_THREAD 2 // 1, 2, 4, 8

float height = HEIGHT; /* size of window in complex plane */
float width = WIDTH;
float cx = CENTERX; /* center of window in complex plane */
float cy = CENTERY; 
int max = MAX_ITER; /* number of interations per point */

int n=N;
int m=M;

/* Use unsigned bytes for image */

GLubyte image[N][M];

/* Complex data type and complex add, mult, and magnitude functions */
/* Probably not worth overhead */

typedef float complex[2];

void add(complex a, complex b, complex p)
{
    p[0]=a[0]+b[0];
    p[1]=a[1]+b[1];
}

void mult(complex a, complex b, complex p)
{
    p[0]=a[0]*b[0]-a[1]*b[1];
    p[1]=a[0]*b[1]+a[1]*b[0];
}

float mag2(complex a)
{
    return(a[0]*a[0]+a[1]*a[1]);
}

void form(float a, float b, complex p)
{
    p[0]=a;
    p[1]=b;
}

void display()
{
    glClear(GL_COLOR_BUFFER_BIT);
    glDrawPixels(n,m,GL_COLOR_INDEX, GL_UNSIGNED_BYTE, image);
}


void myReshape(int w, int h)
{
    glViewport(0, 0, w, h);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    if (w <= h)
    gluOrtho2D(0.0, 0.0, (GLfloat) n, (GLfloat) m* (GLfloat) h / (GLfloat) w);
    else
    gluOrtho2D(0.0, 0.0, (GLfloat) n * (GLfloat) w / (GLfloat) h,(GLfloat) m);
    glMatrixMode(GL_MODELVIEW);
    // display();
}

void myinit(int num_trds)
{
    float redmap[256], greenmap[256],bluemap[256];
    int i;

    glClearColor (1.0, 1.0, 1.0, 1.0);
    gluOrtho2D(0.0, 0.0, (GLfloat) n, (GLfloat) m);

/* Define pseudocolor maps, ramps for red and blue,
   random for green */

    #pragma omp parallel for num_threads(num_trds)
    for(i=0;i<256;i++) 
    {
         redmap[i]=i/255.;
         greenmap[i]=drand48();
         bluemap[i]=1.0-i/255.;
    }
    // printf("Initiate thread numbers: %d\n", omp_get_thread_num());

    glPixelMapfv(GL_PIXEL_MAP_I_TO_R, 256, redmap);
    glPixelMapfv(GL_PIXEL_MAP_I_TO_G, 256, greenmap);
    glPixelMapfv(GL_PIXEL_MAP_I_TO_B, 256, bluemap); 
}


int main(int argc, char *argv[])
{
    int i, j, k;
    float x, y, v;
    complex c0, c, d;
    double start = omp_get_wtime();

    if(argc>1) cx = atof(argv[1]); /* center x */
    if(argc>2) cy = atof(argv[2]);  /* center y */
    if(argc>3) height=width=atof(argv[3]); /* rectangle height and width */
    if(argc>4) max=atoi(argv[4]); /* maximum iterations */

    bool flag = false;
    #pragma omp parallel for num_threads(NUM_THREAD)
    for (i=0; i<n; i++) {
        #pragma omp parallel for num_threads(NUM_THREAD)
        for(j=0; j<m; j++) {
            /* starting point */
            if (!flag) {
                printf("Core numbers: %d\n", omp_get_thread_num());
                flag = true;
            }
            x= i *(width/(n-1)) + cx -width/2;
            y= j *(height/(m-1)) + cy -height/2;

            form(0,0,c);
            form(x,y,c0);

                /* complex iteration */
                
                for(k=0; k<max; k++) {
                    mult(c,c,d);
                    add(d,c0,c);
                    v=mag2(c);
                    if(v>4.0) break; /* assume not in set if mag > 4 */
                }

                /* assign gray level to point based on its magnitude */
                if(v>1.0) v=1.0; /* clamp if > 1 */
                image[i][j]=255*v;
        }
    }

    glutInit(&argc, argv);
    // glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
    glutInitWindowSize(N, M);
    glutCreateWindow("mandlebrot");
    myinit(NUM_THREAD);
    glutReshapeFunc(myReshape);
    double end = omp_get_wtime();
    // glutDisplayFunc(display);
    printf("Elapsed time: %.2f ms\n", 1000*(end-start));

    glutMainLoop();

    return 0;
}
