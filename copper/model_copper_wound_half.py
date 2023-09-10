import math
from copy import copy
from math import cos, pi, radians

from digital_twin_distiller import inch2mm
from digital_twin_distiller.boundaries import DirichletBoundaryCondition
from digital_twin_distiller.boundaries import PeriodicBoundaryCondition
from digital_twin_distiller.boundaries import PeriodicAirGap
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

class SzEReluctanceMotorHalf(BaseModel):
    """docstring for SzE Reluctance Motor"""
    def __init__(self, **kwargs):
        super(SzEReluctanceMotorHalf, self).__init__(**kwargs)
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
        I0 = kwargs.get("I0", 100)  # Stator current of one phase [A]
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
        femm_metadata.depth = 70

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

        steel = Material("S235")
        steel.conductivity = 5.8
        steel.thickness = 0.65
        steel.fill_factor = 0.98

#         MEASUREMENT
        steel.h = [0, 21.6667, 43.3333, 65.0, 86.6667, 108.3333, 130.0, 151.6667, 173.3333, 195.0, 195.0, 299.7884,
                   404.5767, 509.3651, 614.1534, 718.9418, 823.7302, 928.5185, 1033.3069, 1138.0952, 1242.8836,
                   1347.672, 1452.4603, 1557.2487, 1662.037, 1766.8254, 1871.6138, 1976.4021, 2081.1905, 2185.9788,
                   2290.7672, 2395.5556, 2500.3439, 2605.1323, 2709.9206, 2814.709, 2919.4974, 3024.2857, 3129.0741,
                   3233.8624, 3338.6508, 3443.4392, 3548.2275, 3653.0159, 3757.8042, 3862.5926, 3967.381, 4072.1693,
                   4176.9577, 4281.746, 4386.5344, 4491.3228, 4596.1111, 4700.8995, 4805.6878, 4910.4762, 5015.2646,
                   5120.0529, 5224.8413, 5329.6296, 5434.418, 5539.2063, 5643.9947, 5748.7831, 5853.5714, 5958.3598,
                   6063.1481, 6167.9365, 6272.7249, 6377.5132, 6482.3016, 6587.0899, 6691.8783, 6796.6667, 6901.455,
                   7006.2434, 7111.0317, 7215.8201, 7320.6085, 7425.3968, 7530.1852, 7634.9735, 7739.7619, 7844.5503,
                   7949.3386, 8054.127, 8158.9153, 8263.7037, 8368.4921, 8473.2804, 8578.0688, 8682.8571, 8787.6455,
                   8892.4339, 8997.2222, 9102.0106, 9206.7989, 9311.5873, 9416.3757, 9521.164, 9625.9524, 9730.7407,
                   9835.5291, 9940.3175, 10045.1058, 10149.8942, 10254.6825, 10359.4709, 10464.2593, 10569.0476,
                   10673.836, 10778.6243, 10883.4127, 10988.2011, 11092.9894, 11197.7778, 11302.5661, 11407.3545,
                   11512.1429, 11616.9312, 11721.7196, 11826.5079, 11931.2963, 12036.0847, 12140.873, 12245.6614,
                   12350.4497, 12455.2381, 12560.0265, 12664.8148, 12769.6032, 12874.3915, 12979.1799, 13083.9683,
                   13188.7566, 13293.545, 13398.3333, 13503.1217, 13607.9101, 13712.6984, 13817.4868, 13922.2751,
                   14027.0635, 14131.8519, 14236.6402, 14341.4286, 14446.2169, 14551.0053, 14655.7937, 14760.582,
                   14865.3704, 14970.1587, 15074.9471, 15179.7354, 15284.5238, 15389.3122, 15494.1005, 15598.8889,
                   15703.6772, 15808.4656, 15913.254, 16018.0423, 16122.8307, 16227.619, 16332.4074, 16437.1958,
                   16541.9841, 16646.7725, 16751.5608, 16856.3492, 16961.1376, 17065.9259, 17170.7143, 17275.5026,
                   17380.291, 17485.0794, 17589.8677, 17694.6561, 17799.4444, 17904.2328, 18009.0212, 18113.8095,
                   18218.5979, 18323.3862, 18428.1746, 18532.963, 18637.7513, 18742.5397, 18847.328, 18952.1164,
                   19056.9048, 19161.6931, 19266.4815, 19371.2698, 19476.0582, 19580.8466, 19685.6349, 19790.4233,
                   19895.2116, 20000.0]

        steel.b = [0, 0.0764, 0.2463, 0.396, 0.5298, 0.6508, 0.7612, 0.8627, 0.9567, 1.0441, 1.0554, 1.1649, 1.1983,
                   1.2186, 1.2333, 1.2448, 1.2542, 1.2623, 1.2692, 1.2754, 1.2809, 1.2859, 1.2905, 1.2947, 1.2986,
                   1.3022, 1.3056, 1.3088, 1.3118, 1.3147, 1.3174, 1.32, 1.3224, 1.3248, 1.327, 1.3292, 1.3312, 1.3332,
                   1.3352, 1.337, 1.3388, 1.3406, 1.3422, 1.3439, 1.3454, 1.347, 1.3485, 1.3499, 1.3513, 1.3527, 1.3541,
                   1.3554, 1.3566, 1.3579, 1.3591, 1.3603, 1.3615, 1.3626, 1.3637, 1.3648, 1.3659, 1.3669, 1.368, 1.369,
                   1.37, 1.3709, 1.3719, 1.3728, 1.3738, 1.3747, 1.3756, 1.3764, 1.3773, 1.3781, 1.379, 1.3798, 1.3806,
                   1.3814, 1.3822, 1.383, 1.3837, 1.3845, 1.3852, 1.386, 1.3867, 1.3874, 1.3881, 1.3888, 1.3895, 1.3902,
                   1.3908, 1.3915, 1.3921, 1.3928, 1.3934, 1.394, 1.3947, 1.3953, 1.3959, 1.3965, 1.3971, 1.3977,
                   1.3982, 1.3988, 1.3994, 1.3999, 1.4005, 1.401, 1.4016, 1.4021, 1.4027, 1.4032, 1.4037, 1.4042,
                   1.4047, 1.4053, 1.4058, 1.4063, 1.4068, 1.4072, 1.4077, 1.4082, 1.4087, 1.4092, 1.4096, 1.4101,
                   1.4105, 1.411, 1.4115, 1.4119, 1.4123, 1.4128, 1.4132, 1.4137, 1.4141, 1.4145, 1.4149, 1.4154,
                   1.4158, 1.4162, 1.4166, 1.417, 1.4174, 1.4178, 1.4182, 1.4186, 1.419, 1.4194, 1.4198, 1.4202,
                   1.4205, 1.4209, 1.4213, 1.4217, 1.422, 1.4224, 1.4228, 1.4231, 1.4235, 1.4238, 1.4242, 1.4246,
                   1.4249, 1.4253, 1.4256, 1.4259, 1.4263, 1.4266, 1.427, 1.4273, 1.4276, 1.428, 1.4283, 1.4286,
                   1.4289, 1.4293, 1.4296, 1.4299, 1.4302, 1.4305, 1.4309, 1.4312, 1.4315, 1.4318, 1.4321, 1.4324,
                   1.4327, 1.433, 1.4333, 1.4336, 1.4339, 1.4342, 1.4345, 1.4348, 1.4351, 1.4353, 1.4356, 1.4359,
                   1.4362, 1.4365]

