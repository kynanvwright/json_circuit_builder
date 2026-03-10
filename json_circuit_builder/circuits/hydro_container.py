
from ..components.circuit import Circuit
from ..components.specific_components import Pump, BucherValve, CV_rk1, PRV_DB4E, Orifice, Branch, Accumulator, IntensifierRam, Endcap


hyd_circuit = Circuit()
hyd_circuit.add_properties_and_imports()

# 301 Pump block
pb_301 = hyd_circuit.add_subcircuit("301_PUMP_BLOCK")
## components
pb_301.add_component(Pump(name='201_PUMP',displacement=4.09e-6))
pb_301.add_components(BucherValve, ['P1D', 'P2D', 'P3D'])
pb_301.add_components(CV_rk1, ['P2C', 'P3C'])
pb_301.add_component(PRV_DB4E(name='P1R',crack_pressure=320e5))
pb_301.add_component(PRV_DB4E(name='P2R',crack_pressure=500e5))
pb_301.add_component(Orifice(name='P1D_Orifice',diameter=1.5e-3))
pb_301.add_component(Orifice(name='P2D_Orifice',diameter=1.5e-3))
## branches
pb_301.add_component(Branch('branch_TPP1',output_name='TPP1'))
pb_301.add_component(Branch('branch_TPP2',output_name='TPP2'))
pb_301.add_component(Branch('branch_TPP3',output_name='TPP3'))
pb_301.add_component(Branch('branch_TPP4',output_name='TPP4'))
## connections
pb_301.add_connection('201_PUMP','branch_TPP1')
pb_301.add_connection('branch_TPP1','P2C')
pb_301.add_connection('branch_TPP1','P3C')
pb_301.add_connection('P2C','P3D')
pb_301.add_connection('P3D','branch_TPP3')
pb_301.add_connection('branch_TPP3','P1R')
pb_301.add_connection('branch_TPP3','P1D_Orifice')
pb_301.add_connection('P1D_Orifice','P1D')
pb_301.add_connection('P1D','branch_TPP4')
pb_301.add_connection('P1R','branch_TPP4')
pb_301.add_connection('P3C','branch_TPP2')
pb_301.add_connection('branch_TPP2','P2D')
pb_301.add_connection('branch_TPP2','P2R')
pb_301.add_connection('P2D','P2D_Orifice')
pb_301.add_connection('P2D_Orifice','branch_TPP4')
pb_301.add_connection('P2R','branch_TPP4')

# 302 Ram A Block
b_302 = hyd_circuit.add_subcircuit("302_RAM_A")
## components
b_302.add_components(BucherValve, ['A1D', 'A2D', 'A3D'])
b_302.add_components(PRV_DB4E, ['A1R', 'A2R', 'A3R', 'A4R'])
## branches
b_302.add_component(Branch('branch_TPA1',output_name='TPA1'))
b_302.add_component(Branch('branch_Tank_302'))
b_302.add_component(Branch('branch_LP_302'))
b_302.add_component(Branch('branch_HP_302'))
b_302.add_component(Branch('branch_TPV2_302'))
## connections
b_302.add_connection('branch_LP_302','A2R')
b_302.add_connection('A2R','branch_Tank_302')
b_302.add_connection('branch_LP_302','A2D')
b_302.add_connection('branch_HP_302','A1R')
b_302.add_connection('A1R','branch_Tank_302')
b_302.add_connection('branch_HP_302','A1D')
b_302.add_connection('A1D','branch_TPA1')
b_302.add_connection('A2D','branch_TPA1')
b_302.add_connection('branch_TPA1','A3D')
b_302.add_connection('branch_TPA1','A3R')
b_302.add_connection('A3R','branch_Tank_302')
b_302.add_connection('A3D','branch_TPV2_302')
b_302.add_connection('branch_TPV2_302','A4R')
b_302.add_connection('A4R','branch_Tank_302')

