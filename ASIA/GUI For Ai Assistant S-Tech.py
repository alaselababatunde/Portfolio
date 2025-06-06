import threading
import pygame
from pygame import *
import os.path
import struct
import time
import pyttsx3
from PIL import Image

#variable for whole program
MASTER= "Boss"
AINAME= "A.S.I.A"
USERNAME= "Alasela"
TALKING= False
WAKE= "n"
SHOW= False
COUNT = 1
SESSION_ID = "me"
USER = "Boss"

#GUI Info
class imageHandler:
    def __init__(self):
        self.pics = dict()

    def loadFromFile(self, filename, id = None):
        if id == None: id == filename
        self.pics[id] = pygame.image.load(filename).convert()

    def loadFromSurface(self, surface, id):
        self.pics[id] = surface.convert_alpha()

    def render(self, surface, id, position=None, clear=False, size=None):
        if clear == True:
            surface.fill((5, 2, 23))#

        if position == None:
            picX = int(surface.get_width()/2-self.pics[id].get_width()/2)
        else:
            picX = position[0]
            picY = position[1]

        if size==None:
            surface.blit(self.pics[id], (picX, picY))

        else:
            surface.blit(pygame.transform.smoothscale(self.pics[id], size), (picX, picY))


#initialize the display
#initiates the diplay pygame
pygame.display.init()
pygame.display.set_caption("A.S.I.A")
screen = pygame.display.set_mode((1000, 600), pygame.NOFRAME)
handler = imageHandler()

def display():
    #Normal-Orb Non Speaking
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_00_delay-0.04s.gif", "0")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_01_delay-0.04s.gif", "1")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_02_delay-0.04s.gif", "2")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_03_delay-0.04s.gif", "3")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_04_delay-0.04s.gif", "4")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_05_delay-0.04s.gif", "5")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_06_delay-0.04s.gif", "6")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_07_delay-0.04s.gif", "7")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_08_delay-0.04s.gif", "8")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_09_delay-0.04s.gif", "9")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_10_delay-0.04s.gif", "10")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_11_delay-0.04s.gif", "11")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_12_delay-0.04s.gif", "12")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_13_delay-0.04s.gif", "13")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_14_delay-0.04s.gif", "14")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_15_delay-0.04s.gif", "15")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_16_delay-0.04s.gif", "16")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_17_delay-0.04s.gif", "17")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_18_delay-0.04s.gif", "18")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_19_delay-0.04s.gif", "19")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_20_delay-0.04s.gif", "20")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_21_delay-0.04s.gif", "21")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_22_delay-0.04s.gif", "22")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_23_delay-0.04s.gif", "23")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_24_delay-0.04s.gif", "24")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_25_delay-0.04s.gif", "25")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_26_delay-0.04s.gif", "26")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_27_delay-0.04s.gif", "27")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_28_delay-0.04s.gif", "28")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_29_delay-0.04s.gif", "29")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_30_delay-0.04s.gif", "30")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_31_delay-0.04s.gif", "31")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_32_delay-0.04s.gif", "32")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_33_delay-0.04s.gif", "33")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_34_delay-0.04s.gif", "34")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_35_delay-0.04s.gif", "35")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_36_delay-0.04s.gif", "36")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_37_delay-0.04s.gif", "37")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_38_delay-0.04s.gif", "38")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_39_delay-0.04s.gif", "39")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_40_delay-0.04s.gif", "40")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_41_delay-0.04s.gif", "41")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_42_delay-0.04s.gif", "42")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_43_delay-0.04s.gif", "43")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_44_delay-0.04s.gif", "44")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_45_delay-0.04s.gif", "45")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_46_delay-0.04s.gif", "46")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_47_delay-0.04s.gif", "47")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_48_delay-0.04s.gif", "48")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_49_delay-0.04s.gif", "49")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_50_delay-0.04s.gif", "50")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_51_delay-0.04s.gif", "51")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_52_delay-0.04s.gif", "52")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_53_delay-0.04s.gif", "53")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_54_delay-0.04s.gif", "54")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_55_delay-0.04s.gif", "55")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_56_delay-0.04s.gif", "56")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_57_delay-0.04s.gif", "57")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_58_delay-0.04s.gif", "58")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_59_delay-0.04s.gif", "59")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_60_delay-0.04s.gif", "60")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_61_delay-0.04s.gif", "61")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_62_delay-0.04s.gif", "62")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_63_delay-0.04s.gif", "63")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_64_delay-0.04s.gif", "64")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_65_delay-0.04s.gif", "65")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_66_delay-0.04s.gif", "66")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_67_delay-0.04s.gif", "67")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_68_delay-0.04s.gif", "68")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_69_delay-0.04s.gif", "69")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_70_delay-0.04s.gif", "70")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_71_delay-0.04s.gif", "71")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_72_delay-0.04s.gif", "72")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_73_delay-0.04s.gif", "73")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_74_delay-0.04s.gif", "74")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-74c4a079b6-gif-im\frame_75_delay-0.04s.gif", "75")

    #Normal-Orb Speaking
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_00_delay-0.04s.gif", "100")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_01_delay-0.04s.gif", "101")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_02_delay-0.04s.gif", "102")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_03_delay-0.04s.gif", "103")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_04_delay-0.04s.gif", "104")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_05_delay-0.04s.gif", "105")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_06_delay-0.04s.gif", "106")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_07_delay-0.04s.gif", "107")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_08_delay-0.04s.gif", "108")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_09_delay-0.04s.gif", "109")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_10_delay-0.04s.gif", "110")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_11_delay-0.04s.gif", "111")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_12_delay-0.04s.gif", "112")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_13_delay-0.04s.gif", "113")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_14_delay-0.04s.gif", "114")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_15_delay-0.04s.gif", "115")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_16_delay-0.04s.gif", "116")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_17_delay-0.04s.gif", "117")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_18_delay-0.04s.gif", "118")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_19_delay-0.04s.gif", "119")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_20_delay-0.04s.gif", "120")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_21_delay-0.04s.gif", "121")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_22_delay-0.04s.gif", "122")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_23_delay-0.04s.gif", "123")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_24_delay-0.04s.gif", "124")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_25_delay-0.04s.gif", "125")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_26_delay-0.04s.gif", "126")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_27_delay-0.04s.gif", "127")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_28_delay-0.04s.gif", "128")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_29_delay-0.04s.gif", "129")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_30_delay-0.04s.gif", "130")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_31_delay-0.04s.gif", "131")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_32_delay-0.04s.gif", "132")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_33_delay-0.04s.gif", "133")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_34_delay-0.04s.gif", "134")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_35_delay-0.04s.gif", "135")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_36_delay-0.04s.gif", "136")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_37_delay-0.04s.gif", "137")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_38_delay-0.04s.gif", "138")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_39_delay-0.04s.gif", "139")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_40_delay-0.04s.gif", "140")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_41_delay-0.04s.gif", "141")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_42_delay-0.04s.gif", "142")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_43_delay-0.04s.gif", "143")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_44_delay-0.04s.gif", "144")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_45_delay-0.04s.gif", "145")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_46_delay-0.04s.gif", "146")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_47_delay-0.04s.gif", "147")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_48_delay-0.04s.gif", "148")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_49_delay-0.04s.gif", "149")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_50_delay-0.04s.gif", "150")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_51_delay-0.04s.gif", "151")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_52_delay-0.04s.gif", "152")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_53_delay-0.04s.gif", "153")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_54_delay-0.04s.gif", "154")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_55_delay-0.04s.gif", "155")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_56_delay-0.04s.gif", "156")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_57_delay-0.04s.gif", "157")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_58_delay-0.04s.gif", "158")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_59_delay-0.04s.gif", "159")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_60_delay-0.04s.gif", "160")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_61_delay-0.04s.gif", "161")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_62_delay-0.04s.gif", "162")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_63_delay-0.04s.gif", "163")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_64_delay-0.04s.gif", "164")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_65_delay-0.04s.gif", "165")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_66_delay-0.04s.gif", "166")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_67_delay-0.04s.gif", "167")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_68_delay-0.04s.gif", "168")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_69_delay-0.04s.gif", "169")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_70_delay-0.04s.gif", "170")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_71_delay-0.04s.gif", "171")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_72_delay-0.04s.gif", "172")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_73_delay-0.04s.gif", "173")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_74_delay-0.04s.gif", "174")
    handler.loadFromFile(r"C:\Users\HP\Documents\Python_Scripts\PythonProject\A.S.I.A\ezgif-1-9482c10dc3-gif-im\frame_75_delay-0.04s.gif", "175")

