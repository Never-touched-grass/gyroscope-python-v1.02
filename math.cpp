#include "pch.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
using namespace std;
vector<int> fib(int n) {
	vector<int> fibs = { 1, 1 };
	for (int i = 0; i < n; i++) {
		fibs.push_back(fibs[i] + fibs[i + 1]);
	}
	return fibs;
}
PYBIND11_MODULE(math_util, m) {
	m.doc() = "Miscallaneous math functions";
	m.def("fib", &fib, "A function that returns the first n Fibonacci numbers",
		pybind11::arg("n"));
}