# 303 Ram B Block
b_303 = hyd_circuit.add_subcircuit("303_RAM_B")
## components
b_303.add_components(BucherValve, ['B1D', 'B2D', 'B3D'])
b_303.add_components(PRV_DB4E, ['B1R', 'B2R', 'B3R', 'B4R'])
b_303.add_component(Accumulator('601_HP_ACCUMULATOR', 2e-3, precharge_pressure=200e5))
b_303.add_component(Accumulator('602_LP_ACCUMULATOR', 5e-3, precharge_pressure=125e5))
## branches
b_303.add_component(Branch('branch_TPB1',output_name='TPB1'))
b_303.add_component(Branch('branch_Tank_303'))
b_303.add_component(Branch('branch_LP_303'))
b_303.add_component(Branch('branch_HP_303'))
b_303.add_component(Branch('branch_TPV2_303'))
## connections
b_303.add_connection('branch_LP_303','B2R')
b_303.add_connection('B2R','branch_Tank_303')
b_303.add_connection('branch_LP_303','B2D')
b_303.add_connection('branch_HP_303','B1R')
b_303.add_connection('B1R','branch_Tank_303')
b_303.add_connection('branch_HP_303','B1D')
b_303.add_connection('B1D','branch_TPB1')
b_303.add_connection('B2D','branch_TPB1')
b_303.add_connection('branch_TPB1','B3D')
b_303.add_connection('branch_TPB1','B3R')
b_303.add_connection('B3R','branch_Tank_303')
b_303.add_connection('B3D','branch_TPV2_303')
b_303.add_connection('branch_TPV2_303','B4R')
b_303.add_connection('B4R','branch_Tank_303')
b_303.add_connection('branch_HP_303','601_HP_ACCUMULATOR')
b_303.add_connection('branch_LP_303','602_LP_ACCUMULATOR')

# 307 MOOG
b_307 = hyd_circuit.add_subcircuit("307_MOOG")
## components
# b_307.add_component(NG3_2L('M1P'))
b_307.add_component(Branch('M1P')) # placeholder
b_307.add_component(CV_rk1('M1C'))
b_307.add_component(CV_rk1('I1C'))
b_307.add_component(PRV_DB4E('M1R', 600e5))
b_307.add_component(PRV_DB4E('M2R', 600e5))
b_307.add_component(IntensifierRam('110_Intensifier'))
b_307.add_component(Endcap('Intens_A_Endcap')) # placeholder
## branches
b_307.add_component(Branch('branch_TPM1', output_name='TPM1'))
b_307.add_component(Branch('branch_TPM2', output_name='TPM2'))
b_307.add_component(Branch('branch_Tank_307'))
b_307.add_component(Branch('branch_Intens_D'))
## connections
b_307.add_connection('branch_TPM1','M1R')
b_307.add_connection('branch_TPM1','M1P')
b_307.add_connection('branch_TPM2','M2R')
b_307.add_connection('branch_TPM2','M1P')
b_307.add_connection('M1C','M1P')
b_307.add_connection('M1R','branch_Tank_307')
b_307.add_connection('M2R','branch_Tank_307')
b_307.add_connection('M1P','branch_Tank_307')
b_307.add_connection('I1C','branch_Intens_D')
b_307.add_connection('branch_TPM1','110_Intensifier', outlet_port_override='B')
b_307.add_connection('branch_TPM2','110_Intensifier', outlet_port_override='C')
b_307.add_connection('branch_Intens_D','110_Intensifier', outlet_port_override='D')
b_307.add_connection('110_Intensifier','Intens_A_Endcap', inlet_port_override='A') # placeholder


# Tank Block
tank_400 = hyd_circuit.add_subcircuit("400_TANK")
## components
tank_400.add_component(Accumulator('400Tank', 0.02, 0.19, 1.4, 1.1e5, True))
## branches
tank_400.add_component(Branch('branch_Tank', output_name='TPC1'))
## connections
tank_400.add_connection('branch_Tank', '400Tank')

# Inter-block connections
hyd_circuit.add_connection('branch_Tank', '400_TANK', '201_PUMP', '301_PUMP_BLOCK')
hyd_circuit.add_connection('branch_TPP4', '301_PUMP_BLOCK', 'branch_Tank', '400_TANK')
hyd_circuit.add_connection('branch_Tank_302', '302_RAM_A', 'branch_Tank', '400_TANK')
hyd_circuit.add_connection('branch_TPP3', '301_PUMP_BLOCK', 'branch_LP_302', '302_RAM_A')
hyd_circuit.add_connection('branch_TPP2', '301_PUMP_BLOCK', 'branch_HP_302', '302_RAM_A')
hyd_circuit.add_connection('branch_Tank_303', '303_RAM_B', 'branch_Tank', '400_TANK')
hyd_circuit.add_connection('branch_LP_302', '302_RAM_A', 'branch_LP_303', '303_RAM_B')
hyd_circuit.add_connection('branch_HP_302', '302_RAM_A', 'branch_HP_303', '303_RAM_B')
hyd_circuit.add_connection('branch_TPP2', '301_PUMP_BLOCK', 'M1C', '307_MOOG')
hyd_circuit.add_connection('branch_Tank', '400_TANK', 'I1C', '307_MOOG')
hyd_circuit.add_connection('branch_TPA1', '302_RAM_A', 'branch_Intens_D', '307_MOOG')


# Final tidy up and checks
hyd_circuit.update_branch_pressure_outputs()
hyd_circuit.run_connection_checks()