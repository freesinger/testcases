#include <iostream>
#include <Eigen/Dense>
using namespace Eigen;
using namespace std;
int main()
{
  MatrixXd m = MatrixXd::Random(4,3);
  m = (m + MatrixXd::Constant(4,3,1.2)) * 50;
  cout << "m =" << endl << m << endl;
  Vector3d v(1,2,3);
  //v << 1, 2, 3;
  cout << "m * v =" << endl << m * v << endl;
}
