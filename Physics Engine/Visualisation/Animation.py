import pygame
from .Projection import Cameraframe
import numpy as np

class Animation:
    def __init__(self, simulation, dt, boundaries):
        self.simulation = simulation
        self.dt = dt
        self.boundaries = boundaries
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption('Physics Engine')
        self.running = True
        self.clock = pygame.time.Clock()
        self.bodies2D = []
        self.projected_size = []
        self.orientation = [0, 0]


        self.camera_distance = 300
        self.mouse_zoom_step = 10.0
        self.mouse_rotation_sensitivity = 0.35
        self.rotating_with_mouse = False
        self.cameraframe = Cameraframe(self.camera_distance, self.orientation)


    def update(self):
        bodies = self.simulation()
        self.bodies2D = []
        self.projected_size = []
        self.cameraframe = Cameraframe(self.camera_distance, self.orientation)


        for body in bodies:
            projection = self.cameraframe.project(body)
            if projection is not None:
                position, size = projection
                self.bodies2D.append(position)
                self.projected_size.append(size)

    def boundary_edges(self):
        edges = []
        for boundary in self.boundaries:
            if boundary.get("type") != "cube":
                continue

            size = boundary["size"]
            corners = [
                np.array([x, y, z], dtype=float)
                for x in (-size, size)
                for y in (-size, size)
                for z in (-size, size)
            ]
            pairs = (
                (0, 1), (0, 2), (0, 4),
                (1, 3), (1, 5), (2, 3),
                (2, 6), (3, 7), (4, 5),
                (4, 6), (5, 7), (6, 7),
            )

            for start, end in pairs:
                projected_start = self.cameraframe.project_point(corners[start])
                projected_end = self.cameraframe.project_point(corners[end])
                if projected_start is not None and projected_end is not None:
                    edges.append((projected_start, projected_end))

        return edges


    def move_camera(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            self.rotating_with_mouse = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            self.rotating_with_mouse = False
        elif event.type == pygame.MOUSEWHEEL:
            self.camera_distance = max(
                10,
                self.camera_distance - event.y * self.mouse_zoom_step,
            )
        elif event.type == pygame.MOUSEMOTION and self.rotating_with_mouse:
            horizontal, vertical = event.rel
            sensitivity = self.mouse_rotation_sensitivity
            self.orientation[0] -= vertical * sensitivity
            self.orientation[1] += horizontal * sensitivity

        return

    def loop(self):

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else: 
                    self.move_camera(event)

            self.update()   
            self.screen.fill((0, 0, 0))

            screen_center = np.array((self.screen.get_width() // 2, self.screen.get_height() // 2))
            for start, end in self.boundary_edges():
                start = tuple((start + screen_center).astype(int))
                end = tuple((end + screen_center).astype(int))
                pygame.draw.line(self.screen, (70, 120, 180), start, end, 1)

            for i in range(len(self.bodies2D)):
                position = self.bodies2D[i] + (self.screen.get_width() // 2, self.screen.get_height() // 2)
                pygame.draw.circle(self.screen, (255, 255, 255), position, self.projected_size[i])

            pygame.display.flip()
            self.clock.tick(round(1 / self.dt))
        pygame.quit()
    