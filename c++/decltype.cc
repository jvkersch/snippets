#include <iostream>
#include <vector>


using namespace std;

auto SimpleAuto(int x, int y)
{
    return x + y;
}

template<typename Container, typename Index>
decltype(auto) AutoContainerReference(Container&& c, Index i)
{
    return c[i];
}

template<typename T>
class TD;

int main()
{
    // Standard auto deduction of return type.
    cout << SimpleAuto(3, 4) << endl;

    // Templated function with universal reference. For lvalue arguments a
    // "standard" reference would have sufficed.
    vector<int> c{1, 2, 3};
    cout << AutoContainerReference(c, 1) << endl;

    // For rvalue arguments we need that universal reference.
    cout << AutoContainerReference(vector<int>{7, 8}, 1) << endl;

    // What is the return type of AutoContainerReference?
    auto& x = AutoContainerReference(vector<int>{7, 8}, 1);
    // need boost for this
    TD<decltype(AutoContainerReference(vector<int>{7, 8}, 1))> xType;

    
    return 0;
}
