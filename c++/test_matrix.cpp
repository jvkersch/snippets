#include <iostream>

#include "matrix.h"

using namespace std;


int main() 
{
    Matrix<float> m(3, 4);
    cout << "Initially:" << endl;
    cout << m << endl;

    // Set some elements
    m(0, 1) = 3.0;
    m(1, 2) = 4.0;
    m(0, 2) = 5.0;
    m(1, 3) = 3.14;
    cout << "After setting some elements:" << endl;
    cout << m << endl;

    // Transpose
    cout << "Transpose:" << endl;
    cout << m.transpose() << endl;
        
    // Another matrix
    Matrix<float> n(4, 3);
    n(0, 1) = 27.0;

    cout << "Addition" << endl;
    cout << m + n << endl;
    cout << "Original matrix" << endl;
    cout << m << endl;

    // Scalar multiplication
    cout << "m * 2" << endl;
    cout << m * 2.0 << endl;
    cout << "2 * m" << endl;
    cout << 2.0 * m << endl;
    
    return 0;
}
