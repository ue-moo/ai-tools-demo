"""Advanced mathematical functions."""

from typing import List


def factorial(n: int) -> int:
    """Calculate factorial of n.

    Args:
        n: Non-negative integer.

    Returns:
        n! (n factorial)
    """
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number.

    Args:
        n: Position in Fibonacci sequence (0-indexed).

    Returns:
        The nth Fibonacci number.
    """
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def sqrt(x: float, tolerance: float = 1e-10) -> float:
    """Calculate square root using Newton's method.

    Args:
        x: Number to find square root of.
        tolerance: Convergence tolerance.

    Returns:
        Square root of x.
    """
    if x < 0:
        raise ValueError("Cannot calculate square root of negative number")
    if x == 0:
        return 0

    guess = x / 2
    while True:
        new_guess = (guess + x / guess) / 2
        if abs(new_guess - guess) < tolerance:
            return new_guess
        guess = new_guess


def is_prime(n: int) -> bool:
    """Check if a number is prime.

    Args:
        n: Integer to check.

    Returns:
        True if n is prime, False otherwise.
    """
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


def gcd(a: int, b: int) -> int:
    """Calculate greatest common divisor using Euclidean algorithm.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        Greatest common divisor of a and b.
    """
    while b:
        a, b = b, a % b
    return a


def mean(numbers: List[float]) -> float:
    """Calculate arithmetic mean.

    Args:
        numbers: List of numbers.

    Returns:
        Arithmetic mean.
    """
    return sum(numbers) / len(numbers)


def median(numbers: List[float]) -> float:
    """Calculate median.

    Args:
        numbers: List of numbers.

    Returns:
        Median value.
    """
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2
    return sorted_nums[mid]


def variance(numbers: List[float]) -> float:
    """Calculate population variance.

    Args:
        numbers: List of numbers.

    Returns:
        Population variance.
    """
    m = mean(numbers)
    return sum((x - m) ** 2 for x in numbers) / len(numbers)


def std_dev(numbers: List[float]) -> float:
    """Calculate population standard deviation.

    Args:
        numbers: List of numbers.

    Returns:
        Population standard deviation.
    """
    return sqrt(variance(numbers))


if __name__ == "__main__":
    print(f"5! = {factorial(5)}")
    print(f"fib(10) = {fibonacci(10)}")
    print(f"sqrt(16) = {sqrt(16)}")
    print(f"is_prime(17) = {is_prime(17)}")
    print(f"gcd(48, 18) = {gcd(48, 18)}")

    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"mean({data}) = {mean(data)}")
    print(f"median({data}) = {median(data)}")
    print(f"variance({data}) = {variance(data)}")
    print(f"std_dev({data}) = {std_dev(data)}")
