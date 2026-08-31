"""Generate a Build 2025-style MCNP input deck.

This is a standalone adaptation of the construction pattern in
FullFieldSimulation/GUI/mcnp_wrapper.py.
"""

from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from MCNPAutoScripting import Surfaces, mcnp


def build_2025():
    detector_cell = mcnp.Cell(
        cell_id=101,
        material_id=301,
        density=5.08,
        surface_string="-201",
        label="Detector",
    )
    detector_surface = Surfaces.rcc(
        surface_id=201,
        vx=56,
        vy=-5,
        vz=-1,
        h1=0,
        h2=20,
        h3=0,
        r=4.5,
    )
    detector_material = mcnp.Material(
        material_id=301,
        elements=["35079", "35081", "57139", "58140"],
        portions=[0.2946, 0.3069, 0.3485, 0.0500],
        labels=["Br79", "Br81", "La139", "Ce140"],
        label="Detector",
    )

    shielding_cell = mcnp.Cell(
        cell_id=121,
        material_id=2,
        density=4.78,
        surface_string="-31",
        label="PE+Pb shielding",
    )
    shielding_surface = Surfaces.rpp(
        surface_id=31,
        x1=19,
        x2=29,
        y1=-7.5,
        y2=7.5,
        z1=-11,
        z2=9,
    )
    shielding_material = mcnp.Material(
        material_id=2,
        elements=["6000", "1001", "82000"],
        portions=[0.04286, 0.00714, 0.95000],
        labels=["C", "H", "Pb"],
        label="PE+Pb",
    )

    wheel_cell = mcnp.Cell(
        cell_id=21,
        material_id=13,
        density=0.92,
        surface_string="-41 42",
        label="Wheel",
    )
    wheel_outer_surface = Surfaces.rcc(
        surface_id=41,
        vx=-2,
        vy=77,
        vz=8,
        h1=0,
        h2=25,
        h3=0,
        r=29,
    )
    wheel_inner_surface = Surfaces.rcc(
        surface_id=42,
        vx=-2,
        vy=77,
        vz=8,
        h1=0,
        h2=25,
        h3=0,
        r=27.7,
    )
    wheel_material = mcnp.Material(
        material_id=13,
        elements=["1001", "6000"],
        portions=[0.118371, 0.881629],
        labels=["H", "C"],
        label="Wheel",
    )

    detector_tally = mcnp.DetectorTally8(
        tally_id=8,
        detector_cells=[detector_cell.cell_id],
        geb=(-0.026198, 0.059551, -0.037176),
        phl=(1, 6, 1, 0),
    )

    soil_cell = mcnp.Cell(
        cell_id=1,
        material_id=1,
        density=1.6,
        surface_string="-11",
        label="Soil",
    )
    soil_material = mcnp.Material(
        material_id=1,
        elements=["1001", "8016", "11023"],
        portions=[0.111, 0.888, 0.001],
        labels=["H", "O", "Na"],
        label="Soil",
    )
    soil_surface = Surfaces.rpp(
        surface_id=11,
        x1=-100,
        x2=100,
        y1=-100,
        y2=100,
        z1=20,
        z2=100,
    )


    return mcnp.MCNP(
        title="Build 2025 example",
        cells=[detector_cell, shielding_cell, wheel_cell, soil_cell],
        surfaces=[
            detector_surface,
            shielding_surface,
            wheel_outer_surface,
            wheel_inner_surface,
            soil_surface,
        ],
        source=mcnp.Source(energy_string="14.0", position_string="0 0 0"),
        materials=[detector_material, shielding_material, wheel_material, soil_material],
        tallies=[detector_tally],
    )


def main():
    output_path = Path(__file__).with_name("build_2025.i")
    output_path.write_text(build_2025().string(), encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()