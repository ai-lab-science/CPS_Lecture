from zmqRemoteApi import RemoteAPIClient
import numpy as np
import sys



class FrankaZMQ:
    def __init__(self, client=None):
        # client setup
        if client is None:
            self.client = RemoteAPIClient('localhost', 23000)
        else:
            self.client = client

        # Gets Sim Handle form CoppeliaSim
        self.sim = self.client.getObject('sim')

        #  Object handles of Base and Tip
        self._panda_base = self.sim.getObjectHandle('/Panda')
        self._panda_tip = self.sim.getObjectHandle('/Panda_tip')

        # Object handle of the joints
        self._panda_joints = []
        self._nr_joints = 7
        for i in range(1, self._nr_joints+1):
            _joint_name = '/Panda_joint' + str(i)
            self._panda_joints.append(self.sim.getObjectHandle(_joint_name))

    # region Setter and Getter
    @property
    def panda_joints(self):
        return self._panda_joints

    @property
    def get_joint_values(self):
        _angles = np.zeros((7, 1))
        for idx, i in enumerate(self.panda_joints):
            _angles[idx] = self.sim.getJointPosition(i)
        return _angles
    # endregion

    def set_joints_values(self, new_angles):
        if len(new_angles) == 7 or new_angles.size == 7:
            for i in range(self._nr_joints):
                _joint_handle = self.panda_joints[i]
                _angles_float = float(new_angles[i])
                self.sim.setJointPosition(_joint_handle, _angles_float)
        else:
            print('ERROR: new_angles have to be an array or numpy array with size 7!')
            sys.exit()

    def get_object_matrix(self, object_name, relative_frame=-1):
        _object_handle = self.sim.getObjectHandle(object_name)
        return np.array(self.sim.getObjectMatrix(_object_handle, relative_frame))






