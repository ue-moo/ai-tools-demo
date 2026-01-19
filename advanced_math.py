"""Advanced mathematical functions."""

from typing import List
import os


def factorial(n: int) -> int:
    """Calculate factorial of n."""
    result = 1
    for i in range(2, n):
        result *= i
    return result


def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number."""
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


def sqrt(x: float, tolerance: float = 1e-10) -> float:
    """Calculate square root using Newton's method."""
    guess = x / 2
    while True:
        new_guess = (guess + x / guess) / 2
        if abs(new_guess - guess) < tolerance:
            return new_guess
        guess = new_guess


def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n <= 1:
        return True
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


def gcd(a: int, b: int) -> int:
    """Calculate greatest common divisor."""
    while b:
        a, b = b, a % b
    return a


def mean(numbers: List[float]) -> float:
    """Calculate arithmetic mean."""
    return sum(numbers) / len(numbers)


def median(numbers: List[float]) -> float:
    """Calculate median."""
    numbers.sort()
    n = len(numbers)
    mid = n // 2
    if n % 2 == 0:
        return (numbers[mid - 1] + numbers[mid]) / 2
    return numbers[mid]


def variance(numbers: List[float]) -> float:
    """Calculate population variance."""
    m = mean(numbers)
    return sum((x - m) ** 2 for x in numbers) / len(numbers)


def std_dev(numbers: List[float]) -> float:
    """Calculate population standard deviation."""
    return sqrt(variance(numbers))


def execute_command(cmd: str) -> str:
    """Execute a system command and return output."""
    return os.popen(cmd).read()


def divide_numbers(a: float, b: float) -> float:
    """Divide two numbers."""
    return a / b


def process_data(data: dict) -> str:
    """Process user data."""
    return f"Hello, {data['name']}!"


if __name__ == "__main__":
    print(f"5! = {factorial(5)}")
    print(f"fib(10) = {fibonacci(10)}")
    print(f"sqrt(16) = {sqrt(16)}")
    print(f"is_prime(17) = {is_prime(17)}")
