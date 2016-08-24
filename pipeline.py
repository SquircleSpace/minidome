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

def run(pixels, pipeline, sleep_time=.01):
        tick = 0
        while True:
                tick += 1
                run_pipeline(pixels, pipeline, tick)
                if simulate:
                        draw_into_buffer(pixels, simulation)
                        cv2.imshow('simulation', simulation)
                        print pixels[0].color
                        cv2.waitKey()
                else:
                        client.put_pixels(convert_to_opc(pixels))
                time.sleep(sleep_time)
