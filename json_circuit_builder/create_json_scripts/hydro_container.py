from pathlib import Path

from ..circuits.hydro_container import hyd_circuit

_output_dir = Path(__file__).resolve().parent.parent / "outputs"
hyd_circuit.create_json(str(_output_dir / "Hydro_Container_Circuit_generated.json"))