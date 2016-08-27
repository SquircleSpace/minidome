#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import colorsys, hashlib, random
import pipeline

def rainbow(tick, pixel_info):
        cycle = (tick % 200.0) / 199.0
        hue = (cycle + pixel_info.distance) % 1.0
        rgb = colorsys.hsv_to_rgb(hue, 1, 1)
        pixel_info.color = rgb

class Ascend(pipeline.Shader):
        def __init__(self, frequency, strictness):
                self.frequency = frequency
                self.strictness = strictness
                self.offset = random.randint(0, frequency - 1)

        def fragment(self, tick, pixel_info):
                tick += self.offset
	        ascension = tick / self.frequency
	        ascension_progress = (tick % self.frequency) / 20.0
	        if ascension_progress > 1:
	                return
	        inv_distance = 1 - pixel_info.distance
	        if abs(inv_distance - ascension_progress) < self.strictness:
	                pixel_info.color = (1.0, 1.0, 1.0)

class Laser(pipeline.Shader):
        def __init__(self):
                self.random = random.randint(0, 313)
                self.down = random.randint(0, 1) == 1
                self.speed = random.randint(200, 500)

        def pre_frame(self, tick, pixels):
                tick += self.random
                self.laser_number = tick / self.speed
                self.laser_progress = (tick % self.speed) / 61.0
                hashed_strip = int(hashlib.md5(str(self.laser_number)).hexdigest(), 16)
                self.target_strip = (hashed_strip + self.random) % pipeline.strips
                self.down = int(hashlib.md5(str(self.laser_number + self.random)).hexdigest(), 16) % 2 == 1

        def fragment(self, tick, pixel_info):
                if self.laser_progress > 2:
	                return
	        if pixel_info.strip != self.target_strip:
	                return
	        color = colorsys.hsv_to_rgb((tick % 256) / 255.0, 1, 1)

                if self.laser_progress <= 1:
                        laser_progress = self.laser_progress
	        else:
	                laser_progress = 1 - (self.laser_progress - 1)
                if self.down:
                        pixel_distance = pixel_info.distance
                else:
                        pixel_distance = 1 - pixel_info.distance

                if pixel_distance <= laser_progress:
                        pixel_info.color = color

ourPipeline = [pipeline.Fragment(rainbow), Laser(), Laser(), Laser(), Ascend(2000, .01)]

if __name__ == '__main__':
        pipeline.run(pipeline.pixels, ourPipeline, .03)
