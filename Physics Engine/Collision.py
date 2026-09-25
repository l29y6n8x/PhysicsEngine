import numpy as np



class collision:
    def __init__(self, body, object, type):
        self.type = type
        if type == "boundary":
            self.body = body
            self.object = object

        if type == "body":
            self.body1 = body
            self.body2 = object

        self.collision_occurred = False

    def check_collision(self):
        if self.type == "body":
            r = self.body2.state[0] - self.body1.state[0]
            distance = np.linalg.norm(r)
            if distance <= (self.body1.radius + self.body2.radius):
                self.resolve_body_collision()

        if self.type == "boundary":
            if self.object["type"] == "cube":
                for i in range(3):
                    if self.body.state[0][i] + self.body.radius >= self.object["size"] or self.body.state[0][i] - self.body.radius <= -self.object["size"]:
                        self.resolve_boundary_collision()
                        break

    def resolve_body_collision(self):

        p1 = self.body1.state[0]
        p2 = self.body2.state[0]

        v1 = self.body1.state[1]
        v2 = self.body2.state[1]

        m1 = self.body1.mass
        m2 = self.body2.mass

        difference = p2 - p1
        distance_value = np.linalg.norm(difference)

        if distance_value == 0:
            return

        normal = difference / distance_value

        v_relative = v2 - v1
        relative_normal_velocity = np.dot(v_relative, normal)

        # Körper bewegen sich bereits voneinander weg
        if relative_normal_velocity >= 0:
            return

        restitution = 1.0

        impulse = (
            -(1 + restitution) * relative_normal_velocity
            / (1 / m1 + 1 / m2)
        )

        J = impulse * normal

        self.body1.state[1] -= J / m1
        self.body2.state[1] += J / m2

        penetration_depth = (self.body1.radius + self.body2.radius) - distance_value
        correction = penetration_depth / (1 / m1 + 1 / m2) * normal

        self.body1.state[0] -= correction / m1
        self.body2.state[0] += correction / m2

    def resolve_boundary_collision(self):
        print("Boundary collision detected for body at position:", self.body.state[0])
        for i in range(3):
            if self.body.state[0][i] + self.body.radius >= self.object["size"]:
                if self.body.state[1][i] > 0:  
                    self.body.state[1][i] = -self.body.state[1][i]
                    penetration_depth = (self.body.state[0][i] - self.object["size"]) + self.body.radius
                    self.body.state[0][i] -= penetration_depth

            elif self.body.state[0][i] - self.body.radius <= -self.object["size"]:
                if self.body.state[1][i] < 0:
                    self.body.state[1][i] = -self.body.state[1][i] 
                    penetration_depth = (self.body.state[0][i] + self.object["size"]) - self.body.radius
                    print("Penetration depth:", penetration_depth)
                    self.body.state[0][i] += -penetration_depth

        
