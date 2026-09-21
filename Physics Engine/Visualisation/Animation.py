import pygame
from .Projection import Cameraframe
import numpy as np

class Animation:
    def __init__(self, simulation, dt):
        self.simulation = simulation
        self.dt = dt
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption('Physics Engine')
        self.running = True
        self.clock = pygame.time.Clock()
        self.bodies2D = []
        self.projected_size = []
        self.position = np.array([-100.0, 0.0, 0.0])
        self.orientation = [0, 0]

        self.orientation = [0, 0]
        self.position = np.array([-100.0, 0.0, 0.0])
        self.camera_speed = 600.0
        self.rotation_speed = 90.0
        self.cameraframe = Cameraframe(self.position, self.orientation)


    def update(self):
        bodies = self.simulation()
        self.bodies2D = []
        self.projected_size = []
        self.cameraframe = Cameraframe(self.position, self.orientation)

        for body in bodies:
            projection = self.cameraframe.project(body)
            if projection is not None:
                position, size = projection
                self.bodies2D.append(position)
                self.projected_size.append(size)


    def move_camera(self):
        keys = pygame.key.get_pressed()
        distance = self.camera_speed * self.dt
        angle = self.rotation_speed * self.dt

        self.cameraframe.rotation_matrix(-np.radians(self.orientation[0]), -np.radians(self.orientation[1]))

        R = self.cameraframe.matrix_theta @ self.cameraframe.matrix_phi

        forward = R @ np.array([1, 0, 0])
        print(forward)
        right = R @ np.array([0, 1, 0])
        up = R @ np.array([0, 0, 1])

        if keys[pygame.K_w]:
            self.position += forward * distance
        if keys[pygame.K_s]:
            self.position -= forward * distance
        if keys[pygame.K_a]:
            self.position -= right * distance
        if keys[pygame.K_d]:
            self.position += right * distance
        if keys[pygame.K_SPACE]:
            self.position -= distance * up
        if keys[pygame.K_LSHIFT]:
            self.position += distance * up

        if keys[pygame.K_UP]:
            self.orientation[0] += angle
        if keys[pygame.K_DOWN]:
            self.orientation[0] -= angle
        if keys[pygame.K_LEFT]:
            self.orientation[1] -= angle
        if keys[pygame.K_RIGHT]:
            self.orientation[1] += angle

        

    def loop(self):

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.move_camera()
            self.update()
            self.screen.fill((0, 0, 0))

            for i in range(len(self.bodies2D)):
                position = self.bodies2D[i] + (self.screen.get_width() // 2, self.screen.get_height() // 2)
                pygame.draw.circle(self.screen, (255, 255, 255), position, self.projected_size[i])

            pygame.display.flip()
            self.clock.tick(round(1 / self.dt))
        pygame.quit()
    