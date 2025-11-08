"""
Computation of Standard Poincaré Plot Descriptors and Heart Rate Asymmetry Measures
==================================================================================

This code computes the nonlinear measures (standard Poincaré plot descriptors and
Heart Rate Asymmetry Measures) for the purposes of the study:

    “Mapping the Heart Rhythm: Leveraging Poincaré Plot Asymmetry to Detect
    Congestive Heart Failure and Age-related Changes”
    by Mijat Paunović, Marko Ćosić, Nikola N. Radovanović,
    Mirjana M. Platiša, and Nadica Miljković

==================================================================================
==================================================================================
User Instructions

To reproduce the results presented in the above study, configure the following
parameters in the **USER CONFIGURATION** block:

    Set choice value to perform statistical analysis for appropriate subject groups:
     - '1' for oHS vs. CHF
     - '2' for yHS vs. oHS

Optionally, the user may modify parameters in the **OPTIONAL SETTINGS** block
to experiment with different analysis configurations.

==================================================================================
Input: Path to the directory HRV data.

Output: CSV files containing computed nonlinear measures.

==================================================================================
For inquiries or bug reports, please contact:

    • M. Paunović — paunovicjata@gmail.com
    • N. Miljković — nadica.miljkovic@etf.bg.ac.rs
"""

from __future__ import annotations
from pathlib import Path
import os
import re
import csv
import numpy as np
import scipy.io
from scipy.stats import gaussian_kde
from tqdm import tqdm  # progress bars

from pathlib import Path

# --- Project root and data layout --------------------------------------------
# Root directory is the directory where this script is located
ROOT_DIR = Path(__file__).resolve().parent

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                          USER CONFIGURATION                                ║
# ╚════════════════════════════════════════════════════════════════════════════╝

# set '1' for oHS vs. CHF
# set '2' for yHS vs. oHS
choice = 2 

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                             OPTIONAL                                       ║
# ╚════════════════════════════════════════════════════════════════════════════╝

# Analysis parameters ----------------------------------------------------------
GRID_SIZE     = 1000                # for KDE AMI
NUM_BINS_LIST = [25, 50, 100, 150, 200, 300, 500, 1000]  # for HB AMI
LOWER_BOUND   = 300                 # ms (RR lower limit)
UPPER_BOUND   = 2000                # ms (RR upper limit)

if choice == 1:
    # Cohort abbreviations ensure descriptive output file naming
    g1 = 'oHS'
    g2 = 'CHF'
    
    # Inclusion CSVs (first column must contain numeric subject IDs, header allowed)
    g1_IDS_PATH = ROOT_DIR / "input_data/IDs/IDs-oHS.csv"
    g2_IDS_PATH = ROOT_DIR / "input_data/IDs/IDs-CHF.csv"

    # Base folders containing per-timescale subfolders with .mat files
    g1_BASE_DIR = ROOT_DIR / "input_data/HRV/HS"
    g2_BASE_DIR = ROOT_DIR / "input_data/HRV/CHF"

elif choice == 2:
        # Cohort abbreviations ensure descriptive output file naming
    g1 = 'yHS'
    g2 = 'oHS'

    # Inclusion CSVs (first column must contain numeric subject IDs, header allowed)
    g1_IDS_PATH = ROOT_DIR / "input_data/IDs/IDs-yHS.csv"
    g2_IDS_PATH = ROOT_DIR / "input_data/IDs/IDs-oHS.csv"

    # Base folders containing per-timescale subfolders with .mat files
    g1_BASE_DIR = ROOT_DIR / "input_data/HRV/HS"
    g2_BASE_DIR = ROOT_DIR / "input_data/HRV/HS"

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                     END OF USER CONFIGURATION (DO NOT EDIT)                ║
# ╚════════════════════════════════════════════════════════════════════════════╝

EXPORT_DIR = ROOT_DIR / "results" / "nonlinear_measures" / f"{g1}_vs_{g2}"

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                      Nonlinear Measure Definitions                         ║
# ╚════════════════════════════════════════════════════════════════════════════╝

def SD1(rr_intervals: np.ndarray) -> float:
    diffs = np.diff(rr_intervals)
    sdsd = np.sqrt(np.var(diffs, ddof=1))
    return float(sdsd / np.sqrt(2.0))

def SD2(rr_intervals: np.ndarray) -> float:
    sdrr = np.std(rr_intervals, ddof=1)
    sdsd = np.std(np.diff(rr_intervals), ddof=1)
    return float(np.sqrt(2 * sdrr**2 - 0.5 * sdsd**2))

def porta_index(M: np.ndarray) -> float:
    rrn, rrn1 = M[:, 0], M[:, 1]
    above = np.sum(rrn1 > rrn)
    below = np.sum(rrn1 < rrn)
    denom = above + below
    if denom == 0:
        return 0.0
    p = above / denom
    return float(2 * abs(p - 0.5))

