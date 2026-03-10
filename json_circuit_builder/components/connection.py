from .base_component import BaseComponent


class Connection(BaseComponent):
    def __init__(
            self, 
            name: str, 
            type: str,
            inlet: str,
            outlet: str,
            length: float | None = None,
            diameter: float | None = None
            ):
        super().__init__(name, type=type)
        self.Inlet = inlet
        self.Outlet = outlet
        self.set_if_not_none("Length", length)
        self.set_if_not_none("Diameter",diameter)