#         M36
#         steel.b = [0.000000, 0.050000, 0.100000, 0.150000, 0.200000, 0.250000, 0.300000, 0.350000, 0.400000, 0.450000,
#                    0.500000, 0.550000, 0.600000, 0.650000, 0.700000, 0.750000, 0.800000, 0.850000, 0.900000, 0.950000,
#                    1.000000, 1.050000, 1.100000, 1.150000, 1.200000, 1.250000, 1.300000, 1.350000, 1.400000, 1.450000,
#                    1.500000, 1.550000, 1.600000, 1.650000, 1.700000, 1.750000, 1.800000, 1.850000, 1.900000, 1.950000,
#                    2.000000, 2.050000, 2.100000, 2.150000, 2.200000, 2.250000, 2.300000]
#
#         steel.h = [0.000000, 19.398586, 29.611086, 36.311286, 41.398970, 45.654681, 49.463585, 53.042857, 56.529325,
#                    60.018492, 63.584024, 67.288555, 71.190394, 75.348316, 79.825601, 84.694101, 90.039004, 95.965085,
#                    102.605595, 110.135639, 118.793308, 128.914555, 140.993285, 155.789587, 174.533840, 199.329946,
#                    233.989035, 285.821861, 369.571626, 515.788276, 785.785104, 1282.793798, 2108.172454, 3257.880122,
#                    4726.442631, 6512.009401, 8720.265553, 11459.429229, 14887.904937, 19350.577348, 26042.602019,
#                    39200.400311, 65518.130312, 100476.654669, 136976.920182, 176029.817842, 215228.810312]