def guzik_index(M: np.ndarray) -> float:
    rrn, rrn1 = M[:, 0], M[:, 1]
    perp = np.abs(rrn - rrn1) / np.sqrt(2.0)
    sq = perp**2
    sa = np.sum(sq[rrn1 > rrn])
    sb = np.sum(sq[rrn1 < rrn])
    denom = sa + sb
    if denom == 0:
        return 0.0
    g = sa / denom
    return float(2 * abs(g - 0.5))

def asymmetric_spread_index(M: np.ndarray) -> float:
    rrn, rrn1 = M[:, 0], M[:, 1]
    slopes = np.abs(np.arctan2(rrn1, rrn) - np.pi / 4.0)
    dist = np.sqrt(rrn**2 + rrn1**2)
    arc = slopes * dist
    valid = rrn1 != rrn
    if not np.any(valid) or np.sum(rrn1 > rrn) == 0:
        return 0.0
    sd_above = np.std(arc[rrn1 > rrn], ddof=1)
    sd_total = np.std(arc[valid], ddof=1)
    if sd_total == 0:
        return 0.0
    return float(sd_above / (2.0 * sd_total))

def scaled_frobenius_norm(rr_intervals: np.ndarray, num_bins: int) -> float:
    prev, curr = rr_intervals[:-1], rr_intervals[1:]
    xedges = np.linspace(LOWER_BOUND, UPPER_BOUND, num_bins + 1)
    yedges = np.linspace(LOWER_BOUND, UPPER_BOUND, num_bins + 1)
    counts, _, _ = np.histogram2d(prev, curr, bins=[xedges, yedges])
    diff = counts - counts.T
    max_abs = np.max(np.abs(diff))
    if max_abs == 0:
        return 0.0
    scaled = diff / max_abs
    theory = np.triu(np.ones((num_bins, num_bins)), 1) - np.tril(np.ones((num_bins, num_bins)), -1)
    norm_theory = theory / np.max(np.abs(theory))
    frob_max = np.linalg.norm(norm_theory, "fro")
    frob = np.linalg.norm(scaled, "fro")
    return float(frob / frob_max)

def area_index(M: np.ndarray) -> float:
    rrn, rrn1 = M[:, 0], M[:, 1]
    angles = np.abs(np.arctan2(rrn1, rrn) - np.pi / 4.0)
    dist = np.sqrt(rrn**2 + rrn1**2)
    sector = 0.5 * dist**2 * angles
    total_area = np.sum(sector)
    if total_area == 0:
        return 0.0
    area = np.sum(sector[rrn1 > rrn])
    ai = area / total_area
    return float(2 * abs(ai - 0.5))

def slope_index(M: np.ndarray) -> float:
    rrn, rrn1 = M[:, 0], M[:, 1]
    slopes = np.abs(np.arctan2(rrn1, rrn) - np.pi / 4.0)
    s_total = np.sum(slopes)
    if s_total == 0:
        return 0.0
    s_above = np.sum(slopes[rrn1 > rrn])
    val = s_above / s_total
    return float(2 * abs(val - 0.5))

def ami_kde(rr_intervals: np.ndarray, grid_size: int) -> float:
    if rr_intervals.size < 3:
        return 0.0
    pairs = np.column_stack((rr_intervals[1:], rr_intervals[:-1]))
    kde = gaussian_kde(pairs.T)
    x = np.linspace(LOWER_BOUND, UPPER_BOUND, grid_size)
    y = np.linspace(LOWER_BOUND, UPPER_BOUND, grid_size)
    X, Y = np.meshgrid(x, y, indexing="xy")
    coords = np.vstack([X.ravel(), Y.ravel()])
    density = kde(coords).reshape(grid_size, grid_size)
    diff = density - density.T
    max_abs = np.max(np.abs(diff))
    if max_abs == 0:
        return 0.0
    scaled_diff = diff / max_abs
    theory = np.triu(np.ones((grid_size, grid_size)), 1) - np.tril(np.ones((grid_size, grid_size)), -1)
    norm_theory = theory / np.max(np.abs(theory))
    frob_max = np.linalg.norm(norm_theory, "fro")
    frob = np.linalg.norm(scaled_diff, "fro")
    return float(frob / frob_max)

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                             Utility Function                               ║
# ╚════════════════════════════════════════════════════════════════════════════╝

# Toggle tqdm progress bars
USE_TQDM = True

def _list_mat_files(directory: Path) -> list[Path]:
    """Return sorted list of .mat files in directory."""
    return sorted(p for p in directory.glob("*.mat"))

def _load_rr(file_path: Path) -> np.ndarray:
    """Load RR intervals from a .mat file assuming variable 'data'."""
    mat = scipy.io.loadmat(file_path)
    rr = np.asarray(mat["rr_intervals"]).squeeze()
    return rr

def _filter_rr(rr: np.ndarray) -> np.ndarray:
    """Keep RR values within [LOWER_BOUND, UPPER_BOUND] ms."""
    return rr[(rr >= LOWER_BOUND) & (rr <= UPPER_BOUND)]

def _write_csv(rows: np.ndarray, header: list[str], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)

