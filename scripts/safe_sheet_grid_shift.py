#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

GRID_MM = 1.27
CANDIDATE_STEP_MM = 0.005

COORD_PATTERNS = [
    re.compile(r"(\(at\s+)(-?\d+(?:\.\d+)?)(\s+)(-?\d+(?:\.\d+)?)"),
    re.compile(r"(\(xy\s+)(-?\d+(?:\.\d+)?)(\s+)(-?\d+(?:\.\d+)?)"),
    re.compile(r"(\(start\s+)(-?\d+(?:\.\d+)?)(\s+)(-?\d+(?:\.\d+)?)"),
    re.compile(r"(\(end\s+)(-?\d+(?:\.\d+)?)(\s+)(-?\d+(?:\.\d+)?)"),
    re.compile(r"(\(center\s+)(-?\d+(?:\.\d+)?)(\s+)(-?\d+(?:\.\d+)?)"),
    re.compile(r"(\(mid\s+)(-?\d+(?:\.\d+)?)(\s+)(-?\d+(?:\.\d+)?)"),
]


def fmt_num(value: float) -> str:
    out = f"{value:.4f}".rstrip("0").rstrip(".")
    return out if out else "0"


def paren_delta_ignoring_quotes(line: str) -> int:
    in_quote = False
    escaped = False
    delta = 0
    for char in line:
        if escaped:
            escaped = False
            continue
        if char == "\\" and in_quote:
            escaped = True
            continue
        if char == '"':
            in_quote = not in_quote
            continue
        if not in_quote:
            if char == "(":
                delta += 1
            elif char == ")":
                delta -= 1
    return delta


def block_end(lines: list[str], start: int) -> int:
    depth = 0
    idx = start
    while idx < len(lines):
        depth += paren_delta_ignoring_quotes(lines[idx])
        if depth == 0:
            return idx
        idx += 1
    return len(lines) - 1


def find_lib_symbols_range(lines: list[str]) -> tuple[int | None, int | None]:
    for idx, line in enumerate(lines):
        if line.strip() == "(lib_symbols":
            return idx, block_end(lines, idx)
    return None, None


def extract_coords(text: str) -> tuple[list[float], list[float]]:
    xs: list[float] = []
    ys: list[float] = []
    for pattern in COORD_PATTERNS:
        for match in pattern.finditer(text):
            xs.append(float(match.group(2)))
            ys.append(float(match.group(4)))
    return xs, ys


def dist_to_grid(value: float, step: float) -> float:
    scaled = value / step
    return abs(scaled - round(scaled)) * step


def avg_grid_error(values: list[float], delta: float, step: float) -> float:
    if not values:
        return 0.0
    return sum(dist_to_grid(value + delta, step) for value in values) / len(values)


def best_delta(
    values: list[float], step: float, candidate_step: float
) -> tuple[float, float, float]:
    lower = -step / 2
    upper = step / 2
    count = int((upper - lower) / candidate_step) + 1
    candidates = [lower + idx * candidate_step for idx in range(count)]
    before = avg_grid_error(values, 0.0, step)
    best = min(candidates, key=lambda delta: avg_grid_error(values, delta, step))
    after = avg_grid_error(values, best, step)
    return best, before, after


def shift_text(text: str, dx: float, dy: float) -> str:
    shifted = text

    def repl(match: re.Match[str]) -> str:
        x = float(match.group(2)) + dx
        y = float(match.group(4)) + dy
        return f"{match.group(1)}{fmt_num(x)}{match.group(3)}{fmt_num(y)}"

    for pattern in COORD_PATTERNS:
        shifted = pattern.sub(repl, shifted)
    return shifted


def process_file(
    path: Path, threshold: float, min_improvement: float, apply: bool
) -> tuple[bool, str]:
    original = path.read_text(encoding="utf-8")
    lines = original.splitlines()

    lib_start, lib_end = find_lib_symbols_range(lines)
    if lib_start is None or lib_end is None:
        schematic_text = "\n".join(lines)
        prefix = ""
    else:
        prefix = "\n".join(lines[: lib_end + 1])
        schematic_text = "\n".join(lines[lib_end + 1 :])

    xs, ys = extract_coords(schematic_text)
    if not xs:
        return False, f"{path.name}: skipped (no coordinates found)"

    dx, bx, ax = best_delta(xs, GRID_MM, CANDIDATE_STEP_MM)
    dy, by, ay = best_delta(ys, GRID_MM, CANDIDATE_STEP_MM)

    improvement_x = bx - ax
    improvement_y = by - ay
    significant = (ax <= threshold and ay <= threshold) and (
        improvement_x >= min_improvement or improvement_y >= min_improvement
    )

    if not significant:
        return False, (
            f"{path.name}: skipped (dx={dx:+.3f}, dy={dy:+.3f}, "
            f"x {bx:.3f}->{ax:.3f}, y {by:.3f}->{ay:.3f})"
        )

    updated_schematic = shift_text(schematic_text, dx, dy)
    if prefix:
        updated = prefix + "\n" + updated_schematic
    else:
        updated = updated_schematic
    if original.endswith("\n"):
        updated += "\n"

    if updated == original:
        return False, f"{path.name}: unchanged"

    if apply:
        path.write_text(updated, encoding="utf-8")

    return True, (
        f"{path.name}: shifted dx={dx:+.3f}, dy={dy:+.3f} "
        f"(x {bx:.3f}->{ax:.3f}, y {by:.3f}->{ay:.3f})"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Safely align KiCad schematics to 50-mil grid via whole-sheet translation."
    )
    parser.add_argument(
        "--kicad-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "hardware" / "kicad",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.08,
        help="Max average off-grid error after shift (mm)",
    )
    parser.add_argument(
        "--min-improvement",
        type=float,
        default=0.02,
        help="Minimum required improvement in avg error (mm)",
    )
    parser.add_argument("--apply", action="store_true", help="Write changes")
    args = parser.parse_args()

    files = sorted(args.kicad_dir.glob("*.kicad_sch"))
    changed = 0

    for file_path in files:
        did_change, message = process_file(
            file_path,
            threshold=args.threshold,
            min_improvement=args.min_improvement,
            apply=args.apply,
        )
        print(message)
        if did_change:
            changed += 1

    print(f"\nFiles changed: {changed} / {len(files)}")


if __name__ == "__main__":
    main()