#         S235
#         steel.b = [0, 0.234653226, 0.830119516, 1.102702152, 1.16445836, 1.238611631, 1.312484886, 1.435233622,
#                    1.569004798, 1.677065435]
#
#         steel.h = [0, 531.3935876, 856.2118956, 1141.700714, 1284.826963, 1438.135604, 1704.150598, 2297.784057,
#                    3454.885639, 4960.479591]

#         A36
#         steel.b = [0.0000, 0.0974, 0.1949, 0.3004, 0.3343, 0.3609, 0.3900, 0.4110, 0.4354, 0.4609, 0.4895, 0.5102,
#                    0.5362, 0.5611, 0.5893, 0.6102, 0.6362, 0.6608, 0.6854, 0.7066, 0.7355, 0.7613, 0.7893, 0.8092,
#                    0.8344, 0.8596, 0.8826, 0.9015, 0.9230, 0.9433, 0.9640, 0.9857, 1.0048, 1.0309, 1.0556, 1.0780,
#                    1.0998, 1.1200, 1.1397, 1.1597, 1.1796, 1.1998, 1.2180, 1.2366, 1.2552, 1.2736, 1.2936, 1.3086,
#                    1.3265, 1.3433, 1.3597, 1.3764, 1.3946, 1.4072, 1.4219, 1.4357, 1.4495, 1.4633, 1.4771, 1.4920,
#                    1.5018, 1.5114, 1.5198, 1.5284, 1.5375, 1.5459, 1.5545, 1.5634, 1.5719, 1.5805, 1.5895, 1.5981,
#                    1.6048, 1.6119, 1.6188, 1.6256, 1.6325, 1.6393, 1.6462, 1.6529, 1.6591, 1.6630, 1.6733
# ]
#         steel.h = [0.0000, 119.4373, 177.5188, 221.0054, 241.0910, 251.9625, 265.3464, 277.0617, 287.0970, 299.6462,
#                    313.8689, 326.4229, 338.1333, 351.5214, 365.7444, 379.9749, 393.3619, 407.5887, 420.9770, 436.0455,
#                    453.6212, 470.3617, 487.9383, 504.6847, 521.4258, 539.8434, 555.7485, 571.6575, 590.0790, 608.5016,
#                    626.9239, 645.3451, 663.7690, 682.1858, 700.6040, 717.3479, 734.0924, 752.5152, 770.9384, 789.3614,
#                    807.7844, 826.2072, 844.6320, 863.0563, 881.4807, 899.9052, 918.3281, 936.7561, 955.1812, 973.6074,
#                    992.0339, 1010.4602, 1028.8849, 1047.3153, 1065.7436, 1084.1728, 1102.6020, 1121.0312, 1139.4604,
#                    1157.8884, 1176.3217, 1194.7550, 1213.1896, 1231.6240, 1250.0580, 1268.4925, 1286.9270, 1305.3610,
#                    1323.7956, 1342.2299, 1360.6640, 1379.0984, 1397.5347, 1415.9706, 1434.4067, 1452.8430, 1471.2791,
#                    1489.7153, 1508.1514, 1526.5877, 1545.0245, 1557.5954, 1582.7347]

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
        a01 = DirichletBoundaryCondition("a01", field_type="magnetic", magnetic_potential=0.0)
        a02 = DirichletBoundaryCondition("a02", field_type="magnetic", magnetic_potential=0.0)
        pbc1 = PeriodicBoundaryCondition("pbc1", field_type="magnetic")
        pbc2 = PeriodicBoundaryCondition("pbc2", field_type="magnetic")
        pbc3 = PeriodicBoundaryCondition("pbc3", field_type="magnetic")
        pbc4 = PeriodicBoundaryCondition("pbc4", field_type="magnetic")
        pbc5 = PeriodicBoundaryCondition("pbc5", field_type="magnetic")
        pbc6 = PeriodicBoundaryCondition("pbc6", field_type="magnetic")
        pbc7 = PeriodicBoundaryCondition("pbc7", field_type="magnetic")
        pbc8 = PeriodicBoundaryCondition("pbc8", field_type="magnetic")
        pbc9 = PeriodicBoundaryCondition("pbc9", field_type="magnetic")
        pbc10 = PeriodicBoundaryCondition("pbc10", field_type="magnetic")
        pbag = PeriodicAirGap("pbag", field_type="magnetic", outer_angle=self.rotor_angle + self.delta)

        # Adding boundary conditions to the snapshot
        self.snapshot.add_boundary_condition(a01)
        self.snapshot.add_boundary_condition(a02)
        self.snapshot.add_boundary_condition(pbc1)
        self.snapshot.add_boundary_condition(pbc2)
        self.snapshot.add_boundary_condition(pbc3)
        self.snapshot.add_boundary_condition(pbc4)
        self.snapshot.add_boundary_condition(pbc5)
        self.snapshot.add_boundary_condition(pbc6)
        self.snapshot.add_boundary_condition(pbc7)
        self.snapshot.add_boundary_condition(pbc8)
        self.snapshot.add_boundary_condition(pbc9)
        self.snapshot.add_boundary_condition(pbc10)
        self.snapshot.add_boundary_condition(pbag)

    def add_postprocessing(self):
        entities = [
                (0, 32)]
        # (0,50), (0,58), (0,-50), (0,-58), (-40,35), (40,35), (-40,-35), (40,-35), (-50,0), (-58,0), (50,0), (58,0),
        self.snapshot.add_postprocessing("integration", entities, "Torque")

    def build_model(self):

        model = ModelPiece('model')
        model.load_piece_from_dxf(ModelDir.RESOURCES / "SzESynRM_half_model_ag08mm.dxf")
        self.geom.merge_geometry(model.geom)

    def build_material(self):
        self.assign_material(*Node.from_polar(85, 90), "air_gap")
        self.assign_material(*Node.from_polar(75, 90), "air_gap")
        self.assign_material(*Node.from_polar(51, 90), "air_rot")
        self.assign_material(*Node.from_polar(59, 90), "air_rot")
        self.assign_material(*Node.from_polar(55, 45), "air_rot")
        self.assign_material(*Node.from_polar(55, 135), "air_rot")
        self.assign_material(*Node.from_polar(51, 1), "air_rot")
        self.assign_material(*Node.from_polar(59, 1), "air_rot")
        self.assign_material(*Node.from_polar(51, 179), "air_rot")
        self.assign_material(*Node.from_polar(59, 179), "air_rot")

        self.assign_material(0, 115, "steel_stator")
        self.assign_material(*Node.from_polar(35, 90), "steel_rotor")

        self.snapshot.add_geometry(self.geom)

    def build_coil(self):

        labels = ["U+", "U+", "U+", "V-", "V-", "V-", "V-", "W+", "W+", "W+", "W+",
                  "U-", "U-", "U-", "U-", "V+", "V+", "V+", "V+", "W-", "W-", "W-", "W-",
                  "U+", "U+", "U+", "U+", "V-", "V-", "V-", "V-", "W+", "W+", "W+", "W+",
                  "U-", "U-", "U-", "U-", "V+", "V+", "V+", "V+", "W-", "W-", "W-", "W-",
                  "U+", "U+", "U+", "U+", "V-", "V-", "V-", "V-", "W+", "W+", "W+", "W+",
                  "U-", "U-", "U-", "U-", "V+", "V+", "V+", "V+", "W-", "W-", "W-", "W-",
                  "U+", "U+", "U+", "U+", "V-", "V-", "V-", "V-", "W+", "W+", "W+", "W+",
                  "U-", "U-", "U-", "U-", "V+", "V+", "V+", "V+", "W-", "W-", "W-", "W-",
                  ]
        label = Node.from_polar(100, 172.5)
        for i in range(23):
             self.assign_material(label.x, label.y, labels[i])
             label = label.rotate(-pi / 4 / 6)

        labels = ["U+", "U+", "U+", "V-", "V-", "V-", "V-", "W+", "W+", "W+", "W+",
                  "U-", "U-", "U-", "U-", "V+", "V+", "V+", "V+", "W-", "W-", "W-", "W-",
                  "U+", "U+", "U+", "U+", "V-", "V-", "V-", "V-", "W+", "W+", "W+", "W+",
                  "U-", "U-", "U-", "U-", "V+", "V+", "V+", "V+", "W-", "W-", "W-", "W-",
                  "U+", "U+", "U+", "U+", "V-", "V-", "V-", "V-", "W+", "W+", "W+", "W+",
                  "U-", "U-", "U-", "U-", "V+", "V+", "V+", "V+", "W-", "W-", "W-", "W-",
                  "U+", "U+", "U+", "U+", "V-", "V-", "V-", "V-", "W+", "W+", "W+", "W+",
                  "U-", "U-", "U-", "U-", "V+", "V+", "V+", "V+", "W-", "W-", "W-", "W-",
                  ]
        label = Node.from_polar(90, 172.5)
        for i in range(23):
            self.assign_material(label.x, label.y, labels[i])
            label = label.rotate(-pi / 4 / 6)

        self.assign_material(Node.from_polar(90, 1).x, Node.from_polar(90, 1).y, "U+")
        self.assign_material(Node.from_polar(90, 179.5).x, Node.from_polar(90, 1).y, "U+")
        self.assign_material(Node.from_polar(100, 1).x, Node.from_polar(90, 1).y, "U+")
        self.assign_material(Node.from_polar(100, 179.5).x, Node.from_polar(90, 1).y, "U+")

        self.snapshot.add_geometry(self.geom)

    def build_boundary(self):

        self.assign_boundary_arc(*Node.from_polar(120, 45), "a01")
        self.assign_boundary_arc(*Node.from_polar(120, 135), "a02")
        self.assign_boundary(*Node.from_polar(112, 0), "pbc1")
        self.assign_boundary(*Node.from_polar(112, 180), "pbc1")
        self.assign_boundary(*Node.from_polar(102, 0), "pbc2")
        self.assign_boundary(*Node.from_polar(102, 180), "pbc2")
        self.assign_boundary(*Node.from_polar(92, 0), "pbc3")
        self.assign_boundary(*Node.from_polar(92, 180), "pbc3")
        self.assign_boundary(*Node.from_polar(85.5, 0), "pbc4")
        self.assign_boundary(*Node.from_polar(85.5, 180), "pbc4")
        self.assign_boundary(*Node.from_polar(75, 0), "pbc5")
        self.assign_boundary(*Node.from_polar(75, 180), "pbc5")
        self.assign_boundary(*Node.from_polar(62, 0), "pbc6")
        self.assign_boundary(*Node.from_polar(62, 180), "pbc6")
        self.assign_boundary(*Node.from_polar(59, 0), "pbc7")
        self.assign_boundary(*Node.from_polar(59, 180), "pbc7")
        self.assign_boundary(*Node.from_polar(55, 0), "pbc8")
        self.assign_boundary(*Node.from_polar(55, 180), "pbc8")
        self.assign_boundary(*Node.from_polar(50, 0), "pbc9")
        self.assign_boundary(*Node.from_polar(50, 180), "pbc9")
        self.assign_boundary(*Node.from_polar(30, 0), "pbc10")
        self.assign_boundary(*Node.from_polar(30, 180), "pbc10")
        self.assign_boundary_arc(*Node.from_polar(84.55, 90), "pbag")
        self.assign_boundary_arc(*Node.from_polar(84.95, 90), "pbag")

        self.snapshot.add_geometry(self.geom)

    def build_geometry(self):

            self.build_model()
            self.build_material()
            self.build_coil()
            self.build_boundary()
            self.snapshot.add_geometry(self.geom)

if __name__ == "__main__":
    m = SzEReluctanceMotorHalf(exportname="dev")
    print(m(cleanup=True, devmode=True))
