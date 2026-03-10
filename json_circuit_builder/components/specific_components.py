from typing import Literal

from .base_component import BaseComponent


class Pump(BaseComponent):
    def __init__(
            self, 
            name: str, 
            displacement: float = 0., 
            efficiency_volumetric: float = 0.94,
            efficiency_mechanical: float = 0.94,
            ):
        super().__init__(name, type="Pump")
        self.Displacement = displacement
        self.EfficiencyVolumetric = efficiency_volumetric
        self.EfficiencyMechanical = efficiency_mechanical
        self.Inputs = [ { "Name": f"{name}_RPM", "Type": "RPM" } ]
        self.Outputs = [ 
            { "Name": f"{name}_Torque", "Type": "Torque" },
            { "Name": f"{name}_Flowrate", "Type": "Flowrate" }
            ]


class BucherValve(BaseComponent):
    def __init__(self, name: str):
        super().__init__(name, type="BucherValve")
        self.Inputs = [ { "Name": f"{name}_signal", "Type": "ValveSignal" } ]
        self.init_two_port_outputs()


class CV_rk1(BaseComponent):
    def __init__(self, name: str):
        super().__init__(name, type="CV_rk1")
        self.init_two_port_outputs()


class PRV_DB4E(BaseComponent):
    def __init__(
            self, 
            name: str, 
            crack_pressure: float = 320e5,  # Pa
            ):
        super().__init__(name, type="PRV_DB4E")
        self.CrackPressure = crack_pressure
        self.init_two_port_outputs()


# Fancy valve
class NG3_2L(BaseComponent):
    def __init__(
            self, 
            name: str, 
            diameter: float = 0.0019, # m
            alpha: float = 0.3,
            leak_rate: float = 3.6e+13,
            min_q_for_linearisation: float = 2.0e-6,
            ):
        super().__init__(name, type="NG3_2L")
        self.Diameter = diameter
        self.alpha = alpha
        self.LeakRate = leak_rate
        self.MinQForLinearisation = min_q_for_linearisation
        self.Inputs = [ { "Name": f"{name}_signal", "Type": "ValveSignal" } ]
        self.Outputs = [ 
            { "Name": f"{name}PressureIn", "Type": "Pressure", "Location": "in"},
            { "Name": f"{name}PressureOut", "Type": "Pressure", "Location": "out"},
            { "Name": f"{name}Flowrate", "Type": "Flowrate" } ]


class Orifice(BaseComponent):
    def __init__(
            self, 
            name: str,
            diameter: float = 0.0015, # m
            alpha: float = 0.65,
            min_q_for_linearisation: float = 3.33333e-6,
            ):
        super().__init__(name, type="Orifice")
        self.Diameter = diameter
        self.alpha = alpha
        self.MinQForLinearisation = min_q_for_linearisation
        self.init_two_port_outputs()


class Branch(BaseComponent):
    def __init__(
            self, 
            name: str,
            port_names: list[str] | None = None,
            output_name: str | None = None
            ):
        super().__init__(name, type="Branch")
        self.PortNames = port_names or []
        if output_name:
            self.Outputs = [ { "Name": output_name, "Type": "Pressure", "Location": "" } ]

    def get_port_for_connection(
        self,
        role: Literal["inlet", "outlet"],
        other_name: str,
    ) -> str:
        # Dynamic per-connection port naming
        if role == "inlet":
            port_name = f"from_{other_name}"
        else:
            port_name = f"to_{other_name}"
        self.PortNames.append(port_name)
        return port_name
        
    def set_output_location(self):
        if hasattr(self, "Outputs"):
            self.Outputs[0]["Location"] = self.PortNames[0]


class Endcap(BaseComponent):
    def __init__(
            self, 
            name: str,
            ):
        super().__init__(name, type="Endcap")
        self.Outputs = [ { "Name": f"{name}_Pressure", "Type": "Pressure" } ]

    def get_port_for_connection(
        self,
        role: Literal["inlet", "outlet"],
        other_name: str,
    ) -> str:
        """
        Only has single port.
        """
        return "in"


class Reservoir(BaseComponent):
    def __init__(
            self, 
            name: str,
            pressure_input: str,
            port_names: list[str] | None = None,
            ):
        super().__init__(name, type="Reservoir")
        self.PortNames = port_names or []
        self.Inputs = [ { "Name": pressure_input, "Type": "Pressure" } ]
    

class Accumulator(BaseComponent):
    def __init__(
            self, 
            name: str,
            total_volume: float = 0.0025,
            max_oil_volume: float = 0.0023,
            heat_ratio: float = 1.4,
            precharge_pressure: float = 100e5,
            end_stop: bool = True,
            ):
        super().__init__(name, type="Accumulator")
        self.TotalVolume = total_volume
        self.MaxOilVolume = max_oil_volume
        self.HeatRatio = heat_ratio
        self.PrechargePressure = precharge_pressure
        self.EndStop = end_stop
        self.Outputs = [ 
            { "Name": f"{name}Volume", "Type": "Volume" },
            { "Name": f"{name}Pressure", "Type": "Pressure" },
            { "Name": f"{name}Flowrate", "Type": "Flowrate" } ]
    
    def get_port_for_connection(
        self,
        role: Literal["inlet", "outlet"],
        other_name: str,
    ) -> str:
        """
        Only has single port.
        """
        return "in"
        

class IntensifierRam(BaseComponent):
    def __init__(
            self, 
            name: str,
            layout: str = "PistonRodPiston",
            diameters: list[float] | None = None,
            stroke_length: float = 0.067,
            end_stop: bool = True,
            hard_stop_stiffness: float = 600e9,
            friction: dict[str, float] | None = None,
            ):
        super().__init__(name, type="IntensifierRam")
        self.Layout = layout
        self.StrokeLength = stroke_length
        self.EndStop = end_stop
        self.HardStopStiffness = hard_stop_stiffness
        self.Outputs = [ 
            { "Name": f"{name}Stroke", "Type": "Stroke" },
            { "Name": f"{name}StrokeDot", "Type": "StrokeRate" } ]
        if friction is None:
            friction = {
                "StaticFrictionForce" : 150,
                "DynamicFrictionForce" : 100,
                "ViscousFrictionForce" : 100,
                "StribeckVelocity" : 1.25e-2
            }
        self.Friction = friction
        if diameters is None:
            diameters = [0.05, 0.025, 0.05]
        self.BoreDiameterAB = diameters[0]
        self.RodDiameterBC = diameters[1]
        self.BoreDiameterCD = diameters[2]
    

# # Example usage:
# pump = Pump(
#     name="201_PUMP",
#     displacement=4.09e-6,
#     efficiencyVolumetric=0.94,
#     efficiencyMechanical=0.94,
# )
# a=2