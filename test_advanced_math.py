"""Tests for advanced math functions."""

import pytest
from advanced_math import (
    factorial, fibonacci, sqrt, is_prime, gcd,
    mean, median, variance, std_dev
)


class TestFactorial:
    def test_zero(self):
        assert factorial(0) == 1

    def test_positive(self):
        assert factorial(5) == 120

    def test_one(self):
        assert factorial(1) == 1


class TestFibonacci:
    def test_zero(self):
        assert fibonacci(0) == 0

    def test_one(self):
        assert fibonacci(1) == 1

    def test_sequence(self):
        assert fibonacci(10) == 55


class TestSqrt:
    def test_perfect_square(self):
        assert abs(sqrt(16) - 4) < 1e-9

    def test_non_perfect_square(self):
        assert abs(sqrt(2) - 1.41421356) < 1e-6

    def test_zero(self):
        assert sqrt(0) == 0

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            sqrt(-1)


class TestIsPrime:
    def test_prime(self):
        assert is_prime(17) == True

    def test_not_prime(self):
        assert is_prime(15) == False

    def test_two(self):
        assert is_prime(2) == True

    def test_one(self):
        assert is_prime(1) == False


class TestGcd:
    def test_basic(self):
        assert gcd(48, 18) == 6

    def test_coprime(self):
        assert gcd(17, 13) == 1


class TestStatistics:
    def test_mean(self):
        assert mean([1, 2, 3, 4, 5]) == 3

    def test_median_odd(self):
        assert median([1, 2, 3, 4, 5]) == 3

    def test_median_even(self):
        assert median([1, 2, 3, 4]) == 2.5

    def test_variance(self):
        assert variance([1, 2, 3, 4, 5]) == 2.0

    def test_std_dev(self):
        assert abs(std_dev([1, 2, 3, 4, 5]) - 1.4142135) < 1e-5
