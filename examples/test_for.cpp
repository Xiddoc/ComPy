
#include <iostream>

auto range(int end);
void print(auto print_string);

auto range(int end) {
class range {
public:
	class iterator {
		friend class range;
	public:
		// Must-have for iterator
		long operator *() const { return index_; }

		// Called for each iteration
		const iterator &operator ++() {
			index_ += step_;
			return *this;
		}

		// Called for each iteration
		bool operator !=(const iterator &other) const {
			// If this returns *false*, the loop will quit
			// IF the index is smaller than the end index
			// AND the 'end' flag is not on
			// THEN return true, meaning that any
			// other case will return false (exit loop)
			return !end_now_ && index_ < other.index_;
		}

	protected:
		explicit iterator(long start, long step = 0, bool end_now = false) : index_(start), end_now_(end_now), step_(step) { }

	private:
		long index_;
		bool end_now_;
		long step_;
	};

	// Iterator methods
	iterator begin() const { return begin_; }
	iterator end() const { return end_; }

	// Constructor
	explicit range(long begin, long end, long step = 1) : begin_(begin, step, (begin - end) > 0 == step > 0), end_(end) {}
	explicit range(long end, long step = 1) : begin_(0, step, end < 0 == step > 0), end_(end) {}
private:
	iterator begin_;
	iterator end_;
};
return range(end);
}
void print(auto print_string) {
std::cout<<print_string<<std::endl;
}



int main() {
    /* Transpiled with ComPy */
    for (auto i : range(10)) {
print(i);
};
    return 0;
}
