#!/usr/bin/env python

import colorsys, hashlib, random
import pipeline

class Strobe(pipeline.Shader):
    def __init__(self):
        self.main_color = colorsys.hsv_to_rgb(random.random(), 1, 1)
        self.reset()
        
    def reset(self):
        self.secondary_color = self.main_color
        self.main_color = colorsys.hsv_to_rgb(random.random(), 1, 1)
        self.range_low = (random.randint(0, 3)*12)
        self.time = 20
        
    def pre_frame(self, tick, pixels):
        self.time -=1
        if self.time < 0:
            self.reset()

    def fragment(self, tick, pixel):
        if self.range_low <= pixel.strip_offset < (self.range_low + 12):
            pixel.color = self.main_color
        else:
            pixel.color = self.secondary_color

class Spin(pipeline.Shader):
    def __init__(self):
        self.current_strip = 0
        self.reset()

    def reset(self):
        self.color = (1, 1, 1)
        self.current_strip = (self.current_strip + 1) % pipeline.strips
        self.time = 20 / pipeline.strips

    def pre_frame(self, tick, pixels):
        self.time -= 1
        if self.time < 0:
            self.reset()

    def fragment(self, tick, pixel):
        if pixel.strip == self.current_strip:
            return
        def compute_color(i):
            return pixel.color[i]*.7
        pixel.color = tuple(compute_color(c) for c in xrange(3))

ourPipeline = [Strobe(), Spin()]

if __name__ ==  '__main__':
    pipeline.run(pipeline.pixels, ourPipeline, .01)
