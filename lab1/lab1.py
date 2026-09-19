
"""
color_cube_solver.py

A working 3x3 solver that takes raw colors from the cube and uses the
kociemba two phase algorithm to return a solution.

Requirements:
    pip install kociemba

Input format:
    You provide 54 stickers in this fixed face order:
        U face, then R, then F, then D, then L, then B
    Each face is scanned row by row, left to right, top to bottom.

    Example order:
        U1 U2 U3 U4 U5 U6 U7 U8 U9
        R1 R2 R3 R4 R5 R6 R7 R8 R9
        F1 F2 F3 F4 F5 F6 F7 F8 F9
        D1 D2 D3 D4 D5 D6 D7 D8 D9
        L1 L2 L3 L4 L5 L6 L7 L8 L9
        B1 B2 B3 B4 B5 B6 B7 B8 B9

    Colors can be letters like:
        W, Y, R, O, G, B

    The script figures out which color is the center of each face and
    maps that to Singmaster faces U, R, F, D, L, B as required by kociemba.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict

import kociemba  # type: ignore


FACE_ORDER = ["CubesFace", "CubesRightSide", "CubesBackSide", "CubesLeftSide", "CubesUpperSide", "CubesLowerSide"]


@dataclass
class ColorCube:
    """
    Simple color based representation.

    faces: dict mapping face label (U, R, F, D, L, B)
           to list of 9 stickers (each a color char).
    """

    faces: Dict[str, List[str]]

    @staticmethod
    def from_color_list(colors: List[str]) -> "ColorCube":
        """
        Build from a flat list of 54 colors in the fixed face order:
        U then R then F then D then L then B.
        """
        if len(colors) != 54:
            raise ValueError(f"Expected 54 colors, got {len(colors)}")

        faces: Dict[str, List[str]] = {}
        idx = 0
        for face in FACE_ORDER:
            faces[face] = colors[idx:idx + 9]
            idx += 9
        return ColorCube(faces)

    def center_colors(self) -> Dict[str, str]:
        """
        Return a mapping from face label to its center color.
        Center indices are 4 for each 3x3 face.
        """
        return {face: stickers[4] for face, stickers in self.faces.items()}

    def color_counts(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for stickers in self.faces.values():
            for c in stickers:
                counts[c] = counts.get(c, 0) + 1
        return counts


def build_facelet_string_from_colors(cube: ColorCube) -> str:
    """
    Convert a ColorCube into the facelet string that kociemba expects.

    kociemba format:
        A 54 character string where each character is one of
        U R F D L B

    Each character indicates which face that sticker belongs to in the
    solved state. The mapping is determined by the center colors.

    Steps:
        1. Identify the color on the centers of each face
        2. Build a mapping: color -> face letter (U, R, F, D, L, B)
        3. For each sticker, look up its color to get the face letter
        4. Output in the same face order U, R, F, D, L, B
    """

    centers = cube.center_colors()
    # centers might be for example:
    #   U: 'W', R: 'R', F: 'G', D: 'Y', L: 'O', B: 'B'

    # Build color_to_face mapping, for example:
    #   'W' -> 'U', 'R' -> 'R', etc
    color_to_face: Dict[str, str] = {}
    for face, col in centers.items():
        if col in color_to_face:
            raise ValueError(
                f"Center color {col} appears on more than one face, "
                "color scheme is invalid."
            )
        color_to_face[col] = face

    # Validate there are exactly six colors and each appears nine times
    counts = cube.color_counts()
    if len(counts) != 6:
        raise ValueError(
            f"Expected exactly 6 distinct colors, got {len(counts)}: {counts}"
        )
    for col, cnt in counts.items():
        if cnt != 9:
            raise ValueError(
                f"Color {col!r} must appear exactly 9 times, but appears {cnt} times."
            )

    # Now build the facelet string
    facelets_list: List[str] = []
    for face in FACE_ORDER:
        stickers = cube.faces[face]
        for c in stickers:
            if c not in color_to_face:
                raise ValueError(
                    f"Sticker color {c!r} not found among center colors {color_to_face}"
                )
            facelets_list.append(color_to_face[c])

    facelets = "".join(facelets_list)
    if len(facelets) != 54:
        raise ValueError(f"Internal error, facelet string has length {len(facelets)}")
    return facelets


def solve_cube_from_colors(colors: List[str]) -> str:
    """
    Given a flat list of 54 colors in face order U, R, F, D, L, B,
    return a solution string using the kociemba solver.

    This will raise ValueError if the color layout is invalid.
    """
    cube = ColorCube.from_color_list(colors)
    facelets = build_facelet_string_from_colors(cube)
    # kociemba.solve returns a string like "R U R' U' F2 ..."
    solution = kociemba.solve(facelets)
    return solution


def _read_colors_from_user() -> List[str]:
    """
    Helper for command line usage.
    Prompts the user for each face in order and reads 9 stickers per face.
    Returns a flat list of 54 color chars.
    """
    print("Enter colors for each face in order U, R, F, D, L, B.")
    print("Each face is 9 stickers, row by row, left to right.")
    print("Use single letters like W, Y, R, O, G, B.")
    print()

    colors: List[str] = []
    for face in FACE_ORDER:
        while True:
            s = input(
                f"Enter 9 colors for face {face} (no spaces, for example: WWRWWRWWW): "
            ).strip().upper()
            if len(s) != 9:
                print("You must enter exactly 9 characters, try again.")
                continue
            if not all(ch.isalpha() for ch in s):
                print("All characters must be letters, try again.")
                continue
            colors.extend(list(s))
            break

    return colors


def main():
    print("Rubiks Cube Color Based Solver using kociemba")
    print("You will enter the cube colors, and this will output a solution.")
    print()

    colors = _read_colors_from_user()
    try:
        solution = solve_cube_from_colors(colors)
        print("\nSolution:")
        print(solution)
    except Exception as e:
        print("\nError while solving cube:")
        print(e)


if __name__ == "__main__":
    main()

