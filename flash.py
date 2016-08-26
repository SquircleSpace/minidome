#!/usr/bin/env python

import colorsys, hashlib, random
import pipeline

class Flash(pipeline.Shader):
    def __init__(self):
        self.main_color = colorsys.hsv_to_rgb(random.random(), 1, 1)
        self.reset()

    def reset(self):
        self.secondary_color = self.main_color
        self.main_color = colorsys.hsv_to_rgb(random.random(), 1, 1)
        self.time = 105

    def pre_frame(self, tick):
        self.time -= 1
        if self.time < 0:
            self.reset()

    def fragment(self, tick, pixel):
        if (5 < self.time < 25):
            pixel.color = self.secondary_color
        elif (45 < self.time < 65):
            pixel.color = self.secondary_color
        elif (85 < self.time < 105):
            pixel.color = self.secondary_color
        else:
            pixel.color = self.main_color

ourPipeline = [Flash()]

if __name__ == '__main__':
    pipeline.run(pipeline.pixels, ourPipeline, .01)
