#include<iostream>
#include<cstdio>
#include<ctime>
#include<cstdlib>
#include<string>
#include<mpi.h> 
using namespace std;

/* Calculate file size */
static int fileSize(const char *filename) {
    FILE *p_file = NULL;

    p_file = fopen(filename, "rb");
    fseek(p_file, 0, SEEK_END);
    long int size = ftell(p_file);
    fclose(p_file);

    return size;
}


/* Write data to destination file */
static char* fileWrite(const char *filename, char *dst, const long int size) {
    char read;
    FILE *p_file = NULL;

    p_file = fopen(filename, "r");
    cout<<"Writing files..."<<endl;
    for (int i = 0; i < size; i++) {
        if ((read=fgetc(p_file)) != EOF)
            dst[i] = read;
        else
            cout<<"EOF!"<<endl;
    }
    dst[size] = '\0';

    return dst;
}


/* Validate result arrays */
static bool resultValidate(const char* X, const char* Y, const long int size) {
    cout<<"Validating results..."<<endl;
    for (int i = 0; i < size; i++)
        if (int(X[i]) != int(Y[i]))
            return false;
    return true;
}


int main(int argc, char **argv) 
{ 
    int nproc, id, bufsize, blocksize; 
    char *block, *A, *B;
    string P;
    MPI_File fh;
    MPI_Status status;
    MPI_Offset offset;
    // MPI_Datatype etype, filetype, contig;
    // MPI_Aint lb, extend;
    MPI_Comm comm = MPI_COMM_WORLD;
    MPI_Init(&argc, &argv); 
    MPI_Comm_size(comm, &nproc);
    MPI_Comm_rank(comm, &id);

    /* Arguments
        argv[1]: Size of array user want to create
        argv[2]: '-p' enable print function for debugging 
     */
    if (argc > 2) {
        bufsize = atoi(argv[1]);
        P = argv[2];
    } else if (argc > 1) {
        bufsize = atoi(argv[1]);
    } else if (id == 0) {
        cout<<"Enter array size!"<<endl;
        exit(-1);
    }

    /* Allocate buffer to procceses */
    if (id != nproc-1)
        blocksize = bufsize/nproc;
    else
        blocksize = bufsize-(nproc-1)*(bufsize/nproc);
    block = (char*)malloc((blocksize+1)*sizeof(char));

    /* Fill blocks with random integers */
    srand(time(NULL));
    for (int i = 0; i < blocksize; i++) {
        block[i] = (rand() % 10) + 1;
    }
	block[blocksize] = '\0';

    if (P == "-p") {
        cout<<"Process "<<id<<": ";
        for (int i = 0; i < blocksize; i++)
            cout<<int(block[i])<<' ';
        cout<<'\n';
	}
	
    /* make sure all writes finish before we seek/read */
    MPI_Barrier(comm);
    MPI_File_open(comm, "mpiio.dat",
                  MPI_MODE_CREATE | MPI_MODE_WRONLY,
                  MPI_INFO_NULL, &fh);
    
    offset = id*(bufsize/nproc);
	cout<<"Offset of process "<<id<<" : "<<offset<<endl;
    
    /* write to file due to process's offset */
    MPI_File_write_at(fh, offset, block, blocksize, MPI_CHAR, &status);
    // MPI_File_close(&fh);

    /* 0 process store data sent from slave processes in array A */
    MPI_Barrier(comm);
    if (id == 0) {
        A = (char*)malloc((bufsize+1)*sizeof(char));
        B = (char*)malloc((bufsize+1)*sizeof(char));

        /* copy 0's data to A */
        memcpy(A, block, blocksize);
        /*
        // prin only 0's data
        cout<<"A1: "<<endl;
        for (int i = 0; i < bufsize; i++)
            cout<<int(A[i])<<' ';
        cout<<'\n';
         */

        /* Recieve data from slaves' process and store in A */
        for (int i = 1; i < nproc; i++)
			if (i != nproc-1) {
                // must specify offset in A to store different processes' data
            	MPI_Recv(&A[i*(bufsize/nproc)], bufsize/nproc, 
                         MPI_CHAR, i, 0, comm, &status);
                cout<<"Process "<<id<<" is recieving data from "<<i<<"..."<<endl;
            } else {
				MPI_Recv(&A[(nproc-1)*(bufsize/nproc)], bufsize-(bufsize/nproc)*(nproc-1),
						 MPI_CHAR, i, 0, comm, &status);
                cout<<"Process "<<id<<" is recieving data from "<<i<<"..."<<endl;
            }

        cout<<"Process "<<id<<" revieced Done!"<<endl;
		free(block);
    } else {
        cout<<"Process "<<id<<" sending..."<<endl;
        MPI_Send(block, blocksize, MPI_CHAR, 0, 0, comm);
		free(block);
    }
    MPI_Barrier(comm);


    if (id == 0) {
        /* 0 process sequential read slave processes' I/O data into arrat B */
        B = fileWrite("mpiio.dat", B, bufsize);

        if (P == "-p") {
            cout<<"A: "<<endl;
            for (int i = 0; i < bufsize; i++)
                cout<<int(A[i])<<' ';
            cout<<'\n';

            cout<<"B: "<<endl;
            for (int i = 0; i < bufsize; i++)
                cout<<int(B[i])<<' ';
            cout<<'\n';
        }

        /* Validation */
        if (resultValidate(A, B, bufsize))
            cout<<"PASS"<<endl;
        else cout<<"FAIL"<<endl;

        free(A);
        free(B);   
    }
    
    /* 
    long int filesize = fileSize("mpiio.dat");
    cout<<"Size: "<<filesize<<" from proc "<<id<<endl;
    
    int nints = filesize / (nproc * sizeof(int));
    offset = id * nints * sizeof(int);
    cout<<nints<<' '<<offset<<endl;

    int count;
    for (int i = 0; i < 40; i++) {
        MPI_File_seek(fh, offset, MPI_SEEK_SET);
        MPI_File_read(fh, buf, nints, MPI_INT, &status);
        MPI_Get_count(&status, MPI_INT, &count);
        cout<<"process "<<id<<" read "<<count<<" ints"<<endl;
    }
    
    if (id == 0) {
        MPI_File_write(fh, buf, 1000, MPI_INT, MPI_STATUSES_IGNORE);
    }

    MPI_File_close(&fh);
    */
   
    MPI_File_close(&fh);
    MPI_Finalize(); 
    return 0; 
} 