# -*- coding: utf-8 -*-

"""Pibooth plugin for extra lights management."""

import pibooth
from gpiozero import LEDBoard

import time
from rpi_ws281x import *
import argparse


__version__ = "2023.7.14.23"


LED_COUNT      = 60
LED_PIN        = 18
LED_FREQ_HZ    = 1000000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 255      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


@pibooth.hookimpl
def pibooth_configure(cfg):
    """Declare the new configuration options"""
    cfg.add_option('CONTROLS', 'flash_led_pin', 18,
                   "Physical GPIO OUT pin to light a LED when the capture is taken (list of pins accepted)")
    cfg.add_option('CONTROLS', 'leds_count', 60,
                   "Number of led")
    cfg.add_option('CONTROLS', 'flash_color', (127,127,127),
                   "If defined set color flash light")

@pibooth.hookimpl
def pibooth_startup(app, cfg):
    
    # Initial state
    app.led_startup.on()
    app.led_sequence.off()
    app.led_flash.off()
    app.flash_pin = cfg.getint('CONTROLS', 'flash_led_pin')
    app.leds_count = cfg.getint('CONTROLS', 'leds_count')

    
    app.flash_color = cfg.gettuple('CONTROLS', 'flash_color', 'color', 1)
    
    app.strip = Adafruit_NeoPixel(app.leds_count, app.flash_pin, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    app.strip.begin()

    flash_off(app)
    flash_on(app, (255, 0, 0))
    time.sleep(50/250.0)
    flash_on(app, (255, 127, 0))
    time.sleep((50/250.0))
    flash_on(app,(255, 255, 0))
    time.sleep((50/250.0))
    flash_on(app,(0, 255, 0))
    time.sleep((50/250.0))
    flash_on(app,(0, 0, 255))
    time.sleep((50/250.0))
    flash_on(app,(46, 43, 95))
    time.sleep((50/250.0))
    flash_on(app,(127, 127, 127))
    time.sleep((50/250.0))
    flash_off(app)



@pibooth.hookimpl
def state_preview_enter(app):
    """Start a new capture sequence."""
    app.led_sequence.on()
    flash_on(app,app.flash_color[0])

@pibooth.hookimpl
def state_capture_exit(app):
    """A capture has been taken."""
    flash_off(app)


@pibooth.hookimpl
def state_processing_enter(app):
    """The capture sequence is done."""
    app.led_sequence.off()

def flash_off(app):
    print("FLAH OFF")
    colorWipe(app.strip, Color(0,0,0))

def flash_on(app, colors):
    print("FLASH ON")
    print(colors)
    colorWipe(app.strip, Color(colors[0], colors[1], colors[2]))



def colorWipe(strip, color, wait_ms=50):
    print("SET FLASH")
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()