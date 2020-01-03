from controller import *
import time
from math import floor
import argparse
import signal
import time
from constants import *
"""
    To parse device option passed to command line, enter in device names (bed, window, shelf, etc)
    followed by an list consisting of their address. If you have a 'scene' like a bedroom consisting
    of multiple devices, enter them all into the list.
    Include 'all' as a list of all of your device addresses as well.
"""
name_addr_dict = {

}

ps = argparse.ArgumentParser(description="Govee Home Control Script")

device_choices = device_names.append("all")
ps.add_argument('mode')
ps.add_argument('--device', default="all", type=str, choices=device_choices)
ps.add_argument('--brightness', type=int)
ps.add_argument('--color', nargs=3, type=int)
ps.add_argument('--period', type=float)
args = ps.parse_args()
chosen_devices = name_addr_dict[args.device]
if args.mode == "set":
    if args.brightness is not None:
        bright = args.brightness
        for device in chosen_devices:
            change_brightness(bright, device)
    if args.color is not None:
        colort = tuple(args.color)
        for device in chosen_devices:
            change_color(colort, device)
elif args.mode == "strobe":
    latency = args.period
    change_brightness_both(255)
    while True:
        for addr in chosen_devices:
            change_color(gen_rand_color(), addr)
        time.sleep(latency)
if args.mode == "wakeup":
    """
    This is the wakeup mode I have set, since I have LED's on my bed and window. 
    I have them set to blue and white respectively, with brightness increasing over 20 minutes.
    You can alter this in whatever way you want, or keep mine if you like it and have similarly
    named devices.
    """
    change_brightness_both(0)
    change_color((0,0,255), bed_address)
    change_color((255,255,255), window_address)
    cur_bright_percent = 0
    while cur_bright_percent < 100:
        now = time.time()
        cur_bright_percent += 5
        bright = floor(cur_bright_percent * 255/100)
        change_brightness(bright, bed_address)
        change_brightness(bright, window_address)
        next_t = now + 60
        time.sleep(next_t - time.time())


