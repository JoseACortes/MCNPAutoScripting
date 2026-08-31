"""Generate a minimal MCNP input deck for a water-filled box."""

from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mcnp_auto_scripting import Surfaces, mcnp


def main():
    water_box = Surfaces.rpp(
        surface_id=1,
        x1=-10,
        x2=10,
        y1=-10,
        y2=10,
        z1=-10,
        z2=10,
        label="Water volume",
    )
    water = mcnp.Material(
        material_id=1,
        elements=["1001.80c", "8016.80c"],
        portions=[2, 1],
        density_type="atomic",
        label="Water",
    )
    water_cell = mcnp.Cell(
        cell_id=1,
        material_id=1,
        density=0.066,
        density_type="atomic",
        surface_string="-1",
        label="Water-filled box",
    )

    deck = mcnp.MCNP(
        title="Water box example",
        cells=[water_cell],
        surfaces=[water_box],
        source=mcnp.Source(energy_string="14.0", position_string="0 0 0"),
        materials=[water],
    )

    output_path = Path(__file__).with_name("water_box.i")
    output_path.write_text(deck.string(), encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()