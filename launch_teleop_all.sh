#!/bin/bash
# Opens one gnome-terminal window with 3 tabs: AMBF sim, dvrk_system, MTM/PSM teleop.
# Each tab stays open after its command exits/crashes so you can read error output.

AMBF_DIR="$HOME/surgical_robotics_challenge"
TELEOP_DIR="$HOME/surgical_robotics_challenge/scripts/surgical_robotics_challenge/teleoperation"
DVRK_JSON="$HOME/ros2_ws/src/dvrk/dvrk_config_jhu/jhu-dVRK/system-MTML-MTMR.json"
VENV_ACTIVATE="$HOME/venv_src/bin/activate"

gnome-terminal \
  --tab --title="ambf-sim" -- bash -c "
    cd '$AMBF_DIR'
    ./run_env_3D_MED_COMPLEX_LND_420006.sh
    echo; echo '[ambf-sim exited, press enter to close]'; read
    exec bash" \
  --tab --title="dvrk-system" -- bash -c "
    sleep 5
    ros2 run dvrk_robot dvrk_system -j '$DVRK_JSON'
    echo; echo '[dvrk_system exited, press enter to close]'; read
    exec bash" \
  --tab --title="mtm-teleop" -- bash -c "
    sleep 12
    source '$VENV_ACTIVATE'
    cd '$TELEOP_DIR'
    ./mtm_psm_pair_teleop_420006.sh
    echo; echo '[mtm-teleop exited, press enter to close]'; read
    exec bash"
