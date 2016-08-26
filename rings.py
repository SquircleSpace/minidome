#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import colorsys, hashlib, random
import pipeline

def clear(tick, pixel):
        pixel.color = tuple((c * .5 for c in pixel.color))

class Ring(pipeline.Shader):
        def __init__(self):
                self.random = random.randint(1, 500)
                self.countdown = self.random

        def reset(self):
                top = random.randint(0, 1) == 0
                if top:
                        self.position = 0
                        self.direction = 1
                else:
                        self.position = pipeline.strip_length - 1
                        self.direction = -1
                self.color = colorsys.hsv_to_rgb(random.random(), 1, 1)

        def pre_frame(self, tick):
                if self.countdown > 0:
                        self.countdown -= 1
                        return
                elif self.countdown == 0:
                        self.countdown -= 1
                        self.reset()

        def fragment(self, tick, pixel):
                if self.countdown >= 0:
                        return
                if pixel.strip_offset == self.position:
                        pixel.color = self.color

        def post_frame(self, tick):
                if self.countdown < 0:
                        self.position += self.direction
                        if self.position < 0 or self.position >= pipeline.strip_length:
                                self.reset()

ourPipeline = [pipeline.Fragment(clear)] + [Ring() for x in xrange(10)]

if __name__ == '__main__':
        pipeline.run(pipeline.pixels, ourPipeline, .03)
