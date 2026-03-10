from collections import Counter

from .base_component import BaseComponent
from .connection import Connection

class SubCircuit:
    def __init__(self, name: str):
        self.Type = "SubCircuit"
        self.Name = name
        self.Components: dict[str, BaseComponent] = {}
        self.Connections: dict[str, Connection] = {}

    def add_component(self, component: BaseComponent):
        self.Components[component.Name] = component
        return component
    
    def add_components(self, component: BaseComponent, names: list[str]):
        components = []
        for name in names:
            self.Components[name] = component(name)
            components.append(self.Components[name])
        return components

    def add_connection(
        self, 
        inlet: str, 
        outlet: str, 
        type: str = "Direct",
        length: float | None = None,
        diameter: float | None = None,
        inlet_port_override: str | None= None,
        outlet_port_override: str | None= None,
    ):
        inlet_comp = self.Components[inlet]
        outlet_comp = self.Components[outlet]

        # Ask each component what port to use
        inlet_port_name = inlet_port_override if inlet_port_override else inlet_comp.get_port_for_connection(
            role="outlet",  # this component is on the "sending" side
            other_name= outlet,
        )
        outlet_port_name = outlet_port_override if outlet_port_override else outlet_comp.get_port_for_connection(
            role="inlet",   # this component is on the "receiving" side
            other_name = inlet,
        )

        name = f"{inlet}_to_{outlet}"

        self.Connections[name] = Connection(
            name=name,
            type=type,
            inlet=f"{inlet}.{inlet_port_name}",
            outlet=f"{outlet}.{outlet_port_name}",
            length=length,
            diameter=diameter,
        )
        return self.Connections[name]

    def to_internal_dict(self) -> dict:
        """Shape used inside the top-level Components dict."""
        return {
            "Type": self.Type,
            "Components": {
                name: comp.to_dict()[name]
                for name, comp in self.Components.items()
            },
            "Connections": {
                name: comp.to_dict()[name]
                for name, comp in self.Connections.items()
            },
        }

    def to_dict(self) -> dict:
        """{ Name: {Type: 'SubCircuit', Components: {...}, ...} }"""
        return {self.Name: self.to_internal_dict()}
