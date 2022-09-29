# Make sure to have CoppeliaSim running, with followig scene loaded:
#
# scenes/messaging/ikMovementViaRemoteApi.ttt
#
# Do not launch simulation, instead run this script

from zmqRemoteApi import RemoteAPIClient

print('Program started')

client = RemoteAPIClient()
sim = client.getObject('sim')

executedMovId = 'notReady'
targetArm = '/Franka'
stringSignalName = targetArm + '_executedMovId'
objHandle = sim.getObject(targetArm)
scriptHandle = sim.getScript(sim.scripttype_childscript, objHandle)


def waitForMovementExecuted(id_):
    global executedMovId, stringSignalName
    while executedMovId != id_:
        s = sim.getStringSignal(stringSignalName)
        executedMovId = s


# Set-up some movement variables:
cartesianMaxVel = 0.1
cartesianMaxAccel = 0.01
cartesianMaxJerk = 80

# jointMaxVel = [2.1750, 2.1750, 2.1750, 2.1750, 2.6100, 2.6100, 2.6100]
jointMaxVel = [2.1750 / 4, 2.1750 / 4, 2.1750 / 4, 2.1750 / 4, 2.6100 / 4, 2.6100 / 4, 2.6100 / 4]
jointMaxAccel = [15, 7.5, 10, 12.5, 15, 20, 20]
jointMaxJerk = [87, 87, 87, 87, 12, 12, 12]

# Start simulation:
sim.startSimulation()

# Wait until ready:
waitForMovementExecuted('ready')

# Get initial pose:
initialPose, initialConfig = sim.callScriptFunction('remoteApi_getPoseAndConfig', scriptHandle)

# Send first movement sequence:
targetPose = [1., 0.3, 1.2, 0, 0, 0, 1]
movementData = {
    'id': 'movSeq1',
    'control': 'ik',
    'type': 'mov',
    'targetPose': targetPose,
    'cartesianMaxVel': cartesianMaxVel,
    'cartesianMaxAccel': cartesianMaxAccel,
    'cartesianMaxJerk': cartesianMaxJerk
}
sim.callScriptFunction('remoteApi_movementDataFunction', scriptHandle, movementData)

# Execute first movement sequence:
sim.callScriptFunction('remoteApi_executeMovement', scriptHandle, 'movSeq1')

# Wait until above movement sequence finished executing:
waitForMovementExecuted('movSeq1')

# Send second and third movement sequence, where third one should execute
# immediately after the second one:
targetPose = [
    1., 0.3, 1.2,
    -0.7071068883, -6.252754758e-08, -8.940695295e-08, -0.7071067691
]
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

# Execute second and third movement sequence:
sim.callScriptFunction('remoteApi_executeMovement', scriptHandle, 'movSeq2')
sim.callScriptFunction('remoteApi_executeMovement', scriptHandle, 'movSeq3')

# Wait until above 2 movement sequences finished executing:
waitForMovementExecuted('movSeq3')

sim.stopSimulation()

print('Program ended')