def _load_ids(csv_path: Path) -> set[int]:
    """Load IDs from first column of a CSV (skips header if present)."""
    ids: set[int] = set()
    with csv_path.open("r", newline="") as f:
        reader = csv.reader(f)
        first = next(reader, None)
        if first is not None:
            try:
                ids.add(int(first[0]))
            except (TypeError, ValueError):
                pass  # header
        for row in reader:
            if not row:
                continue
            try:
                ids.add(int(row[0]))
            except (TypeError, ValueError):
                continue
    return ids

_ID_LEADING_NUM = re.compile(r"^(\d+)")

def _file_id_from_stem(stem: str) -> int | None:
    m = _ID_LEADING_NUM.match(stem)
    return int(m.group(1)) if m else None

# --------------------------------- Helpers ------------------------------------

def _iter_timescale_dirs(base: Path) -> list[Path]:
    """Return sorted subdirectories under `base` that look like timescale folders."""
    subs = [p for p in base.iterdir() if p.is_dir()]
    def _extract_minutes(name: str) -> int:
        digits = "".join(ch for ch in name if ch.isdigit())
        return int(digits) if digits else 0
    return sorted(subs, key=lambda p: _extract_minutes(p.name))

# Compute and export nonlinear measures for a specific group
def _compute_and_export_for_group(
    group_prefix: str,
    base_dir: Path,
    id_set: set[int],
    export_base: Path,
) -> None:
    """Compute indices for one group and write CSVs per timescale & num_bins."""
    for subfolder in _iter_timescale_dirs(base_dir):
        minutes_digits = "".join(ch for ch in subfolder.name if ch.isdigit())
        if not minutes_digits:
            continue
        timescale = int(minutes_digits)

        # Per-timescale output directory
        out_dir = export_base / f"{timescale}min"
        out_dir.mkdir(parents=True, exist_ok=True)

        # Filter files by inclusion IDs
        eligible_files: list[Path] = []
        for f in _list_mat_files(subfolder):
            fid = _file_id_from_stem(f.stem)
            if fid is not None and fid in id_set:
                eligible_files.append(f)

        if not eligible_files:
            continue

        # Precompute KDE AMI per file (once)
        ami_vals: list[float] = []
        iterable = eligible_files
        if USE_TQDM:
            iterable = tqdm(eligible_files, desc=f"KDE AMI {group_prefix} {timescale}min", unit="file")
        for f in iterable:
            rr = _filter_rr(_load_rr(f))
            ami_vals.append(ami_kde(rr, GRID_SIZE))

        # Compute other indices for each histogram resolution
        for num_bins in NUM_BINS_LIST:
            rows = []
            iterable2 = enumerate(eligible_files)
            if USE_TQDM:
                iterable2 = tqdm(
                    enumerate(eligible_files),
                    total=len(eligible_files),
                    desc=f"Indices {group_prefix} {timescale}min_{num_bins}bins",
                    unit="file",
                )
            for idx, f in iterable2:
                rr = _filter_rr(_load_rr(f))
                if rr.size < 3:
                    rows.append([0.0] * 9)
                    continue
                M = np.column_stack((rr[:-1], rr[1:]))

                rows.append([
                    SD1(rr),
                    SD2(rr),
                    guzik_index(M),
                    porta_index(M),
                    asymmetric_spread_index(M),
                    scaled_frobenius_norm(rr, num_bins),
                    slope_index(M),
                    area_index(M),
                    ami_vals[idx],  # KDE AMI (precomputed)
                ])

            arr = np.asarray(rows, dtype=float)

            # Convert selected indices to percent: GI(2), PI(3), HB AMI(5), SI(6), AI(7), KDE AMI(8)
            for c in (2, 3, 5, 6, 7, 8):
                arr[:, c] *= 100.0

            header = [
                "SD1",
                "SD2",
                "Guzik Index",
                "Porta Index",
                "Asymmetric Spread Index",
                "HB AMI",
                "Slope Index",
                "Area Index",
                "KDE AMI",
            ]
            out_name = f"{group_prefix}_{timescale}min_{num_bins}bins.csv"
            _write_csv(arr, header, out_dir / out_name)

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                                 Main                                       ║
# ╚════════════════════════════════════════════════════════════════════════════╝
def main() -> None:
    # Validate paths
    for path in (g1_BASE_DIR, g2_BASE_DIR, g1_IDS_PATH, g2_IDS_PATH):
        if not Path(path).exists():
            raise FileNotFoundError(f"Required path not found: {path}")
    
    # Create an export directory
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Load inclusion ID sets
    g1_ids = _load_ids(g1_IDS_PATH)
    g2_ids = _load_ids(g2_IDS_PATH)

    # Export CSV for the first group
    _compute_and_export_for_group("g1", g1_BASE_DIR, g1_ids, EXPORT_DIR)
    print("Finished group g1")

    # Export CSV for the second group
    _compute_and_export_for_group("g2", g2_BASE_DIR, g2_ids, EXPORT_DIR)
    print("Finished group g2")

if __name__ == "__main__":
    main()
