#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import opc, time, colorsys, hashlib, random
import numpy, cv2

numLEDs = 512
client = opc.Client('localhost:7890')

strip_length = 48
strips = 5

def convert_to_int_color(rgb):
        return tuple((int(255 * value) for value in rgb))

def convert_to_opc(pixels):
        return [convert_to_int_color(p.color) for p in pixels]

def offset_to_strip(offset):
        return offset / strip_length

def offset_to_distance(offset):
        part = offset % strip_length
        return part / float(strip_length - 1)

def offset_to_strip_offset(offset):
        return offset % strip_length

class PixelInfo(object):
        def __init__(self, offset, color):
                self.strip = offset_to_strip(offset)
                self.distance = offset_to_distance(offset)
                self.strip_offset = offset_to_strip_offset(offset)
                self.color = color

pixels = [PixelInfo(off, (0, 0, 0)) for off in xrange(strips * strip_length)]

class Shader(object):
        def fragment(self, tick, pixel_info):
                pass
        def pre_frame(self, tick):
                pass
        def post_frame(self, tick):
                pass

class Fragment(Shader):
        def __init__(self, fn):
                self.fn = fn

        def fragment(self, tick, pixel_info):
                self.fn(tick, pixel_info)

def rainbow(tick, pixel_info):
        cycle = (tick % 200.0) / 199.0
        hue = (cycle + pixel_info.distance) % 1.0
        rgb = colorsys.hsv_to_rgb(hue, 1, 1)
        pixel_info.color = rgb

def ascend(tick, pixel_info):
        ascension = tick / 2000
        ascension_progress = (tick % 2000) / 20.0
        if ascension_progress > 1:
                return
        inv_distance = 1 - pixel_info.distance
        if abs(inv_distance - ascension_progress) < .01:
                pixel_info.color = (1.0, 1.0, 1.0)

class Laser(Shader):
        def __init__(self):
                self.random = random.randint(0, 313)
                self.down = random.randint(0, 1) == 1
                self.speed = random.randint(200, 500)

        def pre_frame(self, tick):
                tick += self.random
                self.laser_number = tick / self.speed
                self.laser_progress = (tick % self.speed) / 61.0
                hashed_strip = int(hashlib.md5(str(self.laser_number)).hexdigest(), 16)
                self.target_strip = (hashed_strip + self.random) % strips
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

pipeline = [Fragment(rainbow), Laser(), Laser(), Laser(), Fragment(ascend)]

def run_pipeline(pixels, pipeline, tick):
        for shader in pipeline:
                shader.pre_frame(tick)
        for pixel in pixels:
                for shader in pipeline:
                        shader.fragment(tick, pixel)
        for shader in pipeline:
                shader.post_frame(tick)

def draw_into_buffer(pixels, buffer):
        for pixel in pixels:
                x = pixel.strip
                y = pixel.strip_offset
                rgb = convert_to_int_color(pixel.color)
                for channel in xrange(3):
                        buffer[x,y,channel] = rgb[channel]

simulate = False

if simulate:
        simulation = numpy.zeros((strips, strip_length, 3), numpy.uint8)

tick = 0
# while True:
#         tick += 1
#         run_pipeline(pixels, pipeline, tick)
#         if simulate:
#                 draw_into_buffer(pixels, simulation)
#                 cv2.imshow('simulation', simulation)
#                 print pixels[0].color
#                 cv2.waitKey()
#         else:
#                 client.put_pixels(convert_to_opc(pixels))
#         time.sleep(0.01)

while True:
        offset = input()
        pixels = [(0,0,0)] * (strips * strip_length)
        pixels[offset] = (255,255,255)
        client.put_pixels(pixels)
