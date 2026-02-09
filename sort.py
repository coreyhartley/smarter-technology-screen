import argparse
import sys

from enum import auto, StrEnum
from typing import Final


class Package(StrEnum):
    STANDARD = auto()
    SPECIAL = auto()
    REJECTED = auto()


def _get_package(is_bulky: bool, is_heavy: bool) -> Package:
    """Determines package depending on bulky or heavy.
    
    Args:
        is_bulky: package is bulky.
        is_heavy: package is heavy.
    """
    if is_bulky and is_heavy:
        return Package.REJECTED
    if is_bulky or is_heavy:
        return Package.SPECIAL
    return Package.STANDARD


def sort(
    width: float, height: float, length: float, mass: float
) -> str:
    """Dispatches packages to the correct stack according to their volume and mass.
    
    Args:
        width: width of package, in cm.
        height: height of package, in cm.
        length: length  of package, in cm.
        mass: mas of package, in kg.

    Raises:
        ValueError: If any fields are not positive.
    """
    VOLUME_THRESHOLD_CM3: Final[float] = 1000000.0
    DIMENSION_THRESHOLD_CM: Final[float] = 150.0
    MASS_THRESHOLD_KG: Final[float] = 20.0

    is_bulky = False
    is_heavy = False
    dimensions = [width, height, length]

    if any(d <= 0 for d in dimensions):
        raise ValueError("All dimensions must be positive")
    if mass <= 0:
        raise ValueError("Mass must be positive")

    volume = length * width * height

    if any(d > DIMENSION_THRESHOLD_CM for d in dimensions):
        is_bulky = True
    if volume >= VOLUME_THRESHOLD_CM3:
        is_bulky = True

    if mass >= MASS_THRESHOLD_KG:
        is_heavy = True

    return _get_package(is_bulky, is_heavy).value.upper()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Package Sorter CLI")

    parser.add_argument("--length", type=float, required=True, help="Length in cm")
    parser.add_argument("--width", type=float, required=True, help="Width in cm")
    parser.add_argument("--height", type=float, required=True, help="Height in cm")
    parser.add_argument("--mass", type=float, required=True, help="Mass in kg")

    args = parser.parse_args()

    try:
        print(
            sort(args.length, args.width, args.height, args.mass)
        )
    except ValueError as err:
        print("Error: invalid input. ", err)
        sys.exit(1)
