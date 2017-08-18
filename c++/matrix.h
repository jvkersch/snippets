#ifndef MATRIX_H
#define MATRIX_H

#include <iomanip>
#include <iostream>

//namespace matrix {

class InvalidMatrixOperation {};

template<class T>
class Matrix;

template<class T>
std::ostream& operator<<(std::ostream&, const Matrix<T>&);

template <class T>
class Matrix {
public:
    Matrix(int rows, int cols);
    Matrix(const Matrix<T>&);
    ~Matrix();

    Matrix<T>& operator+=(const Matrix<T>& rhs);
    // Inline friend definition to avoid ADL issues
    friend Matrix<T> operator+(Matrix<T> m1, const Matrix<T>& m2) {
        m1 += m2;
        return m1;
    }
    Matrix<T>& operator*=(T);
    friend Matrix<T> operator*(Matrix<T> m, T val) 
    {
        m *= val;
        return m;
    }
    friend Matrix<T> operator*(T val, Matrix<T> m) 
    {
        m *= val;
        return m;
    }
    
    friend std::ostream& operator<< <T>(std::ostream&, const Matrix<T>&);
    
    // Direct Fortran style matrix(i,j) indexing
    const T& operator()(int i, int j) const;
    T& operator()(int i, int j);
    
    void clear();
    const Matrix& transpose();
    
private:
    int rows, cols;
    T* elements;
    bool row_major;
};

// template <class T>
// class Row 
// {
// public:

// };
    

template<class T>
Matrix<T>::Matrix(int rows, int cols) : rows(rows), cols(cols), row_major(true)
{
    elements = new T[rows*cols];
    clear();
}

template<class T>
Matrix<T>::Matrix(const Matrix<T>& m)
{
    rows = m.rows;
    cols = m.cols;
    elements = new T[rows*cols];
    for (int i = 0; i < rows*cols; i++)
        elements[i] = m.elements[i];
}

template<class T>
Matrix<T>::~Matrix()
{
    delete[] elements;
}

template<class T>
void Matrix<T>::clear()
{
    for(int i = 0; i < rows*cols; i++)
        elements[i] = 0;
}

template<class T>
Matrix<T>& Matrix<T>::operator+=(const Matrix<T>&m)
{
    if ((m.rows != rows) || (m.cols != cols)) {
        throw InvalidMatrixOperation();
    }

    for (int i = 0; i < rows*cols; i++)
        elements[i] += m.elements[i];

    return (*this);
}

template<class T>
Matrix<T>& Matrix<T>::operator*=(T val)
{
    for (int i = 0; i < rows*cols; i++)
        elements[i] *= val;

    return (*this);
}


template<class T>
const T& Matrix<T>::operator()(int i, int j) const
{
    if (row_major)
        return elements[i * cols + j];
    else
        return elements[j * rows + i];
}

template<class T>
T& Matrix<T>::operator()(int i, int j)
{
    if (row_major)
        return elements[i * cols + j];
    else
        return elements[j * rows + i];
}


template<class T>
const Matrix<T>& Matrix<T>::transpose()
{
    int tmp = rows;
    rows = cols;
    cols = tmp;
    row_major = !row_major;
    return *this;
}


template<class T>
std::ostream& operator<<(std::ostream& os, const Matrix<T>& m)
{
    for (int i = 0; i < m.rows; i++) {
        os << "[ ";
        for (int j = 0; j < m.cols; j++) {
            os << std::setw(7) << m(i,j);
        }
        os << " ]" << std::endl;
    }
    return os;
}
    
    
//}

#endif // MATRIX_H
