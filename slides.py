#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import colorsys, hashlib, random
import pipeline

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
	        color = colorsys.hsv_to_rgb(((tick + self.random) % 600) / 599.0, 1, 1)

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

ourPipeline = [Laser(), Laser(), Laser(), Laser(), Laser(), Laser()]

if __name__ == '__main__':
        pipeline.run(pipeline.pixels, ourPipeline, .03)
