
"""Three-dimensional vector implementation."""

import math
from numbers import Real
from typing import Self


VECTOR_DIMENSION = 3
DEFAULT_COORDINATE_VALUE = 0.0
COMPARISON_PRECISION_TOLERANCE = 1e-9
ZERO_VECTOR_LENGTH = 0.0


class Vector3D:
    """Represent a vector in three-dimensional Euclidean space."""

    def __init__(
        self,
        x: Real = DEFAULT_COORDINATE_VALUE,
        y: Real = DEFAULT_COORDINATE_VALUE,
        z: Real = DEFAULT_COORDINATE_VALUE,
    ) -> None:
        """Initialize a vector with three finite numeric coordinates."""
        self.__x = self.__validate_coordinate(x)
        self.__y = self.__validate_coordinate(y)
        self.__z = self.__validate_coordinate(z)

    @staticmethod
    def __validate_coordinate(value: Real) -> float:
        """Validate and convert a coordinate to a finite float."""
        if isinstance(value, bool) or not isinstance(value, Real):
            raise TypeError("Coordinates must be real numbers.")

        coordinate = float(value)
        if not math.isfinite(coordinate):
            raise ValueError("Coordinates must be finite.")

        return coordinate

    @property
    def x(self) -> float:
        """Return the x-coordinate."""
        return self.__x

    @property
    def y(self) -> float:
        """Return the y-coordinate."""
        return self.__y

    @property
    def z(self) -> float:
        """Return the z-coordinate."""
        return self.__z

    @property
    def coordinates(self) -> tuple[float, float, float]:
        """Return all coordinates as a tuple."""
        return (self.__x, self.__y, self.__z)

    def length(self) -> float:
        """Return the Euclidean length of the vector."""
        return math.sqrt(
            self.__x**2 + self.__y**2 + self.__z**2
        )

    def dot(self, other: Self) -> float:
        """Return the dot product with another vector."""
        self.__check_vector(other)
        return sum(
            a * b for a, b in zip(self.coordinates, other.coordinates)
        )

    def cross(self, other: Self) -> Self:
        """Return the cross product with another vector."""
        self.__check_vector(other)

        x1, y1, z1 = self.coordinates
        x2, y2, z2 = other.coordinates

        return type(self)(
            y1 * z2 - z1 * y2,
            z1 * x2 - x1 * z2,
            x1 * y2 - y1 * x2,
        )

    def cosine_with(self, other: Self) -> float:
        """Return the cosine of the angle between two nonzero vectors."""
        self.__check_vector(other)

        denominator = self.length() * other.length()
        if denominator == ZERO_VECTOR_LENGTH:
            raise ValueError("Cosine is undefined for a zero vector.")

        return self.dot(other) / denominator

    @staticmethod
    def __check_vector(other: object) -> None:
        """Raise an error if the other operand is not a Vector3D."""
        if not isinstance(other, Vector3D):
            raise TypeError("Operand must be a Vector3D.")

    def __add__(self, other: object) -> Self:
        """Add two vectors component by component."""
        self.__check_vector(other)
        return type(self)(
            self.__x + other.x,
            self.__y + other.y,
            self.__z + other.z,
        )

    def __sub__(self, other: object) -> Self:
        """Subtract vectors component by component."""
        self.__check_vector(other)
        return type(self)(
            self.__x - other.x,
            self.__y - other.y,
            self.__z - other.z,
        )

    def __mul__(self, other: object) -> Self | float:
        """Multiply by a scalar or calculate a cross product."""
        if isinstance(other, Vector3D):
            return self.cross(other)

        if isinstance(other, bool) or not isinstance(other, Real):
            return NotImplemented

        scalar = self.__validate_coordinate(other)
        return type(self)(
            self.__x * scalar,
            self.__y * scalar,
            self.__z * scalar,
        )

    def __rmul__(self, scalar: Real) -> Self:
        """Support scalar multiplication from the left."""
        result = self.__mul__(scalar)
        if result is NotImplemented:
            return NotImplemented
        return result

    def __truediv__(self, scalar: Real) -> Self:
        """Divide every coordinate by a nonzero scalar."""
        if isinstance(scalar, bool) or not isinstance(scalar, Real):
            raise TypeError("Divisor must be a real number.")

        divisor = self.__validate_coordinate(scalar)
        if divisor == ZERO_VECTOR_LENGTH:
            raise ZeroDivisionError("Cannot divide a vector by zero.")

        return type(self)(
            self.__x / divisor,
            self.__y / divisor,
            self.__z / divisor,
        )

    def __neg__(self) -> Self:
        """Return the negated vector."""
        return type(self)(-self.__x, -self.__y, -self.__z)

    def __eq__(self, other: object) -> bool:
        """Compare coordinates with a small floating-point tolerance."""
        if not isinstance(other, Vector3D):
            return NotImplemented

        return all(
            math.isclose(
                a,
                b,
                rel_tol=COMPARISON_PRECISION_TOLERANCE,
                abs_tol=COMPARISON_PRECISION_TOLERANCE,
            )
            for a, b in zip(self.coordinates, other.coordinates)
        )

    def __lt__(self, other: object) -> bool:
        """Compare vectors by their lengths."""
        self.__check_vector(other)
        return self.length() < other.length()

    def __le__(self, other: object) -> bool:
        """Check whether this vector is no longer than another."""
        self.__check_vector(other)
        return self.length() <= other.length()

    def __gt__(self, other: object) -> bool:
        """Check whether this vector is longer than another."""
        self.__check_vector(other)
        return self.length() > other.length()

    def __ge__(self, other: object) -> bool:
        """Check whether this vector is at least as long as another."""
        self.__check_vector(other)
        return self.length() >= other.length()

    def __str__(self) -> str:
        """Return a readable coordinate representation."""
        return f"({self.__x:g}, {self.__y:g}, {self.__z:g})"

    def __repr__(self) -> str:
        """Return a representation suitable for debugging."""
        return (
            f"Vector3D({self.__x!r}, "
            f"{self.__y!r}, {self.__z!r})"
        )

    @classmethod
    def from_string(cls, text: str) -> Self:
        """Create a vector from text such as '(1, 2, 3)'."""
        if not isinstance(text, str):
            raise TypeError("Input must be a string.")

        cleaned = text.strip()
        if cleaned.startswith("(") and cleaned.endswith(")"):
            cleaned = cleaned[1:-1]

        parts = cleaned.split(",")
        if len(parts) != VECTOR_DIMENSION:
            raise ValueError("A vector must have exactly three coordinates.")

        try:
            coordinates = [float(part.strip()) for part in parts]
        except ValueError as error:
            raise ValueError("Coordinates must be numeric.") from error

        return cls(*coordinates)


if __name__ == "__main__":
    vector1 = Vector3D(3, 4, 0)
    vector2 = Vector3D(1, 2, 3)

    print("Vector 1:", vector1)
    print("Vector 2:", vector2)
    print("Length of vector 1:", vector1.length())
    print("Addition:", vector1 + vector2)
    print("Subtraction:", vector1 - vector2)
    print("Scalar multiplication:", vector1 * 2)
    print("Dot product:", vector1.dot(vector2))
    print("Cross product:", vector1.cross(vector2))