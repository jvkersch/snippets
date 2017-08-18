#include <algorithm>
#include <string>
#include <iostream>


template<typename C, typename T>
int count(const C& container, const T& element)
{
    int count = 0;

    auto begin = std::begin(container);
    auto end = std::end(container);
    
    while (begin != end) {
        begin = find(begin, end, element);
        if (begin != end) {
            count += 1;
            
            begin += 1;
        }
    }
    
    return count;
}


int main() 
{
    std::string s("Mary had a little lamb");
    std::cout << "a appears " << count(s, 'a') << " times." << std::endl;
    return 0;
}
