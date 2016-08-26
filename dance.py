#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import colorsys, hashlib, random
import pipeline

def clear(tick, pixel):
        pixel.color = tuple((c * .5 for c in pixel.color))

class Dancer(pipeline.Shader):
        def __init__(self, strip):
                self.position = random.randint(0, pipeline.strip_length - 1)
                self.strip = strip
                self.random = random.randint(0, 1000)
                down = random.randint(0, 1) == 1
                if down:
                        self.direction = 1
                else:
                        self.direction = -1

        def pre_frame(self, tick):
                self.position += self.direction
                if self.position >= pipeline.strip_length:
                        self.position = pipeline.strip_length
                        self.direction = -1
                elif self.position < 0:
                        self.position = 0
                        self.direction = 1

        def fragment(self, tick, pixel):
                if pixel.strip != self.strip:
                        return
                time = (tick + self.random) % 500
                if 10 < time <= 50:
                        pixel.color = self.colorful(tick, pixel)
                elif time <= 10 or time <= 60:
                        def mix(c1, m1, c2, m2):
                                parts = [0] * len(c1)
                                for i in xrange(len(c1)):
                                        parts[i] += c1[i] * m1
                                for i in xrange(len(c2)):
                                        parts[i] += c2[i] * m2
                                return tuple(parts)
                        white = self.boring(tick, pixel)
                        color = self.colorful(tick, pixel)
                        if time > 10:
                                time -= 50
                                mult = time/10.0
                                pixel.color = mix(white, mult, color, 1 - mult)
                        else:
                                mult = time/10.0
                                pixel.color = mix(white, 1 - mult, color, mult)
                else:
                        pixel.color = self.boring(tick, pixel)

        def boring(self, tick, pixel):
                if abs(pixel.strip_offset - self.position) > 5:
                        return (0, 0, 0)
                return (1, 1, 1)

        def colorful(self, tick, pixel):
                permitted_distance = 0
                permitted_distance += (tick + self.random) % 1000
                distance = abs(pixel.strip_offset - self.position)
                if distance > permitted_distance:
                        return (0, 0, 0)
                rainbow_distance = 55.0
                percent_distance = distance / rainbow_distance
                return colorsys.hsv_to_rgb(percent_distance, 1, 1)

ourPipeline = [pipeline.Fragment(clear)] + [Dancer(x) for x in xrange(5)]

if __name__ == '__main__':
        pipeline.run(pipeline.pixels, ourPipeline, .03)
