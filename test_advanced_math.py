"""Tests for advanced math functions."""

import pytest
from advanced_math import fibonacci, sqrt, gcd, mean


class TestFibonacci:
    def test_zero(self):
        assert fibonacci(0) == 0

    def test_one(self):
        assert fibonacci(1) == 1

    def test_ten(self):
        assert fibonacci(10) == 55


class TestSqrt:
    def test_sixteen(self):
        assert abs(sqrt(16) - 4) < 1e-9


class TestGcd:
    def test_basic(self):
        assert gcd(48, 18) == 6


class TestMean:
    def test_basic(self):
        assert mean([1, 2, 3, 4, 5]) == 3.0
