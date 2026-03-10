import json
from collections import Counter
from pathlib import Path

from .properties_and_imports import extra_properties
from .subcircuit import SubCircuit
from .base_component import BaseComponent
from .connection import Connection


class Circuit:
    def __init__(self):
        self.components: dict[str, SubCircuit] = {}
        self.connections: dict = {}

        # Optional top-level props
        self.oil_properties = None
        self.valves = None
        self.connectors = None

    def add_properties_and_imports(self, detail_dict: dict = extra_properties):
        self.oil_properties = detail_dict["OilProperties"]
        self.valves = detail_dict["Valves"]
        self.connectors = detail_dict["Connectors"]

    # --- component helpers ---

    def add_subcircuit(self, name: str) -> SubCircuit:
        subcircuit = SubCircuit(name)
        self.components[name] = subcircuit
        return subcircuit

    def add_component(self, component: BaseComponent):
        """Add a top-level component (not in a subcircuit)."""
        self.components[component.Name] = component
        return component

    def get_component(self, name: str):
        return self.components[name]

    # --- connection helpers ---

    def add_connection(self, 
                       inlet: str,
                       inlet_subcircuit: str,
                       outlet: str, 
                       outlet_subcircuit: str,
                       type: str = "Direct",
                       length: float | None = None,
                       diameter: float | None = None):
        # If inlet is a branch, add a port for the connection
        if self.components[inlet_subcircuit].Components[inlet].Type == 'Branch':
            inlet_name = f"to_{outlet}"
            self.components[inlet_subcircuit].Components[inlet].PortNames.append(inlet_name)
        else:
            inlet_name = 'out'
        # If outlet is a branch, add a port for the connection
        if self.components[outlet_subcircuit].Components[outlet].Type == 'Branch':
            outlet_name = f"from_{inlet}"
            self.components[outlet_subcircuit].Components[outlet].PortNames.append(outlet_name)
        else:
            outlet_name = 'in'
        # Add to the connections dict
        name = f"{inlet}_to_{outlet}"
        self.connections[name] = Connection(
            name=name,
            type=type, 
            inlet=f"{inlet}.{inlet_name}", 
            outlet=f"{outlet}.{outlet_name}",
            length=length,
            diameter=diameter)
        return self.connections[f"{inlet}_to_{outlet}"]

    def iter_connections(self):
        """Yield every Connection in the circuit (top-level + inside components)."""
        # Top-level connections
        yield from self.connections.values()

        # Per-component connections
        for comp in self.components.values():
            conns = getattr(comp, "Connections", None)
            if isinstance(conns, dict):
                yield from conns.values()

    def iter_components(self, type=None):
        """Yield every Component in the Subcircuits."""
        # Per-subcircuit component
        for comp in self.components.values():
            children = getattr(comp, "Components", None)
            if isinstance(children, dict):
                for child in children.values():
                    if type is None or child.Type == type:
                        yield child

    def run_connection_checks(self):
        # will need more complex logic once I expand to multiple blocks

        port_counts = Counter(
            port.split('.')[0]
            for c in self.iter_connections()
            for port in (c.Inlet, c.Outlet)
        )
        components = {comp.Name for comp in self.iter_components()}
        components_with_no_connections = components - set(port_counts.keys())
        components_missing_connections = {k for k, v in port_counts.items() if v < 2}
        # extra logic as accumulators only require 1 port
        accumulators = {comp.Name for comp in self.iter_components('Accumulator')}
        endcaps = {comp.Name for comp in self.iter_components('Endcap')}
        components_missing_connections -= (accumulators | endcaps)
        if (len(components_with_no_connections)>0):
            raise ValueError(f"Circuit is missing any connections for the following components: {components_with_no_connections}")
        if (len(components_missing_connections)>0):
            raise ValueError(f"Circuit is missing some connections for the following components: {components_missing_connections}")

    # --- branch updates ---
    def run_on_components(self, type, method_name, *args, **kwargs):
        for comp in self.iter_components(type=type):
            method = getattr(comp, method_name)
            method(*args, **kwargs)

    def update_branch_pressure_outputs(self):
        self.run_on_components('Branch', 'set_output_location')

    # --- serialisation ---

    def to_dict(self) -> dict:
        components_dict: dict[str, dict] = {}

        for name, comp in self.components.items():
            if isinstance(comp, SubCircuit):
                components_dict[name] = comp.to_internal_dict()
            else:
                # BaseComponent: to_dict() returns {name: {...}}
                components_dict[name] = comp.to_dict()[name]

        connections_dict = {
            name: comp.to_dict()[name]
            for name, comp in self.connections.items()
        }

        result = {
            "Components": components_dict,
            "Connections": connections_dict,
        }

        # Only include these if they’ve been set
        if self.oil_properties is not None:
            result["OilProperties"] = self.oil_properties
        if self.valves is not None:
            result["Valves"] = self.valves
        if self.connectors is not None:
            result["Connectors"] = self.connectors

        return result
    
    def create_json(self, path_string: str):
        path = Path(path_string)
        with path.open("w") as f:
            json.dump(self.to_dict(), f, indent=2)