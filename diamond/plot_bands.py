import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# SETTINGS
# ------------------------------------------------------------

input_file = "diamond.bands.dat.gnu"
output_file = "diamond_band_structure.png"

# Diamond has 8 valence electrons in the 2-atom primitive cell.
# Each band holds 2 electrons, so the first 4 bands are occupied.
number_occupied_bands = 4

# ------------------------------------------------------------
# READ QUANTUM ESPRESSO BAND DATA
# ------------------------------------------------------------

# The .gnu file consists of separate band blocks divided by blank lines.
bands = []
current_band = []

with open(input_file, "r") as file:
    for line in file:

        # A blank line means we have reached the end of one band.
        if line.strip() == "":
            if current_band:
                bands.append(np.array(current_band))
                current_band = []
            continue

        values = line.split()

        if len(values) >= 2:
            k = float(values[0])
            energy = float(values[1])
            current_band.append([k, energy])

# Add the final band if the file does not end with a blank line.
if current_band:
    bands.append(np.array(current_band))

print("Number of bands found:", len(bands))

# ------------------------------------------------------------
# FIND THE VALENCE-BAND MAXIMUM
# ------------------------------------------------------------

occupied_bands = bands[:number_occupied_bands]

valence_band_maximum = max(
    np.max(band[:, 1])
    for band in occupied_bands
)

print("Valence-band maximum =", valence_band_maximum, "eV")

# ------------------------------------------------------------
# FIND THE CONDUCTION-BAND MINIMUM AND BAND GAP
# ------------------------------------------------------------

unoccupied_bands = bands[number_occupied_bands:]

conduction_band_minimum = min(
    np.min(band[:, 1])
    for band in unoccupied_bands
)

band_gap = conduction_band_minimum - valence_band_maximum

print("Conduction-band minimum =", conduction_band_minimum, "eV")
print("Calculated band gap =", band_gap, "eV")

# ------------------------------------------------------------
# HIGH-SYMMETRY POINTS
# ------------------------------------------------------------

# Your calculation used:
# Gamma -> X -> W -> K -> Gamma -> L
#
# Each of the first five path segments was generated using the
# K_POINTS crystal_b specification from the QE bands calculation.
#
# We determine the total k-distance from the actual .gnu data.

k_min = min(np.min(band[:, 0]) for band in bands)
k_max = max(np.max(band[:, 0]) for band in bands)

# Relative segment positions for the path used in the calculation.
# These are used only for labeling the horizontal axis.
#
# If you later want exact high-symmetry positions directly from
# bands.x output, these values can be replaced with those positions.

high_symmetry_points = [
    0.0000,   # Gamma
    1.0000,   # X
    1.5000,   # W
    1.8536,   # K
    2.9142,   # Gamma
    3.7802    # L
]

high_symmetry_labels = [
    r"$\Gamma$",
    "X",
    "W",
    "K",
    r"$\Gamma$",
    "L"
]

# ------------------------------------------------------------
# PLOT
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 6))

for band in bands:

    k = band[:, 0]

    # Shift energies so that the valence-band maximum is 0 eV.
    energy = band[:, 1] - valence_band_maximum

    ax.plot(k, energy, linewidth=1.2, color="black")

# Horizontal line at the valence-band maximum.
ax.axhline(0, linewidth=0.8, linestyle="--")

# Vertical lines at high-symmetry points.
for position in high_symmetry_points:
    ax.axvline(position, linewidth=0.6, linestyle=":")

# Label high-symmetry points.
ax.set_xticks(high_symmetry_points)
ax.set_xticklabels(high_symmetry_labels, fontsize=12)

ax.set_xlim(k_min, k_max)

# This range focuses on the bands near the band gap.
# Change these values if you want to display more bands.
ax.set_ylim(-15, 15)

ax.set_xlabel("Wave vector")
ax.set_ylabel("Energy relative to VBM (eV)")
ax.set_title("Electronic Band Structure of Diamond")

plt.tight_layout()

# Save at high resolution for your case-study report.
plt.savefig(output_file, dpi=300, bbox_inches="tight")

print("Plot saved as:", output_file)

