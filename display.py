import pygame as pg
import numpy as np
from math import pi, sin, cos


class PixelDisplay:
    def __init__(self, width, height, ASCII_character):
        self.width = width
        self.height = height
        self.screen = pg.display.set_mode((width, height))
        self.background = (10, 10, 60)
        self.pixelmatrix = None
        self.Ascii_character_list = ASCII_character[::-1]

    def display(self):
        self.screen.fill(self.background)
        for node_index in range(0, self.pixelmatrix.ExpandedMatrix.shape[0]):
            colour = (255, 255, 0)

            if(self.Ascii_character_list[node_index] == "M"):
                colour = (255, 255, 0)
            if(self.Ascii_character_list[node_index] == "d"):
                colour = (0, 255, 0)

            character = self.Ascii_character_list[node_index]
            self.text_surface = my_font.render(
                character, False, colour)
            node = self.pixelmatrix.ExpandedMatrix[node_index]
            if(node[1] > 0):
                self.screen.blit(self.text_surface, (WIDTH / 2 +
                                                     int(node[0]), HEIGHT / 2 + int(node[2])))

    def rotateAll(self, theta):

        node = self.pixelmatrix.ExpandedMatrix
        center = self.pixelmatrix.findCentre()

        c = np.cos(theta)
        s = np.sin(theta)

        # Rotating about Z - axis
        matrix = np.array([[c, -s, 0, 0],
                           [s, c, 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])

        self.pixelmatrix.rotate(center, matrix)


class LocationMatrix:
    def __init__(self, PreExpandedMatrix):
        bottomrow = np.zeros((0, 4))
        addoneTotheRight = np.hstack(
            (PreExpandedMatrix, np.ones((PreExpandedMatrix.shape[0], 1))))
        self.ExpandedMatrix = np.vstack((addoneTotheRight, bottomrow))

    def findCentre(self):
        mean = self.ExpandedMatrix.mean(axis=0) + 10
        return mean

    def rotate(self, center, rotational_matrix):
        for i, node in enumerate(self.ExpandedMatrix):
            self.ExpandedMatrix[i] = center + \
                np.matmul(rotational_matrix, node - center)


if __name__ == "__main__":
    clock = pg.time.Clock()
    FPS = 60

    spin = 0

    WIDTH = 800
    HEIGHT = 800
    ASCII_character_index_mapping = []
    with open('funnyemoji.txt', 'r') as file:
        data = [file.read().replace('\n', '')]
    row_count = 0
    column_count = 0

    for line in data:
        for character in line:
            ASCII_character_index_mapping.append(character)
    print(len(ASCII_character_index_mapping))
    MAP_HEIGHT = 67
    MAP_WIDTH = 143
    # MAP_HEIGHT = 34
    # MAP_WIDTH = 139
    pg.init()

    # this is to get the shpereical coord of the 2d image
    xyz = []

    R = 250
    my_font = pg.font.SysFont('arial', 14)

    for i in range(MAP_HEIGHT):
        lat = (pi / MAP_HEIGHT) * i
        for j in range(MAP_WIDTH):
            lon = (2 * pi / MAP_WIDTH) * j
            x = R * sin(lat) * cos(lon)
            y = R * sin(lat) * sin(lon)
            z = R * cos(lat)
            xyz.append((x, y, z))
    print(len(xyz))
    globle_pixel_matrix = np.array([i for i in xyz])

    running = True

    while running:

        clock.tick(FPS)

        # here is where we decide what to display
        # create a projected globle that contains the pixel location of each point

        PD = PixelDisplay(WIDTH, HEIGHT, ASCII_character_index_mapping)

        ContainerGlobe = LocationMatrix(globle_pixel_matrix)
        PD.pixelmatrix = ContainerGlobe
        PD.rotateAll(spin)
        PD.display()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        pg.display.update()
        spin += 0.05
