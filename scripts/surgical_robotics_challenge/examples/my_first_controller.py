from surgical_robotics_challenge.simulation_manager import SimulationManager
from surgical_robotics_challenge.psm_arm import PSM
from PyKDL import Frame, Rotation, Vector
import numpy as np
import time

# 1. Connect to the already-running simulator over ROS
sm = SimulationManager('my_first_controller')
psm1 = PSM(sm, 'psm1')

# 2. Define two Cartesian targets for the tip, w.r.t PSM1's own base frame.
#    Rotation.RPY(roll, pitch, yaw) in radians, Vector(x, y, z) in meters.
#    pi radians of roll + a small yaw is the "tool pointing down" orientation
#    this arm rests in by default (see the pose we printed above).
pose_a = Frame(Rotation.RPY(np.pi, 0, 0), Vector(0.02, 0.02, -0.12))
pose_b = Frame(Rotation.RPY(np.pi, 0, 0), Vector(-0.02, -0.02, -0.08))

# 3. Move smoothly between them using the built-in interpolated mover.
#    NOTE: move_cp/move_jp launch the trajectory in a background thread and
#    return immediately, so we must sleep for at least execute_time ourselves
#    before issuing the next command, or it'll cut the motion off early.
execute_time = 2.0

print("Moving to pose A...")
psm1.move_cp(pose_a, execute_time=execute_time, control_rate=120)
time.sleep(execute_time + 0.2)

print("Closing jaw...")
psm1.set_jaw_angle(0.0)
time.sleep(1.0)

print("Moving to pose B...")
psm1.move_cp(pose_b, execute_time=execute_time, control_rate=120)
time.sleep(execute_time + 0.2)

print("Opening jaw...")
psm1.set_jaw_angle(0.8)
time.sleep(1.0)

print("Done. Final tip pose:")
print(psm1.measured_cp())
