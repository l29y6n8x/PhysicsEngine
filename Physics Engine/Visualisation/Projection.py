import numpy as np 

class Cameraframe:
    def __init__(self, camera_position, orientation):
        self.c_position = camera_position
        self.c_orientation = orientation
        
        self.focal_length = 400.0

        self.theta = np.radians(self.c_orientation[0])
        self.phi = np.radians(self.c_orientation[1])

        self.camera_normal = np.array([np.cos(self.theta) * np.cos(self.phi), np.cos(self.theta) * np.sin(self.phi), -np.sin(self.theta)])

    def rotation_matrix(self, angle_a, angle_b):
        a = angle_a
        b = angle_b
        
        self.matrix_theta = np.array([[np.cos(a), 0, -np.sin(a)], 
                                      [0, 1, 0], 
                                      [np.sin(a), 0, np.cos(a)]])
        
        self.matrix_phi = np.array([[np.cos(b), np.sin(b), 0], 
                                    [-np.sin(b), np.cos(b), 0], 
                                    [0, 0, 1]])

    def change_frame(self):
        point = self.body_position - self.c_position
        #print(self.camera_normal, self.c_position)
          
        if np.dot(point, self.camera_normal) < 0:
            return None
        else:
            self.rotation_matrix(self.theta, self.phi)
            distance = np.dot(point, self.camera_normal)
            point = self.matrix_theta @ self.matrix_phi @ point
            
            
            if distance == 0:
                return None
            size = float((self.focal_length / distance) * self.body_size)
            if size < 1:
                size = 1
            return point, size


    def project(self, body):
        self.body = body
        self.body_position = body.state[0]
        self.body_size = body.radius

        result = self.change_frame()
        if result is None:
            return None
        point, size = result
        if point.shape != (3,):
            return None

        #print(point)
        projection = np.array([self.focal_length * point[1] / point[0], self.focal_length * point[2] / point[0]])
        return projection, size