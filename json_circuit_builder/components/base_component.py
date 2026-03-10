from typing import Literal

class BaseComponent:
    """Common behaviour for all hydraulic components."""

    def __init__(self, name: str, type: str | None = None):
        self.Name = name
        self.Type = type or self.__class__.__name__
        
        # Standardised fields every component always has
        # self.Inputs: list[dict] = []
        # self.Outputs: list[dict] = []
        # self.PortNames: list[str] = []  # for Branch-like components
        # self.Metadata: dict = {}        # optional extra info

    # ------------------------------------------------------------------
    # Utility initialisers
    # ------------------------------------------------------------------

    def init_two_port_outputs(self):
        """Set standard flowrate + pressure-in + pressure-out outputs."""
        n = self.Name
        self.Outputs = [
            {"Name": f"{n}Flowrate",    "Type": "Flowrate"},
            {"Name": f"{n}PressureIn",  "Type": "Pressure", "Location": "in"},
            {"Name": f"{n}PressureOut", "Type": "Pressure", "Location": "out"},
        ]

    # ------------------------------------------------------------------
    # Port resolution for connections
    # ------------------------------------------------------------------

    def get_port_for_connection(
        self,
        role: Literal["inlet", "outlet"],
        other_name: str,
    ) -> str:
        """
        Default port assignment. Components with multiple ports should override.
        """
        return "in" if role == "inlet" else "out"

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def set_if_not_none(self, attr: str, value):
        """Convenient conditional assignment."""
        if value is not None:
            setattr(self, attr, value)

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """
        Produce { component_name: { ...component fields... } }
        and exclude the `Name` key inside the inner dict.
        """
        internal = {
            key: value
            for key, value in self.__dict__.items()
            if key != "Name"
        }
        return {self.Name: internal}
