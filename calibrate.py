#!/usr/bin/env python

import pipeline
import colorsys, hashlib, random

def calibration(tick, pixel):
        if pixel.strip_offset == pipeline.strip_length - 1:
                base_color = (1, 1, 1)
        elif pixel.strip_offset == 0:
                base_color = colorsys.hsv_to_rgb(pixel.strip / float(pipeline.strips), 0.25, 1)
        elif pixel.strip_offset % 10 == 0:
                base_color = colorsys.hsv_to_rgb(pixel.strip / float(pipeline.strips), 1, 1)
        else:
                base_color = colorsys.hsv_to_rgb(pixel.strip / float(pipeline.strips), 0,5, 1)
        pixel.color = base_color

ourPipeline = [pipeline.Fragment(calibration)]

if __name__ == '__main__':
        pipeline.run(pipeline.pixels, ourPipeline, 20)
