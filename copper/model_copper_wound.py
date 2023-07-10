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
        I0 = kwargs.get("I0", 12.5)  # Stator current of one phase [A]
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
        femm_metadata.depth = 69.20

        self.platform = Femm(femm_metadata)
        self.snapshot = Snapshot(self.platform)

    def define_materials(self):

        # define default materials
        air = Material("air")
        air.meshsize = 1.0

        wire = Material("copper")
        wire.lamination_type = "magnetwire"
        wire.diameter = 0.67
        wire.conductivity = 58e6
        wire.meshsize = 1.0

        steel = Material("S235") # Approximated with 1018 steel
        steel.conductivity = 5.8e6
        steel.thickness = 0.60
        steel.fill_factor = 0.94
        steel.b = [0.000000, 0.250300, 0.925000, 1.250000, 1.390000, 1.525000, 1.710000, 1.870000, 1.955000, 2.020000,
                   2.110000, 2.225000, 2.430000]
        steel.h = [0.000000, 238.732500, 795.775000, 1591.550000, 2387.325000, 3978.875000, 7957.750000, 15915.500000,
                   23873.250000, 39788.750000, 79577.500000, 159155.000000, 318310.000000]

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
