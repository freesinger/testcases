#include<iostream>
#include<typeinfo>
#include<mpi.h>
using namespace std;

int main(int argc, char **argv)
{
    int id, nproc;
    int sum, start, end, acc;
    MPI_Status status;
    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &nproc);
    MPI_Comm_rank(MPI_COMM_WORLD, &id);

    sum = 0;
    start = 10000*id/nproc+1;
    end = 10000*(id+1)/nproc;

    /*
    for (int i = start; i <= end; i++)
        sum += i;
    cout<<"Node "<<id<<"'s partial sum is: "<<sum<<endl;
    //cout<<typeid(sum).name()<<endl; // i
    //cout<<sum<<endl; // output all proc's sum
    if (id != 0) {
        MPI_Send(&sum, 1, MPI_INT, 0, 1, MPI_COMM_WORLD);
    } else {
        for (int i = 1; i < nproc; i++) {
            MPI_Recv(&acc, 1, MPI_INT, i, 1, MPI_COMM_WORLD, &status);
            // this sum is 0's sum
            sum += acc;
            cout<<"Current sum is: "<<sum<<endl;
        }
    }
     */

    // MPI_Reduction version
    int allsum = 0;
    for (int i = start; i <= end; i++)
        sum += i;
    cout<<"Node "<<id<<"'s partial sum is: "<<sum<<endl;

    MPI_Reduce(&sum, &allsum, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

    // You must specify sum id
    if (id == 0)
        cout<<"Sum from 1~10000 is: "<<allsum<<endl;
    MPI_Finalize();
}