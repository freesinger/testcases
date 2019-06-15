#include<iostream>
#include<cstdio>
#include<mpi.h> 
using namespace std;

int fileSize(const char *filename) {
    FILE *p_file = NULL;
    p_file = fopen(filename, "rb");
    fseek(p_file, 0, SEEK_END);
    long int size = ftell(p_file);
    fclose(p_file);
    return size;
}

int main(int argc, char **argv) 
{ 
    
    int nproc, id, count; 
    int buf[100000];
    MPI_File fh;
    MPI_Status status;
    MPI_Offset offset;
    MPI_Datatype etype, filetype, contig;
    MPI_Aint lb, extend;

    MPI_Init(&argc, &argv); 
    MPI_Comm_size(MPI_COMM_WORLD, &nproc);
    MPI_Comm_rank(MPI_COMM_WORLD, &id);



    MPI_File_open(MPI_COMM_WORLD, "matrix",
                  MPI_MODE_CREATE | MPI_MODE_WRONLY,
                  MPI_INFO_NULL, &fh);
    
    long int filesize = fileSize("matrix");
    cout<<"Size: "<<filesize<<" from proc "<<id<<endl;
    
    int nints = filesize / (nproc * sizeof(int));
    offset = id * nints * sizeof(int);
    cout<<nints<<' '<<offset<<endl;

    for (int i = 0; i < 40; i++) {
        MPI_File_seek(fh, offset, MPI_SEEK_SET);
        MPI_File_read(fh, buf, nints, MPI_INT, &status);
        MPI_Get_count(&status, MPI_INT, &count);
        cout<<"process "<<id<<" read "<<count<<" ints"<<endl;
    }
    /* 
    if (id == 0) {
        MPI_File_write(fh, buf, 1000, MPI_INT, MPI_STATUSES_IGNORE);
    }
    */

    MPI_File_close(&fh);


    MPI_Finalize(); 
    return 0; 
} 