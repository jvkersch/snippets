#ifndef RANDOM_SELECTOR_H
#define RANDOM_SELECTOR_H

#include <iterator>
#include <random>

namespace util {
    
template <typename RandomGenerator = std::default_random_engine>
class RandomSelector
{
public:
    RandomSelector(
        RandomGenerator g = RandomGenerator(std::random_device()())) : gen(g) {}

        template <typename Iter>
        Iter select(Iter start, Iter end) {
            std::uniform_int_distribution<> dis(0, std::distance(start, end) - 1);
            std::advance(start, dis(gen));
            return start;
        }

        //convenience function
        template <typename Iter>
        Iter operator()(Iter start, Iter end) {
                return select(start, end);
        }
        
        template <typename Iter>
        int select_idx(Iter start, Iter end) {
            std::uniform_int_distribution<> dis(0, std::distance(start, end) - 1);
            return dis(gen);
        }

    private:
        RandomGenerator gen;
};
    
}


#endif // RANDOM_SELECTOR_H
