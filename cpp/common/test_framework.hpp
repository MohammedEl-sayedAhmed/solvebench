// Minimal header-only test helper — the C++ counterpart of
// python/common/test_framework.py. Include with `-I cpp` so the path
// `common/test_framework.hpp` resolves from any solution's directory.
//
//   #include "common/test_framework.hpp"
//   int main() {
//       tf::TestRunner t;
//       t.check("Example 1", solution(args), expected);
//       return t.summary();   // non-zero exit if any check failed
//   }
#pragma once

#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <utility>

namespace tf {

// UTF-8 byte sequences for the symbols (portable regardless of source encoding).
inline const char* PASS  = "\xE2\x9C\x85";       // check mark
inline const char* FAIL  = "\xE2\x9D\x8C";       // cross mark
inline const char* PARTY = "\xF0\x9F\x8E\x89";   // party popper
inline const char* DASH  = "\xE2\x80\x94";       // em dash
inline const char* DOT   = "\xC2\xB7";           // middle dot

inline std::string rule(int n = 34) {
    std::string s;
    for (int i = 0; i < n; ++i) s += "\xE2\x94\x80";  // box-drawing horizontal
    return s;
}

// ---- pretty-printing helpers so failures show useful values ----------------
template <typename T>
std::string show(const T& v) {
    std::ostringstream os;
    os << std::boolalpha << v;
    return os.str();
}

template <typename T>
std::string show(const std::vector<T>& v) {
    std::ostringstream os;
    os << "[";
    for (std::size_t i = 0; i < v.size(); ++i) {
        if (i) os << ", ";
        os << show(v[i]);
    }
    os << "]";
    return os.str();
}

template <typename A, typename B>
std::string show(const std::pair<A, B>& p) {
    return "(" + show(p.first) + ", " + show(p.second) + ")";
}

// ---- the runner ------------------------------------------------------------
class TestRunner {
    int passed_ = 0;
    int total_ = 0;
    std::vector<std::string> failures_;

public:
    template <typename T>
    void check(const std::string& name, const T& got, const T& expected) {
        ++total_;
        if (got == expected) {
            ++passed_;
            std::cout << PASS << "  " << name << "\n";
        } else {
            failures_.push_back(name);
            std::cout << FAIL << "  " << name << "\n"
                      << "      expected: " << show(expected) << "\n"
                      << "      got:      " << show(got) << "\n";
        }
    }

    // Returns a process exit code: 0 when everything passed, 1 otherwise.
    int summary() const {
        std::cout << "\n" << rule() << "\n";
        if (failures_.empty()) {
            std::cout << PARTY << "  " << passed_ << "/" << total_
                      << " passed " << DASH << " all green\n";
            return 0;
        }
        std::cout << FAIL << "  " << passed_ << "/" << total_
                  << " passed " << DOT << " " << failures_.size() << " failed\n";
        return 1;
    }
};

}  // namespace tf
