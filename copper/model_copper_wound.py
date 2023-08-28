import math
from copy import copy
from math import cos, pi, radians

from digital_twin_distiller import inch2mm
from digital_twin_distiller.boundaries import DirichletBoundaryCondition
from digital_twin_distiller.boundaries import AntiPeriodicBoundaryCondition
from digital_twin_distiller.boundaries import AntiPeriodicAirGap
from digital_twin_distiller.material import Material
from digital_twin_distiller.metadata import FemmMetadata
from digital_twin_distiller.model import BaseModel
from digital_twin_distiller.modelpaths import ModelDir
from digital_twin_distiller.modelpiece import ModelPiece
from digital_twin_distiller.objects import CircleArc, Node, Line
from digital_twin_distiller.platforms.femm import Femm
from digital_twin_distiller.snapshot import Snapshot

ModelDir.set_base(__file__)

def cart2pol(x: float, y: float):
    rho = math.hypot(x, y)
    phi = math.atan2(y, x)
    return rho, phi


def pol2cart(rho: float, phi: float):
    x = rho * math.cos(math.radians(phi))
    y = rho * math.sin(math.radians(phi))
    return x, y

def deg_to_rad(angle_deg):
    angle_rad = angle_deg * math.pi / 180
    return angle_rad

ORIGIN = Node(0.0, 0.0)