def faceA():
    A = 240 #left and right of the screen
    B = -5 #up and down of the screen
    x = 550 #size width
    y = 550 #size length

    COUNT = 1
    global TALKING
    while True:
        if TALKING == False:
            if COUNT >= 75:
                COUNT = COUNT - 100
            img = str(COUNT)
            handler.render(screen, img, (A, B), True, (x, y))
            pygame.display.update(A, B, x, y)
            time.sleep(.04)
            COUNT = COUNT + 1
            if COUNT == 75:
                COUNT = 0

        elif TALKING == True:
            if COUNT <= 100:
                COUNT = COUNT + 100
            img = str(COUNT)
            handler.render(screen, img, (A, B), True, (x, y))
            pygame.display.update(A, B, x, y)
            time.sleep(.04)
            COUNT = COUNT + 1
            if COUNT == 175:
                COUNT = 100

        pygame.quit()


#speak function will pronounce the string passed to it

def speak(text):
    global TALKING
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    TALKING = True
    print("A.S.I.A:" +text+"\n")
    engine.say(text)
    engine.runAndWait()
    TALKING = False

speak ("ASIA, Here")

def jmain():
    porcupine = None
    pa = None
    audio_stream = None

    try:
        custom_keyword_path = r"C:\\Users\\HP\\Documents\\Python_Scripts\\PythonProject\\A.S.I.A\\hey-asia_en_windows_v3_0_0\\hey-asia_en_windows_v3_0_0.ppn"
        porcupine = pvporcupine.create(
        access_key='+noOL8NnQKDqBy+eq/hL0r4PBOAqHyJSOf+K/j80URoyZshWQzDU0g==',
        keyword_paths=[custom_keyword_path]
        )
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
                               rate=porcupine.sample_rate,
                               channels=1,
                               format=pyaudio.paInt16,
                               input=True,
                               frames_per_buffer=porcupine.frame_length)
        while True:
                    pcm = audio_stream.read(porcupine.frame_length)
                    pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

                    keyword_index = porcupine.process(pcm)
                    if keyword_index >= 0:
                        speak("Wake-word Detected......")
                        speak("Greetings Sir")
                        time.sleep(1)
                        speak("Awaiting your call " + USER)
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()


def main():
    t1 = threading.Thread(target=jmain)
    t2 = threading.Thread(target=faceA)

    display()
    t1.start()
    t2.start()

main()