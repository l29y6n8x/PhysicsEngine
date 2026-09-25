import numpy as np 

class Cameraframe:
    def __init__(self, camera_distance, orientation):
        self.c_distance = camera_distance

        self.qy = np.array([np.cos(np.radians(orientation[0] / 2)), 0, np.sin(np.radians(orientation[0] / 2)), 0])
        self.qz = np.array([np.cos(np.radians(orientation[1] / 2)), 0, 0, np.sin(np.radians(orientation[1] / 2))])
        
        self.focal_length = 400.0
        
           

    def q_multiply(self, q1, q2):
        w1, x1, y1, z1 = q1
        w2, x2, y2, z2 = q2

        w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
        x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
        y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
        z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2

        return np.array([w, x, y, z])

    def q_conjugate(self, q):
        w, x, y, z = q
        return np.array([w, -x, -y, -z])

    def q_rotate(self, q, vector):
        p = np.array([0.0, vector[0], vector[1], vector[2]])

        p = self.q_multiply(q, p)
        p = self.q_multiply(p, self.q_conjugate(q))
        return p[1:]

    def frame_transform(self, point):
        return self.q_rotate(self.qy, self.q_rotate(self.qz, point))

    def frame_transform_inverse(self, point):
        return self.q_rotate(self.q_conjugate(self.qz), self.q_rotate(self.q_conjugate(self.qy), point))

    def change_frame(self):
        point = self.body_position - self.c_position
          
        if np.dot(point, self.camera_normal) < 0:
            return None
        else:
            self.point = self.frame_transform_inverse(point)
            distance = np.linalg.norm(point)
            
            
            if distance == 0:
                return None
            size = float((self.focal_length / distance) * self.body_size)
            if size < 1:
                size = 1
            return size


    def project(self, body):
        self.body = body
        self.body_position = body.state[0]
        self.body_size = body.radius

        self.camera_normal = self.frame_transform(np.array([-1, 0, 0]))
        self.c_position = -self.camera_normal * self.c_distance

        

        result = self.change_frame()
        if result is None:
            return None
        size = result
        if self.point.shape != (3,):
            return None

        
        projection = np.array([self.focal_length * self.point[1] / self.point[0], self.focal_length * self.point[2] / self.point[0]])
        return projection, size

    def project_point(self, point):
        camera_normal = self.frame_transform(np.array([-1, 0, 0]))
        camera_position = -camera_normal * self.c_distance
        relative_point = np.asarray(point, dtype=float) - camera_position

        if np.dot(relative_point, camera_normal) < 0:
            return None

        frame_point = self.frame_transform_inverse(relative_point)
        if np.isclose(frame_point[0], 0.0):
            return None

        return np.array([
            self.focal_length * frame_point[1] / frame_point[0],
            self.focal_length * frame_point[2] / frame_point[0],
        ])