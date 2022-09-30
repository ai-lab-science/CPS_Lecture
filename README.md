# CPS Lecture Repository
Code samples for [190.002] Cyber-Physical Systems Lab

## Required Packages
The following software packages are necessary to use the ZMQ API and to generate
motion data for the simulation of the Franka Panda robot in CoppeliaSim:
```bash
$ python -m pip install pyzmq
$ python -m pip install cbor
$ python -m pip install numpy
```

## CoppeliaSim Download
The sample code works only with CoppeliaSim version >=V4.4 rev0. The latest versions of CoppeliaSim 
can be downloaded from the website https://www.coppeliarobotics.com/downloads.

## Usage of the provided code
First CoppeliaSim is started, depending on the operating system,
the program can be executed either via the terminal (Ubuntu) or the .exe (Windows).
For Ubuntu, navigate to the unzipped folder provided by the download page and 
execute the following command in the terminal:
```bash
$ ./coppeliaSim.sh
```
After the start you open the simulation file "scene_with_panda.ttt"
in CoppeliaSim using the menu bar under File>OpenScene. 
All further steps can be done from now on in Pycharm or other IDEs with Python.

## Types of movement and how to perform them
In the current version it is possible to distinguish between two basic types, 
both of which have two additional subtypes. On the one hand the joints can be controlled
directly or on the other hand the pose (position and orientation) of the end effector. 
With the subtypes it is possible to select whether whole trajectories are to be moved
by the simulation or the simulated robot moves only to an end point.

### Joint space trajectories
To run a joint trajectory the following message is sent to CoppeliaSim using the ZMQ API.
 For this purpose a dictonary is generated in Python with the following entries:
```python
movementData = {
    'id': 'movSeq1',
    'control': 'joint',
    'type': 'pts',
    'times': times,
    'j1': j1, 'j2': j2, 'j3': j3, 'j4': j4, 'j5': j5, 'j6': j6
}

sim.callScriptFunction('remoteApi_movementDataFunction', scriptHandle, movementData)
```
Only the id can be changed directly in this message. The variables "times" and "j1", "j2",
etc. are set before the message generation. In these variables the trajectories 
of the joints are deposited, it is important that all must be of the type array
and have the same length. Of course you can calculate these arrays for example with 
a numpy array, but at the end the numpy array must be converted into a normal python array. 

### Joint space point to point movement
For the point-to-point movement in joint space, not only the joint angles
at the end point must be specified, but also the joint velocity and the maximum velocity,
acceleration and jerk values for the movement must be defined. 
The maximum values should not exceed the limits of the robot, 
but they can be reduced to avoid too fast movements.

```python
targetVel = [0, 0, 0, 0, 0, 0, 0]
movementData = {
    'id': 'movSeq3',
    'control': 'joint',
    'type': 'mov',
    'targetConfig': initialConfig,
    'targetVel': targetVel,
    'jointMaxVel': jointMaxVel,
    'jointMaxAccel': jointMaxAccel,
    'jointMaxJerk': jointMaxJerk
}
sim.callScriptFunction('remoteApi_movementDataFunction', scriptHandle, movementData)
```

### Inverse kinematics trajcetories
Similar to the joint space trajectories, complete arrays with all trajectory
data are again sent to the simulation. This time, however, the pose of the
end effector is described instead of the joint angles.
The pose is composed of the position, i.e. the x, y, z values of the end effector,
as well as the orientation, which in this case is described by quatanions.
Quatanions are a method for describing spatial orientations,
which are defined by x, y, z and w. They are the spatial extension of the plane
orientation by complex numbers.
```python
movementData = {
    'id': 'movSeq1',
    'type': 'pts',
    'times': times,
    'x': x, 'y': y, 'z': z,
    'qx': qx, 'qy': qy, 'qz': qz, 'qw': qw
}
sim.callScriptFunction('remoteApi_movementDataFunction',scriptHandle,movementData)
```


### Inverse kinematics point to point movement
Finally, point-to-point movements can also be performed using inverse kinematics.
For this movement, similar to the joint space point to point movement, 
the final pose of the end effector is defined as well as the maximum velocity,
acceleration and jerk. 


```python
movementData = {
    'id': 'movSeq2',
    'control': 'ik',
    'type': 'mov',
    'targetPose': targetPose,
    'cartesianMaxVel': cartesianMaxVel,
    'cartesianMaxAccel': cartesianMaxAccel,
    'cartesianMaxJerk': cartesianMaxJerk
}
sim.callScriptFunction('remoteApi_movementDataFunction', scriptHandle, movementData)
```

In summary, two message outputs decide the type of motion namely control (ik or joint) 
and type (mov or pts) about the motion the robot should perform in the simulation. 
Furthermore, depending on the type of movement, additional information must be provided.

### Execute the movement
So far, only the motion data has been sent to the simulation,
but it still needs to be executed.
For this the remoteApi function "remoteApi_executeMovement" must be called.
When all movements have been sent, the simulation should run until the last movement 
is completed, which is checked by the "waitForMovementExecuted" function. 

```python
sim.callScriptFunction('remoteApi_executeMovement', scriptHandle, 'movSeq1')
waitForMovementExecuted('movSeq1')
```

## Sensing joint angles or pose of the endeffector
To record joint angles or the pose of the end effector,
two functions were created in the simulation file which can be called
cyclically in the Python script. For this only the argument of the
callScriptFunction must be changed. In the following both possibilities are given:

```python
time, data = sim.callScriptFunction('remoteApi_getJointData', scriptHandle)
time, data = sim.callScriptFunction('remoteApi_getPoseData', scriptHandle)
```

The recorded data is stored in the numpy array "sensed_data", which saves the
simulation time in the first row and the joint angle or pose in the remaining rows.