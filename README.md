# MCNPAutoScripting
Tools for automatically generating MCNP input scripts.

## Installation

Install the latest version directly from GitHub:

```bash
python -m pip install "git+https://github.com/JoseACortes/MCNPAutoScripting.git"
```

To update to the latest version, run:

```bash
python -m pip install --upgrade --force-reinstall "git+https://github.com/JoseACortes/MCNPAutoScripting.git"
```

## Usage

```python
from mcnp_auto_scripting import mcnp

cell = mcnp.Cell(cell_id=1, material_id=1, density=1.0)
print(cell.string())
```

See [examples/generate_input.py](examples/generate_input.py) for a complete
example that generates an MCNP input deck. Run it with:

```bash
python examples/generate_input.py
```

For a larger detector, shielding, and wheel model adapted from the full-field
simulation wrapper, run:

```bash
python examples/build_2025.py
```