class SzEReluctanceMotor(BaseModel):
    """docstring for SzE Reluctance Motor"""
    def __init__(self, **kwargs):
        super(SzEReluctanceMotor, self).__init__(**kwargs)
        self._init_directories()

        # Geometric parameters
        """ source: in resources """
        self.msh_air_gap = kwargs.get("msh_air_gap", 1)  # Airgap mesh size [mm]
        self.msh_air_rot = kwargs.get("msh_air_rot", 1)  # Air in rotor mesh size [mm]
        self.msh_steel_stator = kwargs.get("msh_steel_stator", 1)  # Stator steel mesh size [mm]
        self.msh_steel_rotor = kwargs.get("msh_steel_rotor", 1)  # Rotor steel mesh size [mm]
        self.rotor_angle = kwargs.get("rotor_angle", 0)  # Rotor angle in mechanical degrees to 0 degrees [deg]
        self.delta = kwargs.get("delta", -11.25)  # Offset of the rotor angle [°]

        # Excitation setup
        I0 = kwargs.get("I0", 0)  # Stator current of one phase [A]
        alpha = kwargs.get("alpha", 0)  # Current angle [°]
        slot_area = 0.000142793  # area of the slot [m^2]
        Nturns = 8  # turns of the coil in one slot [u.]
        nturns = 20  # paralell copper conductors in one turn [u.]
        d_cond = 0.00067  # diameter of a copper conductor based on IEC 60217-0-1:2013+AMD1:2019 [m]
        A_cond = (pow(d_cond / 2, 2)) * pi
        coil_area = Nturns * nturns * A_cond
        fill_factor = coil_area / slot_area
        J0 = Nturns * I0 / slot_area

        self.JU = J0 * cos(radians(alpha))
        self.JV = J0 * cos(radians(alpha + 120))
        self.JW = J0 * cos(radians(alpha + 240))

    def setup_solver(self):
        femm_metadata = FemmMetadata()
        femm_metadata.problem_type = "magnetic"
        femm_metadata.coordinate_type = "planar"
        femm_metadata.file_script_name = self.file_solver_script
        femm_metadata.file_metrics_name = self.file_solution
        femm_metadata.unit = "millimeters"
        femm_metadata.smartmesh = True
        femm_metadata.depth = 78

        self.platform = Femm(femm_metadata)
        self.snapshot = Snapshot(self.platform)

    def define_materials(self):

        # define default materials
        air = Material("air")
        air.meshsize = 1.0

        wire = Material("copper")
        wire.lamination_type = "0"
        wire.diameter = 0.67
        wire.conductivity = 58e6
        wire.meshsize = 1.0

        steel = Material("S235") # Approximated with A36 steel
        steel.conductivity = 5.8e6
        steel.thickness = 1.2
        steel.fill_factor = 0.98
        steel.b = [0.0000, 0.0974, 0.1949, 0.3004, 0.3343, 0.3609, 0.3900, 0.4110, 0.4354, 0.4609, 0.4895, 0.5102,
                   0.5362, 0.5611, 0.5893, 0.6102, 0.6362, 0.6608, 0.6854, 0.7066, 0.7355, 0.7613, 0.7893, 0.8092,
                   0.8344, 0.8596, 0.8826, 0.9015, 0.9230, 0.9433, 0.9640, 0.9857, 1.0048, 1.0309, 1.0556, 1.0780,
                   1.0998, 1.1200, 1.1397, 1.1597, 1.1796, 1.1998, 1.2180, 1.2366, 1.2552, 1.2736, 1.2936, 1.3086,
                   1.3265, 1.3433, 1.3597, 1.3764, 1.3946, 1.4072, 1.4219, 1.4357, 1.4495, 1.4633, 1.4771, 1.4920,
                   1.5018, 1.5114, 1.5198, 1.5284, 1.5375, 1.5459, 1.5545, 1.5634, 1.5719, 1.5805, 1.5895, 1.5981,
                   1.6048, 1.6119, 1.6188, 1.6256, 1.6325, 1.6393, 1.6462, 1.6529, 1.6591, 1.6630, 1.6733
]
        steel.h = [0.0000, 119.4373, 177.5188, 221.0054, 241.0910, 251.9625, 265.3464, 277.0617, 287.0970, 299.6462,
                   313.8689, 326.4229, 338.1333, 351.5214, 365.7444, 379.9749, 393.3619, 407.5887, 420.9770, 436.0455,
                   453.6212, 470.3617, 487.9383, 504.6847, 521.4258, 539.8434, 555.7485, 571.6575, 590.0790, 608.5016,
                   626.9239, 645.3451, 663.7690, 682.1858, 700.6040, 717.3479, 734.0924, 752.5152, 770.9384, 789.3614,
                   807.7844, 826.2072, 844.6320, 863.0563, 881.4807, 899.9052, 918.3281, 936.7561, 955.1812, 973.6074,
                   992.0339, 1010.4602, 1028.8849, 1047.3153, 1065.7436, 1084.1728, 1102.6020, 1121.0312, 1139.4604,
                   1157.8884, 1176.3217, 1194.7550, 1213.1896, 1231.6240, 1250.0580, 1268.4925, 1286.9270, 1305.3610,
                   1323.7956, 1342.2299, 1360.6640, 1379.0984, 1397.5347, 1415.9706, 1434.4067, 1452.8430, 1471.2791,
                   1489.7153, 1508.1514, 1526.5877, 1545.0245, 1557.5954, 1582.7347]

        ### create concrete materials
        # Airgap material
        airgap = copy(air)
        airgap.name = 'air_gap'
        airgap.meshsize = self.msh_air_gap

        # Flux barrier material
        airrot = copy(air)
        airrot.name = 'air_rot'
        airrot.meshsize = self.msh_air_rot

        # Coils
        # PHASE U
        phase_U_positive = copy(wire)
        phase_U_positive.name = "U+"
        phase_U_positive.Je = self.JU

        phase_U_negative = copy(wire)
        phase_U_negative.name = "U-"
        phase_U_negative.Je = -self.JU

        # PHASE V
        phase_V_positive = copy(wire)
        phase_V_positive.name = "V+"
        phase_V_positive.Je = self.JV

        phase_V_negative = copy(wire)
        phase_V_negative.name = "V-"
        phase_V_negative.Je = -self.JV

        # PHASE W
        phase_W_positive = copy(wire)
        phase_W_positive.name = "W+"
        phase_W_positive.Je = self.JW

        phase_W_negative = copy(wire)
        phase_W_negative.name = "W-"
        phase_W_negative.Je = -self.JW

        # Stator steel
        steel_stator = copy(steel)
        steel_stator.name = 'steel_stator'
        steel_stator.meshsize = self.msh_steel_stator

        # Rotor steel
        steel_rotor = copy(steel)
        steel_rotor.name = 'steel_rotor'
        steel_rotor.meshsize = self.msh_steel_rotor

        # Adding the used materials to the snapshot
        self.snapshot.add_material(air)
        self.snapshot.add_material(airgap)
        self.snapshot.add_material(airrot)
        self.snapshot.add_material(phase_U_positive)
        self.snapshot.add_material(phase_U_negative)
        self.snapshot.add_material(phase_V_positive)
        self.snapshot.add_material(phase_V_negative)
        self.snapshot.add_material(phase_W_positive)
        self.snapshot.add_material(phase_W_negative)
        self.snapshot.add_material(steel_stator)
        self.snapshot.add_material(steel_rotor)

    def define_boundary_conditions(self):
        # Define boundary conditions
        a0 = DirichletBoundaryCondition("a0", field_type="magnetic", magnetic_potential=0.0)

        # Adding boundary conditions to the snapshot
        self.snapshot.add_boundary_condition(a0)

    def add_postprocessing(self):
        entities = [
                (0, 32)]
        # (0,50), (0,58), (0,-50), (0,-58), (-40,35), (40,35), (-40,-35), (40,-35), (-50,0), (-58,0), (50,0), (58,0),
        self.snapshot.add_postprocessing("integration", entities, "Torque")

    def build_stator(self):

        stator= ModelPiece('stator')
        stator.load_piece_from_dxf(ModelDir.RESOURCES / "SzESynRM_stator.dxf")
        self.geom.merge_geometry(stator.geom)

    def build_rotor(self):

        rotor = ModelPiece('rotor')
        rotor.load_piece_from_dxf(ModelDir.RESOURCES / "SzESynRM_rotor.dxf")
        rotor.rotate(ref_point=(0, 0), alpha=self.rotor_angle + self.delta)

        self.geom.merge_geometry(rotor.geom)

    def build_material(self):
        self.assign_material(*Node.from_polar(75, 90 + self.rotor_angle + self.delta), "air_gap")
        self.assign_material(*Node.from_polar(51, 90 + self.rotor_angle + self.delta), "air_rot")
        self.assign_material(*Node.from_polar(59, 90 + self.rotor_angle + self.delta), "air_rot")
        self.assign_material(*Node.from_polar(51, -90 + self.rotor_angle + self.delta), "air_rot")
        self.assign_material(*Node.from_polar(59, -90 + self.rotor_angle + self.delta), "air_rot")
        self.assign_material(*Node.from_polar(55, 45 + self.rotor_angle + self.delta), "air_rot")
        self.assign_material(*Node.from_polar(55, 135 + self.rotor_angle + self.delta), "air_rot")
        self.assign_material(*Node.from_polar(55, -45 + self.rotor_angle + self.delta), "air_rot")
        self.assign_material(*Node.from_polar(55, -135 + self.rotor_angle + self.delta), "air_rot")
        self.assign_material(*Node.from_polar(51, 0 + self.rotor_angle + self.delta), "air_rot")
        self.assign_material(*Node.from_polar(59, 0 + self.rotor_angle + self.delta), "air_rot")
        self.assign_material(*Node.from_polar(51, 180 + self.rotor_angle + self.delta), "air_rot")
        self.assign_material(*Node.from_polar(59, 180 + self.rotor_angle + self.delta), "air_rot")
        self.assign_material(0, 0, "air_rot")

        self.assign_material(0, 115, "steel_stator")
        self.assign_material(*Node.from_polar(35, 90 + self.rotor_angle + self.delta), "steel_rotor")

        self.snapshot.add_geometry(self.geom)

    def build_coil(self):

        labels = ["U+", "U+", "U+", "U+", "V-", "V-", "V-", "V-", "W+", "W+", "W+", "W+",
                  "U-", "U-", "U-", "U-", "V+", "V+", "V+", "V+", "W-", "W-", "W-", "W-",
                  "U+", "U+", "U+", "U+", "V-", "V-", "V-", "V-", "W+", "W+", "W+", "W+",
                  "U-", "U-", "U-", "U-", "V+", "V+", "V+", "V+", "W-", "W-", "W-", "W-",
                  "U+", "U+", "U+", "U+", "V-", "V-", "V-", "V-", "W+", "W+", "W+", "W+",
                  "U-", "U-", "U-", "U-", "V+", "V+", "V+", "V+", "W-", "W-", "W-", "W-",
                  "U+", "U+", "U+", "U+", "V-", "V-", "V-", "V-", "W+", "W+", "W+", "W+",
                  "U-", "U-", "U-", "U-", "V+", "V+", "V+", "V+", "W-", "W-", "W-", "W-",
                  ]
        label = Node.from_polar(100, 90)
        for i in range(48):
             self.assign_material(label.x, label.y, labels[i])
             label = label.rotate(-pi / 4 / 6)

        labels = ["U+", "U+", "U+", "U+", "V-", "V-", "V-", "V-", "W+", "W+", "W+", "W+",
                  "U-", "U-", "U-", "U-", "V+", "V+", "V+", "V+", "W-", "W-", "W-", "W-",
                  "U+", "U+", "U+", "U+", "V-", "V-", "V-", "V-", "W+", "W+", "W+", "W+",
                  "U-", "U-", "U-", "U-", "V+", "V+", "V+", "V+", "W-", "W-", "W-", "W-",
                  "U+", "U+", "U+", "U+", "V-", "V-", "V-", "V-", "W+", "W+", "W+", "W+",
                  "U-", "U-", "U-", "U-", "V+", "V+", "V+", "V+", "W-", "W-", "W-", "W-",
                  "U+", "U+", "U+", "U+", "V-", "V-", "V-", "V-", "W+", "W+", "W+", "W+",
                  "U-", "U-", "U-", "U-", "V+", "V+", "V+", "V+", "W-", "W-", "W-", "W-",
                  ]
        label = Node.from_polar(90, 90)
        for i in range(48):
            self.assign_material(label.x, label.y, labels[i])
            label = label.rotate(-pi / 4 / 6)

        self.snapshot.add_geometry(self.geom)

    def build_boundary(self):

        self.assign_boundary_arc(120, -0, "a0")
        self.assign_boundary_arc(-120, 0, "a0")

        self.snapshot.add_geometry(self.geom)

    def build_geometry(self):

            self.build_stator()
            self.build_rotor()
            self.build_material()
            self.build_coil()
            self.build_boundary()
            self.snapshot.add_geometry(self.geom)

if __name__ == "__main__":
    m = SzEReluctanceMotor(exportname="dev")
    print(m(cleanup=True, devmode=True))
