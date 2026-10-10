

from numbers import Real
from typing import Self


DEFAULT_COEFFICIENT = 0.0
ZERO_POLYNOMIAL_DEGREE = 0


class Polynomial:

    def __init__(self, *coefficients: Real) -> None:
        if not coefficients:
            coefficients = (DEFAULT_COEFFICIENT,)

        validated = tuple(
            self.__validate_coefficient(value) for value in coefficients
        )

        while len(validated) > 1 and validated[-1] == 0.0:
            validated = validated[:-1]

        self.__coefficients = validated

    @staticmethod
    def __validate_coefficient(value: Real) -> float:
        import math

        if isinstance(value, bool) or not isinstance(value, Real):
            raise TypeError("Polynomial coefficients must be real numbers.")

        coefficient = float(value)
        if not math.isfinite(coefficient):
            raise ValueError("Polynomial coefficients must be finite.")

        return coefficient

    @property
    def coefficients(self) -> tuple[float, ...]:
        return self.__coefficients

    @property
    def degree(self) -> int:
        if self.is_zero():
            return ZERO_POLYNOMIAL_DEGREE
        return len(self.__coefficients) - 1

    def is_zero(self) -> bool:
        return all(value == 0.0 for value in self.__coefficients)

    def __getitem__(self, power: int) -> float:
        if not isinstance(power, int) or isinstance(power, bool):
            raise TypeError("Power must be an integer.")
        if power < 0:
            raise IndexError("Power cannot be negative.")
        if power >= len(self.__coefficients):
            return DEFAULT_COEFFICIENT
        return self.__coefficients[power]

    def evaluate(self, x: Real) -> float:
        value = self.__validate_coefficient(x)
        result = DEFAULT_COEFFICIENT

        for coefficient in reversed(self.__coefficients):
            result = result * value + coefficient

        return result

    def __add__(self, other: object) -> Self:
        if not isinstance(other, Polynomial):
            return NotImplemented

        size = max(len(self.__coefficients), len(other.__coefficients))
        coefficients = [
            self[index] + other[index] for index in range(size)
        ]
        return type(self)(*coefficients)

    def __sub__(self, other: object) -> Self:
        if not isinstance(other, Polynomial):
            return NotImplemented

        size = max(len(self.__coefficients), len(other.__coefficients))
        coefficients = [
            self[index] - other[index] for index in range(size)
        ]
        return type(self)(*coefficients)

    def __mul__(self, other: object) -> Self:
        if isinstance(other, Real) and not isinstance(other, bool):
            scalar = self.__validate_coefficient(other)
            return type(self)(
                *(coefficient * scalar for coefficient in self.__coefficients)
            )

        if not isinstance(other, Polynomial):
            return NotImplemented

        result_size = (
            len(self.__coefficients) + len(other.__coefficients) - 1
        )
        result = [DEFAULT_COEFFICIENT] * result_size

        for left_power, left_value in enumerate(self.__coefficients):
            for right_power, right_value in enumerate(other.__coefficients):
                result[left_power + right_power] += left_value * right_value

        return type(self)(*result)

    def __rmul__(self, scalar: Real) -> Self:
        return self * scalar

    def __truediv__(self, other: object) -> Self:
        if isinstance(other, Real) and not isinstance(other, bool):
            divisor = self.__validate_coefficient(other)
            if divisor == 0.0:
                raise ZeroDivisionError("Cannot divide by zero.")
            return type(self)(
                *(coefficient / divisor for coefficient in self.__coefficients)
            )

        if not isinstance(other, Polynomial):
            return NotImplemented

        if other.is_zero():
            raise ZeroDivisionError("Cannot divide by the zero polynomial.")

        remainder = list(self.__coefficients)
        quotient_size = max(1, len(remainder) - len(other.__coefficients) + 1)
        quotient = [DEFAULT_COEFFICIENT] * quotient_size

        while len(remainder) >= len(other.__coefficients):
            while len(remainder) > 1 and remainder[-1] == 0.0:
                remainder.pop()

            if len(remainder) < len(other.__coefficients):
                break

            power = len(remainder) - len(other.__coefficients)
            factor = remainder[-1] / other.__coefficients[-1]
            quotient[power] = factor

            for index, coefficient in enumerate(other.__coefficients):
                remainder[power + index] -= factor * coefficient

        while len(remainder) > 1 and abs(remainder[-1]) < 1e-10:
            remainder.pop()

        if any(abs(value) >= 1e-10 for value in remainder):
            raise ValueError("Polynomial division has a nonzero remainder.")

        return type(self)(*quotient)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Polynomial):
            return NotImplemented
        return self.__coefficients == other.__coefficients

    def __neg__(self) -> Self:
        return type(self)(*(-value for value in self.__coefficients))

    def __str__(self) -> str:
        return f"[{', '.join(f'{value:g}' for value in self.__coefficients)}]"

    def __repr__(self) -> str:
        return f"Polynomial({', '.join(repr(value) for value in self.__coefficients)})"

    @classmethod
    def from_string(cls, text: str) -> Self:
        if not isinstance(text, str):
            raise TypeError("Input must be a string.")

        cleaned = text.strip()
        if cleaned.startswith("[") and cleaned.endswith("]"):
            cleaned = cleaned[1:-1].strip()

        if not cleaned:
            return cls(DEFAULT_COEFFICIENT)

        try:
            coefficients = [
                float(part.strip()) for part in cleaned.split(",")
            ]
        except ValueError as error:
            raise ValueError("Coefficients must be numeric.") from error

        return cls(*coefficients)


if __name__ == "__main__":
    polynomial1 = Polynomial(2, 3, 4)
    polynomial2 = Polynomial(1, 2)

    print("Polynomial 1:", polynomial1)
    print("Polynomial 2:", polynomial2)
    print("P1(2):", polynomial1.evaluate(2))
    print("Addition:", polynomial1 + polynomial2)
    print("Subtraction:", polynomial1 - polynomial2)
    print("Multiplication:", polynomial1 * polynomial2)
    print("Scalar multiplication:", polynomial1 * 2)
    print("Division:", Polynomial(2, 3, 1) / Polynomial(1, 1))
