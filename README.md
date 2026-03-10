# JSON Builder

Programmatic builder for hydraulic circuit JSON definitions.

## Setup (new repo)

After creating the new repo, move `setup.py`, `README.md`, and `.gitignore` to the repo root so the structure is:

```
repo-root/
├── setup.py
├── README.md
├── .gitignore
└── json_builder/
    ├── __init__.py
    ├── test.py
    ├── components/
    ├── circuits/
    ├── create_json_scripts/
    └── outputs/
```

Then install in editable mode:

```bash
pip install -e .
```

## Usage

```python
from json_builder.components import Circuit, Pump, Branch

circuit = Circuit()
circuit.add_properties_and_imports()

block = circuit.add_subcircuit("MY_BLOCK")
block.add_component(Pump(name="pump_1", displacement=4.09e-6))
block.add_component(Branch("branch_1", output_name="TP1"))
block.add_connection("pump_1", "branch_1")

circuit.create_json("output.json")
```

## Project Structure

```
json_builder/
├── components/       # Core classes: Circuit, SubCircuit, BaseComponent, Connection
├── circuits/         # Pre-built circuit definitions
├── create_json_scripts/  # Scripts to generate JSON from circuit definitions
└── outputs/          # Generated JSON files
```

## Notes

- The `Valves` and `Connectors` file paths in `components/properties_and_imports.py` reference external database files. Update these paths to match your local environment.
