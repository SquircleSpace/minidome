#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import colorsys, hashlib, random
import pipeline

def randomish(thing):
        hash_str = hashlib.md5(str(thing)).hexdigest()
        return int(hash_str, 16)

class Cycle(pipeline.Shader):
        def __init__(self):
                self.target_strip = 0
                self.color = (1, 1, 1)

        def pre_frame(self, tick):
                fade_progress = tick % 60
                fade_distance = fade_progress / 59.0
                if fade_progress == 0:
                        self.target_strip = randomish(tick) % pipeline.strips
                        self.color = colorsys.hsv_to_rgb(random.random(), .25, 1)
                self.strength = 1 - fade_distance

        def fragment(self, tick, pixel):
                if pixel.strip != self.target_strip:
                        return
                def compute_color(i):
                        flash_part = self.color[i] * self.strength
                        base_part = pixel.color[i] * (1 - self.strength)
                        return flash_part + base_part
                pixel.color = tuple((compute_color(c) for c in xrange(3)))

class Raindrop(pipeline.Shader):
        def __init__(self):
                self.strip = random.randint(0, pipeline.strips - 1)
                self.position = random.randint(0, pipeline.strip_length - 1)
                self.color = colorsys.hsv_to_rgb(random.random(), .1, .5)

        def pre_frame(self, tick):
                self.position += 1
                if self.position == pipeline.strip_length:
                        self.strip = random.randint(0, pipeline.strips - 1)
                        self.position = 0
                        self.color = colorsys.hsv_to_rgb(random.random(), .2, .5)

        def fragment(self, tick, pixel):
                if pixel.strip != self.strip:
                        return

                if pixel.strip_offset != self.position:
                        return

                pixel.color = self.color

def sky(tick, pixel):
        base_color = (.1, .1, .15)
        pixel.color = base_color

class Lightning(pipeline.Shader):
        def __init__(self):
                self.reset()

        def reset(self):
                self.strip = random.randint(0, pipeline.strips - 1)
                self.color = colorsys.hsv_to_rgb(random.random(), .4, 4)
                self.strength = 0
                self.delay = random.randint(61, 500)

        def pre_frame(self, tick):
                self.delay -= 1
                if self.delay < 0:
                        self.reset()
                if self.delay >= 60:
                        self.strength = 0
                        return

                fade_progress = self.delay
                fade_distance = fade_progress / 59.0
                self.strength = fade_distance

        def fragment(self, tick, pixel):
                if pixel.strip != self.strip:
                        return
                def compute_color(i):
                        flash_part = self.color[i] * self.strength
                        base_part = pixel.color[i] * (1 - self.strength)
                        return flash_part + base_part
                pixel.color = tuple((compute_color(c) for c in xrange(3)))

ourPipeline = [pipeline.Fragment(sky)] + [Raindrop() for x in xrange(50)] + [Lightning()]

if __name__ == '__main__':
        pipeline.run(pipeline.pixels, ourPipeline, .03)
