from random import randint
import time
import pexpect
import signal
import sys
from constants import *

gatt = pexpect.spawn('gatttool -I')
def exit_gracefully(sig, other):
    gatt.sendline("disconnect")
    gatt.sendline("quit")
    sys.exit(1)
signal.signal(signal.SIGINT, exit_gracefully)
def int_to_hex(intv):
    h = hex(intv).replace("0x", "")
    while len(h) < 2:
        h = "0" + h
    return h
def get_rgb_hex(r,g,b):
    sig = (3*16 + 1) ^ r ^ g ^ b
    bins = [51, 5, 2, r, g, b, 0, 255, 174, 84, 0, 0, 0, 0, 0, 0, 0, 0, 0, sig]
    bins_str = map(int_to_hex, bins)
    return "".join(bins_str)
def get_brightness_hex(bright):
    sig = (3*16 + 3) ^ (4) ^ bright
    bins = [51, 4, bright, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, sig]
    bins_str = map(int_to_hex, bins)
    return "".join(bins_str)

def write_data(data, addr):
    gatt.sendline(f"connect {addr}")
    try:
        gatt.expect("Connection successful", timeout=5)
    except pexpect.exceptions.TIMEOUT:
        dev = addr_dev_dict[addr]
        print(f"Failed to connect to {dev}")
        return

    gatt.sendline(f"char-write-cmd {handle_hex} {data}")
    gatt.expect(".*")
    gatt.sendline("disconnect")
    gatt.expect(".*")
def change_color(rgbt, addr):
    r, g, b = rgbt
    hexstr = get_rgb_hex(r,g,b)
    write_data(hexstr, addr)
    print(f"Changed {addr_dev_dict[addr]} color to {rgbt}")

def change_brightness(bright, addr):
    hexstr = get_brightness_hex(bright)
    write_data(hexstr, addr)
    print(f"Changed {addr_dev_dict[addr]} brightness to {bright}")

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

def change_color_all(rgbt):
    for addr in devices.values():
        change_color(rgbt, addr)
def change_brightness_both(bright):
    for addr in devices.values():
        change_brightness(bright, addr)
def gen_rand_color():
    r = randint(0,255)
    g = randint(0,255)
    b = randint(0,255)
    max_c = max([r,g,b])
    factor = 255/max_c
    rp = round(r*factor)
    gp = round(g*factor)
    bp = round(b*factor)
    rgbt = (rp, gp, bp)
    return rgbt
