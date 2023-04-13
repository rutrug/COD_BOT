import pyautogui
import time
import os
import configparser
from numpy import sqrt
import numpy as np
import smtplib
from email.message import EmailMessage
import datetime
import random
from screeninfo import get_monitors
from ctypes import *
import subprocess
import cv2
import math
import traceback
import logging
import telegram
from termcolor import colored
from enum import Enum

class Resource(Enum):
    GOLD = 1
    WOOD = 2
    ORE = 3
    MANA = 4
    NONE = 5

pyautogui.useImageNotFoundException()

api_key = '5523515228:AAEAh9CCIGHEi71jT_W74ViN95tAyl3VZyE'
bot = telegram.Bot(token=api_key)

RECEIVER_TELEGRAM_ID = "0"
TASKS_CLEARALL_BUTTON_NOX = (0,0)
NOTIFICATION_EXPECTED_NOX = (0,0)
NOTIFICATION_PX = (0,0,0)
NOTIFICATION_CLOSE = (0,0)
CITY_BUTTON = (0,0)
ALLIANCE_BUILDING = (0,0)
SCOUT_BUILDING = (0,0)
SCOUT_BUTTON = (0,0)
CENTER_OF_SCREEN = (0,0)

TIER5_UNIT_POS = (0,0)
TRAIN_OFFSET = (0,0)

ALLIANCE_BUTTON = (0,0)
TERRITORY_BUTTON = (0,0)

MARCH_1_PRESET = (0,0)
MARCH_2_PRESET = (0,0)
MARCH_3_PRESET = (0,0)
MARCH_4_PRESET = (0,0)

NEW_TROOPS = (0,0)
NEW_TROOPS_PX = (0,0,0)
REMOVE_COMMANDER = (0,0,0)
LAUNCH_MISSION = (0,0)
SEARCH_BUTTON = (0,0)
GOLDDEPO = (0, 0)
LOGGINGCAMP = (0,0)
OREDEPO = (0, 0)
MANADEPO = (0, 0)
SEARCH_DEPO_Y_OFFSET = 0
GATHER_BUTTON = (0,0)
RESOURCE_OWNER_BOX_TOPLEFT = (0,0)
RESOURCE_OWNER_BOX_BOTRIGHT = (0,0)

BLACKSMITH_POSITION = (0,0)
MATERIAL_PRODUCTION = (0,0)
MAT_LEATHER_POSITION = (0,0)
MAT_STONE_POSITION = (0,0)
MAT_WOOD_POSITION = (0,0)
MAT_BONE_POSITION = (0,0)

CURRENT_MARCHES_TOPLEFT = (0,0)
CURRENT_MARCHES_BOTTOMRIGHT = (0,0)

TAVERN_POSITION = (0,0)
TAVERN_OPEN_INFO_POSITION = (0,0)
TAVERN_INFO_BACK_POSITION = (0,0)
TAVERN_OPEN_SILVER_BOTTOM_RIGHT_CORNER_POSITION = (0,0)

MAX_NUM_OF_MARCHES_TOTAL = 0
MAX_GATHERING_MARCHES_ALLOWED = 0

FREE_MARCHES_CALENDAR = [(0,0),(1,0)] # ((HOUR OF DAY, NUM OF RESERVED MARCHES),(-,-),..)
CLICK_TIME_MULTIPLIER = 1.0
EXECUTION_START = datetime.datetime.now()

RES_COUNTER_FOOD = 0
RES_COUNTER_WOOD = 0
RES_COUNTER_STONE = 0
RES_COUNTER_GOLD = 0

MAT_LEATHER_WEIGHT = 1
MAT_STONE_WEIGHT = 1
MAT_WOOD_WEIGHT = 1
MAT_BONE_WEIGHT = 1

RES_FOOD_WEIGHT = 1
RES_WOOD_WEIGHT = 1
RES_STONE_WEIGHT = 1
RES_GOLD_WEIGHT = 1

SWORDSMAN_CAMP = (0,0)
KNIGHT_CAMP = (0,0)
BALLISTA_FACTORY = (0,0)
ABBEY = (0,0)
SAFE_CITY_GOBACK = (0,0)

MEASUREMENT_SLEEP_SECONDS = 1

GAME_RES_ITERATOR = random.randint(0, 4)
DATE_LAST_ACTION = datetime.datetime.now()
DRAG_DISTANCE_VERTICAL = 400
DRAG_DISTANCE_HORIZONTAL = 1200

MAIL = "mirko.omegabot@gmail.com"
PWD = "fiplvdhsfcercqyn"
CUSTOM_GAME_PATH = r"D:\rok.lnk"
CUSTOM_LAUNCH_SLEEPTIME = 40

END_STATE = 0
RESTART_REQUIRED = 0

CURRENT_NUMBER_OF_MARCHES = 0

def main():
    
    while 1:
    
        try:
        
            pyautogui.FAILSAFE = True
            printMirkoBotHead()
            print("1. Run MirkoBot and launch game.")
            print("2. Run MirkoBot and listen for notifications.")
            print("3. Take measurements and create save file.")
            print("4. Manual helper; print pos and color.\n")
            
            val1 = input("Continue with: ")
            clear = lambda: os.system('cls')
            clear()
            
            
            
            if val1 == "1":
                while 1:
                    loadConfigAndRun()

                    if isGameStateValid():
                        notificationListenerLoop()
                
            if val1 == "2":
                loadConfigAndWait()
                
            if val1 == "3":
                takeMeasurements()
                saveMeasurementsToFile()
                print("Measurements taken! Pogu!")
                main()
            if val1 == "4":
                reportMousePosition()
            if val1 == "5":
                loadMeasurementsFromFile()
                
                while(1):
                    #guessActionPointsPercentage()
                    nm = CURRENT_NUMBER_OF_MARCHES
                    time.sleep(1)
                    
                val1 = input("Continue with: ")
                
        except:
            print('\n')
            logging.error(traceback.format_exc())
            val1 = input("\n Press enter to exit. :(")
        
def test():

    input("b")
    (x, y) = pyautogui.position()
    pixel1 = pyautogui.pixel(getAdjustedX(x), y)
    print(pixel1)
    
    input("a")
    (x, y) = pyautogui.position()
    pixel2 = pyautogui.pixel(getAdjustedX(x), y)
    print(pixel2)
    
    d=sqrt(abs((pixel2[0]-pixel1[0])^2+(pixel2[1]-pixel1[1])^2+(pixel2[2]-pixel1[2])^2))
    
    p=d/ sqrt((255)^2+(255)^2+(255)^2)
    print("diff", p)
    print("--")
    
def notificationListenerLoop():
    
    print(getCurrentTimestamp() + " > Listening for notification.")
    
    BOREDOM_THRESHOLD = 600
    
    while(1):
    
        pixel = pyautogui.pixel(getAdjustedX(NOTIFICATION_EXPECTED_NOX[0]), NOTIFICATION_EXPECTED_NOX[1])
        if pixel == NOTIFICATION_PX:
            #Prisla notifikacia
            print(getCurrentTimestamp() + colored(" > Notification detected! Game launching in 10 seconds.", "green"))
            time.sleep(1)
            click(getAdjustedX(NOTIFICATION_CLOSE[0]),NOTIFICATION_CLOSE[1], 1)
            time.sleep(8)
            break
        
        dt = datetime.datetime.now() - DATE_LAST_ACTION
        
        if dt.seconds > BOREDOM_THRESHOLD:
            print(getCurrentTimestamp() + " > Boredom threshold ", colored(BOREDOM_THRESHOLD, "yellow"), " passed, launching game.")
            break
            
            
        time.sleep(1)

    
def launchGame():
    global DATE_LAST_ACTION
    global CUSTOM_GAME_PATH
    global EXECUTION_START

    DATE_LAST_ACTION = datetime.datetime.now()
    EXECUTION_START = datetime.datetime.now()

   # FNULL = open(os.devnull, 'w')
    #args = CUSTOM_GAME_PATH
    #subprocess.Popen(args, stdout=FNULL, stderr=FNULL, shell=False)
    os.startfile(CUSTOM_GAME_PATH)

    time.sleep(CUSTOM_LAUNCH_SLEEPTIME)

    while 1:
        try:
            loc = pyautogui.locateOnScreen('COD_LOADING.png', confidence=0.6)
            locPoint = pyautogui.center(loc)
            time.sleep(2)
        except pyautogui.ImageNotFoundException:
            break



    pyautogui.press('F11')

    time.sleep(6)
    doWork()
    
def getNumberOfCalendarReservations():

    now = datetime.datetime.now()
    
    stringTimestamp = now.strftime("%H")
    hour = int(stringTimestamp)
    
    for i in FREE_MARCHES_CALENDAR:
    
        if i[0] == hour:
            return i[1]
    return 0
    
def printResourceStatistics():

    print("> [CROP:",colored(RES_COUNTER_FOOD,'yellow'),"] [WOOD:",colored(RES_COUNTER_WOOD,'yellow'),"] [STONE:",colored(RES_COUNTER_STONE,'yellow'),"] [GOLD:",colored(RES_COUNTER_GOLD,'yellow'),"]")
    
def guessActionPointsPercentage():
    
    ACTION_COLOR = np.array([142, 255, 0])
    EMPTY_COLOR = np.array([20, 82, 122])
    
    DISTANCE_THRESHOLD = 100
    
    pyautogui.screenshot("actionbar.png", region = (0,0,180,180))
    img = cv2.imread('actionbar.png')
    (h, w) = img.shape[:2]
    
    indexX = 0
    indexY = 0
    
    actionBarStart = w
    actionBarEnd = 0
    emptyBarStart = w
    emptyBarEnd = 0
    
    lastValidPX = (0,0)
    
    for indexX in range(0, w):
        for indexY in range(0, h):
            
            (b, g, r) = img[indexX, indexY]
            imagePx = np.array([r,g,b])
            
            if colorDistance(ACTION_COLOR, imagePx) < 256:
                if indexX < actionBarStart:
                    actionBarStart = indexX
                    
                if indexX > actionBarEnd:
                    actionBarEnd = indexX
                    emptyBarStart = indexX
                    lastValidPX = (indexX, indexY)
                    
                break
                
            if colorDistance(EMPTY_COLOR, imagePx) < 256 and math.dist(lastValidPX, (indexX,indexY)) < 5:
                    
                if indexX > emptyBarEnd and indexX > emptyBarStart:
                    emptyBarEnd = indexX
                    lastValidPX = (indexX, indexY)
                    
                break
            
            indexY += 1
        indexX += 1
    
    print(actionBarStart, " ", actionBarEnd, " ", emptyBarStart, " ", emptyBarEnd)
    
def colorDistance(rgb1, rgb2):

    #rgb1 = np.array([1,1,0])
    #rgb2 = np.array([0,0,0])
    
    rm = 0.5*(rgb1[0]+rgb2[0])
    d = sum(abs((2+rm,4,3-rm)*(rgb1-rgb2))**2)**0.5
    return d


def updateNumberOfMarches():

    global CURRENT_NUMBER_OF_MARCHES
    time.sleep(1)
    
    width = CURRENT_MARCHES_BOTTOMRIGHT[0] - CURRENT_MARCHES_TOPLEFT[0]
    height = CURRENT_MARCHES_BOTTOMRIGHT[1] - CURRENT_MARCHES_TOPLEFT[1]
    region=(CURRENT_MARCHES_TOPLEFT[0], CURRENT_MARCHES_TOPLEFT[1], width, height)
    
    pyautogui.screenshot("img.png", region)
    
    templates = (cv2.imread('_1.png', cv2.IMREAD_UNCHANGED), cv2.imread('_2.png', cv2.IMREAD_UNCHANGED), cv2.imread('_3.png', cv2.IMREAD_UNCHANGED), cv2.imread('_4.png', cv2.IMREAD_UNCHANGED), cv2.imread('_5.png', cv2.IMREAD_UNCHANGED))
    
    index = 0
    threshhold = 1
    found = False
    
    targetIndex = 0
    targetThreshold = -1
    
    while threshhold > 0.96 and found == False:
        while index < 5 and found == False:
            img = cv2.imread('img.png')
            #template = cv2.imread('_4.png', cv2.IMREAD_UNCHANGED)
            hh, ww = templates[index].shape[:2]

            # extract base image and alpha channel and make alpha 3 channels
            base = templates[index][:,:,0:3]
            alpha = templates[index][:,:,3]
            alpha = cv2.merge([alpha,alpha,alpha])
            
            # do masked template matching and save correlation image
            correlation = cv2.matchTemplate(img, base, cv2.TM_CCORR_NORMED, mask=alpha)

            # set threshold and get all matches
            
            loc = np.where(correlation >= threshhold)
            
            result = img.copy()
            for pt in zip(*loc[::-1]):
                cv2.rectangle(result, pt, (pt[0]+ww, pt[1]+hh), (0,0,255), 1)
                found = True
                targetIndex = index
                targetThreshold = threshhold
                #print(index, " ", threshhold)
                break
            index += 1
        
        if found == True:
            break
        index = 0
        threshhold -= 0.001
    
    perc = ((0.04 - (1 - targetThreshold)) / 0.04) * 100
    
    if found == False:
        print("> Current marches not found, probably", colored('0', 'yellow'), ".")
    else:
        print("> Current marches",  colored(targetIndex + 1, 'yellow'), "confidence", colored(round(perc), 'yellow'), "%")
        
    CURRENT_NUMBER_OF_MARCHES = targetIndex + 1
    return CURRENT_NUMBER_OF_MARCHES
    
def isBoxNearPosition(foundBox, targetPos):
    
    # not in use omegalul
    foundPosX = foundBox[0] + foundBox[2] * 0.5
    foundPosY = foundBox[1] + foundBox[3] * 0.5
    
    if foundPosX > targetPos[0] - 15:
        if foundPosX < targetPos[0] + 15:
            if foundPosY > targetPos[1] - 15:
                if foundPosY < targetPos[1] + 15:
                    return True
    
    return False
    
workIntensity = 0
def doWork():
    global workIntensity

    err = 0

    if err <= 0:
        err += hitAllianceBuilding()

    if err <= 0:
        err += trainTroops()

    #if err <= 0:
    #    err += tryHelpAlliance()

    #if err <= 0:
    #    err += hitScoutBuilding()

    if err <= 0:
        err += gatherResources()

    time.sleep(2)

    workIntensity += 1

    if err >= 1:
        return 0

    return 1

def tryHelpAlliance():

    click(CITY_BUTTON[0], CITY_BUTTON[1], 1)
    # try find builder

    try:
        loc = pyautogui.locateOnScreen("BUILDER.png", confidence=0.75)
        click(CITY_BUTTON[0], CITY_BUTTON[1], 1)
        return 0
    except pyautogui.ImageNotFoundException:
        pass

    click(ALLIANCE_BUTTON[0], ALLIANCE_BUTTON[1], 1)
    click(TERRITORY_BUTTON[0], TERRITORY_BUTTON[1], 1)

    try:
        loc = pyautogui.locateOnScreen("COD_ALLIANCE_ROLLBACK.png", confidence=0.75)
        locPoint = pyautogui.center(loc)
        click(locPoint[0], locPoint[1], 1)
    except pyautogui.ImageNotFoundException:
        pass

    try:
        loc = pyautogui.locateOnScreen("COD_ALLIANCE_TOWERS.png", confidence=0.75)
        locPoint = pyautogui.center(loc)
        click(locPoint[0], locPoint[1], 1)
    except pyautogui.ImageNotFoundException:
        pass

    # try to look for participation

    try:
        loc = pyautogui.locateOnScreen("COD_ALLIANCE_ROLLBACK.png", confidence=0.75)
        locPoint = pyautogui.center(loc)
        click(locPoint[0], locPoint[1], 1.2)
    except pyautogui.ImageNotFoundException:
        pass

    try:
        loc = pyautogui.locateOnScreen("COD_ALLIANCE_ROADS.png", confidence=0.75)
        locPoint = pyautogui.center(loc)
        click(locPoint[0], locPoint[1], 1)
    except pyautogui.ImageNotFoundException:
        pass

    # try to look for participation

    try:
        loc = pyautogui.locateOnScreen("COD_ALLIANCE_GOBACK.png", confidence=0.75)
        locPoint = pyautogui.center(loc)
        click(locPoint[0], locPoint[1], 1)

        try:
            loc = pyautogui.locateOnScreen("COD_ALLIANCE_GOBACK.png", confidence=0.75)
            locPoint = pyautogui.center(loc)
            click(locPoint[0], locPoint[1], 1)
            return 1
        except pyautogui.ImageNotFoundException:
            return 0

    except pyautogui.ImageNotFoundException:
        return 0

    click(CITY_BUTTON[0], CITY_BUTTON[1], 2)

def trainTroops():

    handleTrainingInBuilding(SWORDSMAN_CAMP[0], SWORDSMAN_CAMP[1], "COD_SWORDSMEN_TRAIN.png")
    handleTrainingInBuilding(KNIGHT_CAMP[0], KNIGHT_CAMP[1],"COD_KNIGHT_TRAIN.png", 1)
    handleTrainingInBuilding(ABBEY[0], ABBEY[1],"COD_ABBEY_TRAIN.png")
    handleTrainingInBuilding(BALLISTA_FACTORY[0], BALLISTA_FACTORY[1],"COD_BALLISTA_TRAIN.png")

    return 0

def handleTrainingInBuilding(posX, posY, buildingTrain, lockBuildTier = -1):

    click(posX, posY, 0.25)
    click(posX, posY, 0.25)

    try:
        loc = pyautogui.locateOnScreen(buildingTrain, confidence=0.75)
        locPoint = pyautogui.center(loc)
        click(locPoint[0], locPoint[1], 0.75)

        try:
            loc = pyautogui.locateOnScreen("COD_SPEEDUP.png", confidence=0.75)
            click(SAFE_CITY_GOBACK[0], SAFE_CITY_GOBACK[1], 1)
            return 0
        except pyautogui.ImageNotFoundException:
            pass


        # first try to look for upgrades
        activeTier = 1
        maxTier = 5

        if lockBuildTier < 0:
            while activeTier < maxTier:
                xOffset = (maxTier - activeTier) * TRAIN_OFFSET[0]
                click(TIER5_UNIT_POS[0] - xOffset, TIER5_UNIT_POS[1], 0.1)

                try:
                    loc = pyautogui.locateOnScreen("COD_TRAIN_UPGRADE.png", confidence=0.75)
                    # We do have upgrades for this tier
                    locPoint = pyautogui.center(loc)
                    click(locPoint[0], locPoint[1], 0.25)

                    try:
                        loc = pyautogui.locateOnScreen("COD_PROMOTE.png", confidence=0.75)
                        locPoint = pyautogui.center(loc)
                        click(locPoint[0], locPoint[1], 1)
                        # Success upgrade!
                        return 1
                    except pyautogui.ImageNotFoundException:
                        # This shouldn't happen, not enough resources or what?!
                        pass
                    break
                except pyautogui.ImageNotFoundException:
                    # We don't have any units for upgrade on this tier
                    time.sleep(0)

                activeTier += 1


        # now train highest tier

        if lockBuildTier < 0:
            tierCounter = 0
            while tierCounter < maxTier:
                xOffset = TRAIN_OFFSET[0] * tierCounter
                click(TIER5_UNIT_POS[0] - xOffset, TIER5_UNIT_POS[1], 0.1)

                try:
                    loc = pyautogui.locateOnScreen("COD_TRAIN.png", confidence=0.75)
                    # We can train this!
                    locPoint = pyautogui.center(loc)
                    click(locPoint[0], locPoint[1], 1)
                    return 1

                except pyautogui.ImageNotFoundException:
                    # Such unit is not available
                    time.sleep(0)
                tierCounter += 1

        if lockBuildTier > 0:
            xOffset = (TRAIN_OFFSET[0] * (maxTier - lockBuildTier))
            click(TIER5_UNIT_POS[0] - xOffset, TIER5_UNIT_POS[1], 0.5)

            try:
                loc = pyautogui.locateOnScreen("COD_TRAIN.png", confidence=0.75)
                # We can train this!
                locPoint = pyautogui.center(loc)
                click(locPoint[0], locPoint[1], 1)
                return 1

            except pyautogui.ImageNotFoundException:
                # Such unit is not available
                time.sleep(0)

        click(SAFE_CITY_GOBACK[0], SAFE_CITY_GOBACK[1], 1)
        return 0
    except pyautogui.ImageNotFoundException:
        return 0

def gatherResources():

    found = 1
    click(CITY_BUTTON[0], CITY_BUTTON[1], 1)

    while found == 1 :

        found = 0
        priorityFound = 1
        loopCount = 0

        returnVal = 0
        while loopCount < 4:
            priorityFound = 0
            loopCount += 1
            returnVal = tryFindResource(1)
            if returnVal == 1:
                priorityFound = 1
                found = 1
                break
            if returnVal == 2:
                break

        if returnVal == 2:
            print("No free march available")

        if priorityFound == 0 and returnVal != 2:
            time.sleep(5)
            returnVal = tryFindResource(0)
            if returnVal == 0:
                print("No resource found hej")
            if returnVal == 1:
                found = 1

    click(CITY_BUTTON[0], CITY_BUTTON[1], 1)
    return 0


def tryFindResource(priority):

    priorityFound = 0
    resourceName = ""

    resource = Resource.NONE
    # BASED ON FIRST AVAILABLE HERO, CHOOSE RESOURCE

    try:
        loc = pyautogui.locateOnScreen('GATHERER_GOLD.png', confidence=0.75)
        try:
            loc = pyautogui.locateOnScreen('GATHERER_WOOD.png', confidence=0.75)
            try:
                loc = pyautogui.locateOnScreen('GATHERER_ORE.png', confidence=0.75)

            except pyautogui.ImageNotFoundException:
                resource = Resource.ORE

        except pyautogui.ImageNotFoundException:
            resource = Resource.WOOD

    except pyautogui.ImageNotFoundException:
        resource = Resource.GOLD

    if resource == Resource.NONE:
        return 0

    click(SEARCH_BUTTON[0], SEARCH_BUTTON[1], 1)

    # GOLD
    if resource == Resource.GOLD:
        resourceName = "GOLD"
        click(GOLDDEPO[0], GOLDDEPO[1], 1)
    # wood
    elif resource == Resource.WOOD:
        resourceName = "WOOD"
        click(LOGGINGCAMP[0], LOGGINGCAMP[1], 1)
    # ore
    elif resource == Resource.ORE:
        resourceName = "ORE"
        click(OREDEPO[0], OREDEPO[1], 1)

    elif resource == Resource.MANA:
        resourceName = "MANA"
        click(MANADEPO[0], MANADEPO[1], 1)

    try:
        loc = pyautogui.locateOnScreen('COD_BUTTON_SEARCH.png', confidence=0.75)
        locPoint = pyautogui.center(loc)
        click(locPoint[0], locPoint[1], 3)
    except pyautogui.ImageNotFoundException:
        return 0

    click(CENTER_OF_SCREEN[0], CENTER_OF_SCREEN[1], 1.2)

    if priority:
        try:
            loc = pyautogui.locateOnScreen('COD_ALLYTAG.png', confidence=0.75)
            locPoint = pyautogui.center(loc)
        except pyautogui.ImageNotFoundException:
            return 0

        try:
            loc = pyautogui.locateOnScreen('COD_BUTTON_GATHER.png', confidence=0.75)
            locPoint = pyautogui.center(loc)
            click(locPoint[0], locPoint[1], 1.2)
        except pyautogui.ImageNotFoundException:
            return 0
    else:
        try:
            loc = pyautogui.locateOnScreen('COD_NEUTRAL_RESOURCE.png', confidence=0.75)
            locPoint = pyautogui.center(loc)
        except pyautogui.ImageNotFoundException:
            try:
                loc = pyautogui.locateOnScreen('COD_ALLYTAG.png', confidence=0.75)
                locPoint = pyautogui.center(loc)
            except pyautogui.ImageNotFoundException:
                return 0

        try:
            loc = pyautogui.locateOnScreen('COD_BUTTON_GATHER.png', confidence=0.75)
            locPoint = pyautogui.center(loc)
            click(locPoint[0], locPoint[1], 1.2)
        except pyautogui.ImageNotFoundException:
            return 0

    try:
        loc = pyautogui.locateOnScreen('COD_CREATE_LEGION.png', confidence=0.75)
        locPoint = pyautogui.center(loc)
        click(locPoint[0], locPoint[1], 1)

        if resource == Resource.GOLD:
            click(MARCH_1_PRESET[0], MARCH_1_PRESET[1], 0.5)
        elif resource == Resource.WOOD:
            click(MARCH_2_PRESET[0], MARCH_2_PRESET[1], 0.5)
        elif resource == Resource.ORE:
            click(MARCH_3_PRESET[0], MARCH_3_PRESET[1], 0.5)
        elif resource == Resource.MANA:
            click(MARCH_4_PRESET[0], MARCH_4_PRESET[1], 0.5)

        loc = pyautogui.locateOnScreen('COD_MARCH2.png', confidence=0.75)
        locPoint = pyautogui.center(loc)
        click(locPoint[0], locPoint[1], 1)

        print(getCurrentTimestamp() + " Gathering resource! " + " priority " + str(priority) + " resource " + colored(resourceName, 'yellow'))
        found = 1
        time.sleep(1)
        return 1

    except pyautogui.ImageNotFoundException:
        time.sleep(0)
        click(CITY_BUTTON[0], CITY_BUTTON[1], 1)
        return 2
        # no march ready


def hitScoutBuilding():

    while 1:
        click(SCOUT_BUILDING[0], SCOUT_BUILDING[1], 0.5)
        click(SCOUT_BUTTON[0], SCOUT_BUTTON[1], 0.5)

        # ------------            SEND SCOUT
        try:
            loc = pyautogui.locateOnScreen('COD_EXPLORE.png', confidence=0.6)
            locPoint = pyautogui.center(loc)
            click(locPoint[0], locPoint[1], 3)

            loc = pyautogui.locateOnScreen('COD_EXPLORE.png', confidence=0.6)
            locPoint = pyautogui.center(loc)
            click(locPoint[0], locPoint[1], 2)

            loc = pyautogui.locateOnScreen('COD_MARCH.png', confidence=0.6)
            locPoint = pyautogui.center(loc)
            click(locPoint[0], locPoint[1], 1)

            # we are sending scouterino
            click(CITY_BUTTON[0], CITY_BUTTON[1], 3)
            continue

        except pyautogui.ImageNotFoundException:
            # NO FREE SCOUT, GO CHECK OTHER
            try:
                loc = pyautogui.locateOnScreen('COD_OTHER.png', confidence=0.75)
                locPoint = pyautogui.center(loc)
                click(locPoint[0], locPoint[1], 1)

            except pyautogui.ImageNotFoundException:
                # this might be because region is scouted, 100% finish
                print("SCOUT BUILDING :: CANNOT FIND OTHER BUTTON")
                return 0

            try:
                loc = pyautogui.locateOnScreen('COD_VISIT_BUTTON.png', confidence=0.75)
                locPoint = pyautogui.center(loc)
                click(locPoint[0], locPoint[1], 1)


                while 1:

                    time.sleep(2)
                    click(CENTER_OF_SCREEN[0], CENTER_OF_SCREEN[1], 2)
                    time.sleep(2)

                    try:
                        print("GO gound")
                        loc = pyautogui.locateOnScreen('COD_BUTTON_GO.png', confidence=0.75)
                        locPoint = pyautogui.center(loc)
                        click(locPoint[0], locPoint[1], 1)
                        continue

                    except pyautogui.ImageNotFoundException:
                        print("GO not found, make a choice?")
                        # if trader, gotta make a choice
                        click(1200, 600, 2)
                        found = 0

                        try:
                            loc = pyautogui.locateOnScreen('COD_CLAIM.png', confidence=0.75)
                            locPoint = pyautogui.center(loc)
                            print("claim found")
                            click(locPoint[0], locPoint[1], 1)
                            found = 1
                        except pyautogui.ImageNotFoundException:
                            time.sleep(0)

                        try:
                            loc = pyautogui.locateOnScreen('COD_RECRUIT.png', confidence=0.75)
                            locPoint = pyautogui.center(loc)
                            print("recruit found")
                            click(locPoint[0], locPoint[1], 1)
                            found = 1
                        except pyautogui.ImageNotFoundException:
                            time.sleep(0)

                        try: # DUNGEOOOOOOOON
                            loc = pyautogui.locateOnScreen('COD_VISIT_DUNG.png', confidence=0.6)
                            locPoint = pyautogui.center(loc)
                            print("visit dung found")
                            click(locPoint[0], locPoint[1], 0.5)
                            time.sleep(1)

                            loc = pyautogui.locateOnScreen('COD_ROLLDOWN.png', confidence=0.6)
                            locPoint = pyautogui.center(loc)
                            print("rolldown found")
                            click(locPoint[0], locPoint[1], 0.5)

                            loc = pyautogui.locateOnScreen('COD_OPTION.png', confidence=0.7)
                            locPoint = pyautogui.center(loc)
                            print("option found")
                            click(locPoint[0], locPoint[1], 0.5)

                            loc = pyautogui.locateOnScreen('COD_OPTION.png', confidence=0.7)
                            locPoint = pyautogui.center(loc)
                            print("option found")
                            click(locPoint[0], locPoint[1], 0.5)

                            loc = pyautogui.locateOnScreen('COD_CLAIMCHEST.png', confidence=0.7)
                            locPoint = pyautogui.center(loc)
                            print("claim found")
                            click(locPoint[0], locPoint[1], 1)

                            time.sleep(10)

                            loc = pyautogui.locateOnScreen('COD_EYE.png', confidence=0.7)
                            locPoint = pyautogui.center(loc)
                            print("claim found")
                            click(locPoint[0], locPoint[1], 1)

                            found = 1

                            # DUNGEON END

                        except pyautogui.ImageNotFoundException:
                            time.sleep(0)

                        if found == 0:
                            print("break, recruit or claim not found")
                            break


                    time.sleep(1)

                    try:
                        loc = pyautogui.locateOnScreen('COD_BUTTON_GO.png', confidence=0.6)
                        locPoint = pyautogui.center(loc)
                        print("go found")
                        click(locPoint[0], locPoint[1], 1)
                    except pyautogui.ImageNotFoundException:
                        # NO GO BUTTON FOUND, need to go back to village
                        print("NO GO BUTTON FOUND, need to go back to village")
                        break


            except pyautogui.ImageNotFoundException:
                click(CITY_BUTTON[0], CITY_BUTTON[1], 1)
                time.sleep(2)
                return 0
                # no other claimable


    # -----------         CHECK REWARDS

def manageGatherers():

    global DATE_LAST_ACTION
    time.sleep(1)
    
    click(CITY_BUTTON[0], CITY_BUTTON[1], 0.5)
    maxLoopAttempts = 0
    
    updateNumberOfMarches()
    marches = CURRENT_NUMBER_OF_MARCHES
    
    while CURRENT_NUMBER_OF_MARCHES + getNumberOfCalendarReservations() < MAX_NUM_OF_MARCHES_TOTAL:
        
        maxLoopAttempts += 1
        
        if maxLoopAttempts == 6:
            print(colored("> Unknown possible issue detected, aborting loop.", 'red'))
            return 1
            
        if not tryToFindOptimalResource():
            print(colored("> Resources not found!", 'red'))
            #print("> Marches on the map:", colored(CURRENT_NUMBER_OF_MARCHES,'yellow'), "+", colored(getNumberOfCalendarReservations(),'yellow'),"/", colored(MAX_NUM_OF_MARCHES_TOTAL,'yellow'))
            continue
        
        click(GATHER_BUTTON[0], GATHER_BUTTON[1], 1)
        click(NEW_TROOPS[0], NEW_TROOPS[1], 2)
        click(REMOVE_COMMANDER[0], REMOVE_COMMANDER[1], 0.25)
        click(LAUNCH_MISSION[0], LAUNCH_MISSION[1], 1)
        
        time.sleep(1)
        updateNumberOfMarches()
        
        if marches == CURRENT_NUMBER_OF_MARCHES:
            # there might be an issue of some sorts
            print(colored("> Unknown possible issue detected, aborting loop.", 'red'))
            return 1
            
        DATE_LAST_ACTION = datetime.datetime.now()
        marches = CURRENT_NUMBER_OF_MARCHES
        
    if CURRENT_NUMBER_OF_MARCHES + getNumberOfCalendarReservations() >= MAX_NUM_OF_MARCHES_TOTAL:
        print("> Maximum marches on the map:", colored(CURRENT_NUMBER_OF_MARCHES,'yellow'), "+", colored(getNumberOfCalendarReservations(),'yellow'),"/", colored(MAX_NUM_OF_MARCHES_TOTAL,'yellow'))
    
    time.sleep(1)
    printResourceStatistics()
    click(CITY_BUTTON[0], CITY_BUTTON[1], 0.5) # return to neutral position
    return 0
    
def manageTavern():
    
    chance = 50
    if random.randint(1, 100) > chance: # manage only sometimes, TODO move chance to config
        return 0
    
    print("> Managing tavern ", colored((round((chance / 100) * 100)), 'yellow'), "%.")
    
    click(TAVERN_POSITION[0],TAVERN_POSITION[1], 0.5)
    click(TAVERN_OPEN_INFO_POSITION[0],TAVERN_OPEN_INFO_POSITION[1], 1)
    click(TAVERN_OPEN_SILVER_BOTTOM_RIGHT_CORNER_POSITION[0],TAVERN_OPEN_SILVER_BOTTOM_RIGHT_CORNER_POSITION[1], 4)
    click(TAVERN_OPEN_SILVER_BOTTOM_RIGHT_CORNER_POSITION[0],TAVERN_OPEN_SILVER_BOTTOM_RIGHT_CORNER_POSITION[1], 0.5)
    click(TAVERN_INFO_BACK_POSITION[0], TAVERN_INFO_BACK_POSITION[1], 1)
    
    return 0

def detectPossibleVerificationLock():

    
    try:
        x, y = pyautogui.locateCenterOnScreen('verify.png', confidence=0.75)
        
        print(colored("> Verification required!", 'red'))
        reportVerificationLock()
        
    except pyautogui.ImageNotFoundException:
        
        counter = 0
        while counter < 3:
        
            try:
            
               loc = pyautogui.locateOnScreen('verify_chest.png', confidence=0.6)
               locPoint = pyautogui.center(loc)
               click(locPoint[0], locPoint[1], 1)
               print(colored("> Verification required!", 'red'))
               reportVerificationLock()
               return 0
               
            except pyautogui.ImageNotFoundException:
            
                time.sleep(1)
                counter += 1
                pass
           
    return 0
    
def reportVerificationLock():
    
    
    timeCounter = 0
    while(1):
        
        try:
            x, y = pyautogui.locateCenterOnScreen('verify.png', confidence=0.75)
        except pyautogui.ImageNotFoundException:
            break
        
        if timeCounter == 60 or timeCounter == 120 or timeCounter == 360 or timeCounter % 600 == 0:
            if RECEIVER_TELEGRAM_ID != 0:
                msg = prestonGarveySaySomething()
                bot.send_message(chat_id=RECEIVER_TELEGRAM_ID, text=msg)
        
        time.sleep(5)
        timeCounter += 5
    
    print(colored("> Manipulation detected, bot continues in: ", 'green'))
    print("> 30 seconds ..")
    time.sleep(20)
    print("> 10 seconds ..")
    time.sleep(5)
    print("> 5 seconds ..")
    time.sleep(5)
    print("> Back to work! (°͜ʖ°)")
    

def click(xpos,ypos,length):
    
    #time.sleep(0.1)
    (x, y) = pyautogui.position()
    #time.sleep(0.1)

    pyautogui.click(getAdjustedX(xpos),ypos)
    # Move back to where the mouse was before click
    pyautogui.moveTo(x, y)
    
    time.sleep(length * CLICK_TIME_MULTIPLIER)
    
def giveResourceToFarm():

    maxNum = RES_FOOD_WEIGHT + RES_WOOD_WEIGHT + RES_STONE_WEIGHT + RES_GOLD_WEIGHT
    randomNum = random.randint(1, maxNum)
    
    if randomNum <= RES_FOOD_WEIGHT:
        #print(".. resource roll: cropland, chance: ", round((RES_FOOD_WEIGHT / maxNum) * 100), "%")
        return GOLDDEPO
    if randomNum <= RES_FOOD_WEIGHT + RES_WOOD_WEIGHT:
        #print(".. resource roll: wood, chance: ", round((RES_WOOD_WEIGHT / maxNum) * 100), "%")
        return LOGGINGCAMP
    if randomNum <= RES_FOOD_WEIGHT + RES_WOOD_WEIGHT + RES_STONE_WEIGHT:
        #print(".. resource roll: stone, chance: ", round((RES_STONE_WEIGHT / maxNum) * 100), "%")
        return OREDEPO
        
    #print(".. resource roll: gold, chance: ", round((RES_GOLD_WEIGHT / maxNum) * 100), "%")
    return MANADEPO
    
def getResourceString(coordinates):

    if coordinates == GOLDDEPO:
        return colored("[CROP]", 'green')
        
    if coordinates == LOGGINGCAMP:
        return colored("[WOOD]", 'magenta')
        
    if coordinates == OREDEPO:
        return colored("[STONE]", 'cyan')
        
    if coordinates == MANADEPO:
        return colored("[GOLD]", 'yellow')
        
def incrementResourceStat(coordinates):

    global RES_COUNTER_FOOD
    global RES_COUNTER_WOOD
    global RES_COUNTER_STONE
    global RES_COUNTER_GOLD
    
    if coordinates == GOLDDEPO:
        RES_COUNTER_FOOD += 1
        
    if coordinates == LOGGINGCAMP:
        RES_COUNTER_WOOD += 1
        
    if coordinates == OREDEPO:
        RES_COUNTER_STONE += 1
        
    if coordinates == MANADEPO:
        RES_COUNTER_GOLD += 1
        
def getResourceChanceString(coordinates):

    maxNum = RES_FOOD_WEIGHT + RES_WOOD_WEIGHT + RES_STONE_WEIGHT + RES_GOLD_WEIGHT
    chance = ""
    
    if coordinates == GOLDDEPO:
        chance = colored(round((RES_FOOD_WEIGHT / maxNum) * 100), 'yellow')
        
    if coordinates == LOGGINGCAMP:
        chance = colored(round((RES_WOOD_WEIGHT / maxNum) * 100), 'yellow')
        
    if coordinates == OREDEPO:
        chance = colored(round((RES_STONE_WEIGHT / maxNum) * 100), 'yellow')
        
    if coordinates == MANADEPO:
        chance = colored(round((RES_GOLD_WEIGHT / maxNum) * 100), 'yellow')
        
    return chance
    
def tryToFindOptimalResource():
    
    tagHeight = RESOURCE_OWNER_BOX_BOTRIGHT[1] - RESOURCE_OWNER_BOX_TOPLEFT[1]
    tagWidth = RESOURCE_OWNER_BOX_BOTRIGHT[0] - RESOURCE_OWNER_BOX_TOPLEFT[0]
    
    tagRegion = (RESOURCE_OWNER_BOX_TOPLEFT[0], RESOURCE_OWNER_BOX_TOPLEFT[1], tagWidth, tagHeight)
    tagConfidence = 0.6
    
    numOfMarches = CURRENT_NUMBER_OF_MARCHES
    
    prio1Res = giveResourceToFarm()
    prio2Res = giveResourceToFarm()
    
    if prio1Res == prio2Res:
        prio2Res = giveResourceToFarm() # one last chance!
        
    print("> Probing for priority resource:", getResourceString(prio1Res), "alternative resource:", getResourceString(prio2Res), "")
    resourceIterator = 0
    
    # TRY TO FIND ALLY RESOURCE FOR PRIORITY ROLL
    while resourceIterator < 6:
        
        resourceIterator += 1
        
        click(SEARCH_BUTTON[0], SEARCH_BUTTON[1], 0.25)
        click(prio1Res[0], prio1Res[1], 0.25)
        posy = prio1Res[1] + int(SEARCH_DEPO_Y_OFFSET)
        click(prio1Res[0], posy, 1.5)
        
        if isSomeoneComing():
            continue  
        
        click(CENTER_OF_SCREEN[0], CENTER_OF_SCREEN[1], 0.5)
        
        try:
            pyautogui.locateOnScreen('ally_tag.png', region=tagRegion, confidence=tagConfidence)
            print("> Collecting", getResourceString(prio1Res), "weight", getResourceChanceString(prio1Res), "% on", colored("alliance", 'yellow'), "territory.")
            incrementResourceStat(prio1Res)
            return 1
        except pyautogui.ImageNotFoundException:
            pass
            
        
        
    resourceIterator = 0
    
        
        
    # TRY TO FIND ALLY RESOURCE FOR THE SECOND ROLL
    if prio1Res != prio2Res:
    
        while resourceIterator < 5:
        
            resourceIterator += 1
            
            click(SEARCH_BUTTON[0], SEARCH_BUTTON[1], 0.25)
            click(prio2Res[0], prio2Res[1], 0.25)
            posy = prio2Res[1] + int(SEARCH_DEPO_Y_OFFSET)
            click(prio2Res[0], posy, 1.5)
            
            if isSomeoneComing():
                continue
            
            click(CENTER_OF_SCREEN[0], CENTER_OF_SCREEN[1], 0.5)
            
            try:
                pyautogui.locateOnScreen('ally_tag.png', region=tagRegion, confidence=tagConfidence)
                print("> Collecting", getResourceString(prio2Res), "weight", getResourceChanceString(prio2Res), "% on", colored("alliance", 'yellow'), "territory.")
                incrementResourceStat(prio2Res)
                return 1
            except pyautogui.ImageNotFoundException:
                pass
                
            
    
    resourceIterator = 0
    
    # -------------- NEUTRAL AREA FINDER --------------
    
    while resourceIterator < 4:
        
        resourceIterator += 1
        
        click(SEARCH_BUTTON[0], SEARCH_BUTTON[1], 0.25)
        click(prio1Res[0], prio1Res[1], 0.25)
        posy = prio1Res[1] + int(SEARCH_DEPO_Y_OFFSET)
        click(prio1Res[0], posy, 1.5)
        
        if isSomeoneComing():
            continue
               
        
        click(CENTER_OF_SCREEN[0], CENTER_OF_SCREEN[1], 0.5)
            
        try:
            pyautogui.locateCenterOnScreen('none_tag.png', region=tagRegion, confidence=tagConfidence)
            print("> Collecting", getResourceString(prio1Res), "weight", getResourceChanceString(prio1Res), "% on", colored("neutral", 'cyan'), "territory.")
            incrementResourceStat(prio1Res)
            return 1
        except pyautogui.ImageNotFoundException:
            pass
            
        
        
    resourceIterator = 0
    
    # -------------- NEUTRAL AREA FINDER ALTERNATIVE RES --------------
    
    if prio1Res != prio2Res:
    
        while resourceIterator < 3:
        
            resourceIterator += 1
            
            click(SEARCH_BUTTON[0], SEARCH_BUTTON[1], 0.25)
            click(prio2Res[0], prio2Res[1], 0.25)
            posy = prio2Res[1] + int(SEARCH_DEPO_Y_OFFSET)
            click(prio2Res[0], posy, 1.5)
            
            if isSomeoneComing():
                continue
            
            click(CENTER_OF_SCREEN[0], CENTER_OF_SCREEN[1], 0.5)
            
            try:
                pyautogui.locateCenterOnScreen('ally_tag.png', region=tagRegion, confidence=tagConfidence)
                print("> Collecting", getResourceString(prio2Res), "weight", getResourceChanceString(prio2Res), "% on", colored("neutral", 'cyan'), "territory.")
                incrementResourceStat(prio2Res)
                return 1
            except pyautogui.ImageNotFoundException:
                pass
                
    
    resourceIterator = 0
    return 0
        
def getNumberOfAvailableMarches():
    return MAX_NUM_OF_MARCHES_TOTAL - CURRENT_NUMBER_OF_MARCHES + getNumberOfCalendarReservations()
    
def isSomeoneComing():
    
    region=(CENTER_OF_SCREEN[0] - 200, CENTER_OF_SCREEN[1] - 200, 400, 400)
    
    pyautogui.screenshot("center.png", region)
    
    templates = (cv2.imread('mark_self.png', cv2.IMREAD_UNCHANGED), cv2.imread('mark_ally.png', cv2.IMREAD_UNCHANGED), cv2.imread('mark_neutral.png', cv2.IMREAD_UNCHANGED))
    
    index = 0
    threshhold = 1
    found = False
    
    targetIndex = 0
    targetThreshold = -1
    
    while threshhold > 0.9 and found == False:
        while index < 2 and found == False:
            img = cv2.imread('center.png')
            
            hh, ww = templates[index].shape[:2]

            # extract base image and alpha channel and make alpha 3 channels
            base = templates[index][:,:,0:3]
            alpha = templates[index][:,:,3]
            alpha = cv2.merge([alpha,alpha,alpha])
            
            # do masked template matching and save correlation image
            correlation = cv2.matchTemplate(img, base, cv2.TM_CCORR_NORMED, mask=alpha)

            # set threshold and get all matches
            loc = np.where(correlation >= threshhold)
            
            result = img.copy()
            for pt in zip(*loc[::-1]):
                cv2.rectangle(result, pt, (pt[0]+ww, pt[1]+hh), (0,0,255), 1)
                found = True
                targetIndex = index
                targetThreshold = threshhold
                break
            index += 1
        
        if found == True:
            break
        index = 0
        threshhold -= 0.01
    
    perc = round(((0.1 - (1 - targetThreshold)) / 0.1) * 100)
    
    if not found:
        return False
    else:
    
        if targetIndex == 0:
            print(">>> Dbg: ", colored("self", 'yellow'), "is coming to node, abort", colored((round((perc), 'yellow'), "%.")))
        
        elif targetIndex == 1:
            print(">>> Dbg: ", colored("ally", 'yellow'), "is coming to node, abort", colored((round((perc), 'yellow'), "%.")))
        
        elif targetIndex == 2:
            print(">>> Dbg: ", colored("neutral", 'yellow'), "is coming to node, abort", colored((round((perc), 'yellow'), "%.")))
            
        return True
    
def manageBlacksmithProduction():
    # todo config
    chance = 30
    if random.randint(1, 100) > chance: # manage only sometimes, TODO move chance to config
        return 0
    
    
    print("> Managing blacksmith", colored((round((chance / 100) * 100)), 'yellow'), "%.")
    
    click(BLACKSMITH_POSITION[0],  BLACKSMITH_POSITION[1], 0.1)
    click(BLACKSMITH_POSITION[0],  BLACKSMITH_POSITION[1], 0.1)
    click(BLACKSMITH_POSITION[0],  BLACKSMITH_POSITION[1], 0.1)
    click(BLACKSMITH_POSITION[0],  BLACKSMITH_POSITION[1], 0.1)
    
    click(MATERIAL_PRODUCTION[0],  MATERIAL_PRODUCTION[1], 1.5)
    
    iterator = 0
    
    while iterator < 5:
        
        maxNum = MAT_LEATHER_WEIGHT + MAT_STONE_WEIGHT + MAT_WOOD_WEIGHT + MAT_BONE_WEIGHT
        randomNum = random.randint(1, maxNum)
        matPosition = (0,0)
        
        if randomNum <= MAT_LEATHER_WEIGHT:
            #print(".. material roll: leather, chance: ", round((MAT_LEATHER_WEIGHT / maxNum) * 100), "%")
            matPosition = MAT_LEATHER_POSITION
        elif randomNum <= MAT_LEATHER_WEIGHT + MAT_STONE_WEIGHT:
            #print(".. material roll: stone, chance: ", round((MAT_STONE_WEIGHT / maxNum) * 100), "%")
            matPosition = MAT_STONE_POSITION
        elif randomNum <= MAT_LEATHER_WEIGHT + MAT_STONE_WEIGHT + MAT_WOOD_WEIGHT:
            #print(".. material roll: wood, chance: ", round((MAT_WOOD_WEIGHT / maxNum) * 100), "%")
            matPosition = MAT_WOOD_POSITION
        else:
            #print(".. resource roll: bone, chance: ", round((MAT_BONE_WEIGHT / maxNum) * 100), "%")
            matPosition = MAT_BONE_POSITION
            
        click(matPosition[0], matPosition[1], 0.25)
        iterator += 1
    
    click(CITY_BUTTON[0], CITY_BUTTON[1], 0.5)
    return 0
    
    
def hitAllianceBuilding():
    click(ALLIANCE_BUILDING[0], ALLIANCE_BUILDING[1], 0.25)
    return 0

def minimizeGame():

    global END_STATE
    END_STATE = 1
    
    print("> Minimizing game.")
    pyautogui.press('F11')
    pyautogui.press('home')
    openTasksList()

    #loc = pyautogui.locateOnScreen('NOX_CLEARALL.png', confidence=0.75)
    #locPoint = pyautogui.center(loc)
    #click(locPoint[0], locPoint[1], 1)

    time.sleep(2)

    #homeButton()
    #click(TASKS_CLEARALL_BUTTON_NOX[0], TASKS_CLEARALL_BUTTON_NOX[1], 0.25)
    

    #minimizeWindow()
    #printExecutionTime()
    
def endGame():

    global END_STATE
    END_STATE = 0
    
    global RESTART_REQUIRED
    RESTART_REQUIRED = 1

    time.sleep(2)
    openTasksList()

    time.sleep(2)
    print("> Ending game.")
    pyautogui.press('F11')
    time.sleep(2)

    loc = pyautogui.locateOnScreen('NOX_CLEARALL.png', confidence=0.6)
    locPoint = pyautogui.center(loc)
    click(locPoint[0], locPoint[1], 1)

    time.sleep(2)
    
    #pyautogui.press('F11')
    #printExecutionTime()
    
def printExecutionTime():
    timeSpent = datetime.datetime.now() - EXECUTION_START
    print("> Execution time:", colored(timeSpent.seconds,'yellow'), "seconds.")
    
        
def openTasksList():
    pyautogui.keyDown('pgup')
    pyautogui.keyUp('pgup')
    
def homeButton():
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('shift')
    pyautogui.press('1')
    pyautogui.keyUp('ctrl')
    pyautogui.keyUp('shift')
    
def minimizeWindow():
    #EMULATOR
    time.sleep(0.5)
    pyautogui.keyDown('winleft')
    pyautogui.press('down')
    pyautogui.keyUp('winleft')
    
    time.sleep(0.5)
    #BLUE STACKX
    pyautogui.keyDown('winleft')
    pyautogui.press('down')
    pyautogui.keyUp('winleft')
    time.sleep(0.5)
    
def printMirkoBotHead():
    clear = lambda: os.system('cls')
    clear()
    print("--------------------------")
    print("-------", colored('MIRKO BOT', 'yellow'), "--------")
    print("--------------------------\n")
    
def getCurrentTimestamp():
    
    now = datetime.datetime.now()
    stringTimestamp = now.strftime("%H:%M:%S")
    
    return stringTimestamp

def loadConfigAndRun():
    global RESTART_REQUIRED

    RESTART_REQUIRED = 0

    loadMeasurementsFromFile()
    printMirkoBotHead()
    launchGame()
    returnVal = mainGameLoop()

    if returnVal == 0:  # reset req
        RESTART_REQUIRED = 1
        endGame()

    if returnVal == 1: # we can afk bit, life's good
        minimizeGame()
    
def loadConfigAndWait():
    loadMeasurementsFromFile()
    printMirkoBotHead()
    returnVal = mainGameLoop()


    if returnVal == 0: # reset req
        endGame()
    if returnVal == 1: # we can afk bit, life's good
        minimizeGame()
        time.sleep(600)

def mainGameLoop():

    errorCounter = 0

    # loop counter for safety reasons

    while(errorCounter < 3):
        workReturnVal = doWork()

        if workReturnVal == 0: # we need to restart the game
            return 0
        if workReturnVal == 1:
            break # one loop of work is enough for now?

    return 1

       #if isGameStateValid():
       #     notificationListenerLoop()
       #     errorCounter = 0
       # else:
       #     forceLaunchGame()
        #    errorCounter += 1
            
    #print(colored("> Something is not right, aborting.", 'red'))
    #input("Press enter to continue")

def forceLaunchGame():
    
    global RESTART_REQUIRED
    
    if RESTART_REQUIRED == 1:
        RESTART_REQUIRED = 0
        print(colored("> Game restarting.", 'red'))
        launchGame()
        
def isGameStateValid():
    return not RESTART_REQUIRED
    
def takeMeasurements():

    global RECEIVER_TELEGRAM_ID
    global TASKS_CLEARALL_BUTTON_NOX
    global NOTIFICATION_EXPECTED_NOX
    global NOTIFICATION_PX
    global NOTIFICATION_CLOSE
    global CITY_BUTTON
    global ALLIANCE_BUILDING
    global SCOUT_BUILDING
    global SCOUT_BUTTON
    global CENTER_OF_SCREEN
    global NEW_TROOPS
    global NEW_TROOPS_PX
    global REMOVE_COMMANDER
    global LAUNCH_MISSION
    global SEARCH_BUTTON
    global GOLDDEPO
    global LOGGINGCAMP
    global OREDEPO
    global MANADEPO
    global SEARCH_DEPO_Y_OFFSET
    global GATHER_BUTTON
    global BLACKSMITH_POSITION
    global MATERIAL_PRODUCTION
    global MAT_LEATHER_POSITION
    global MAT_STONE_POSITION
    global MAT_WOOD_POSITION
    global MAT_BONE_POSITION
    global TAVERN_POSITION
    global TAVERN_OPEN_INFO_POSITION
    global TAVERN_INFO_BACK_POSITION
    global TAVERN_OPEN_SILVER_BOTTOM_RIGHT_CORNER_POSITION
    global CURRENT_MARCHES_TOPLEFT
    global CURRENT_MARCHES_BOTTOMRIGHT
    global RESOURCE_OWNER_BOX_TOPLEFT
    global RESOURCE_OWNER_BOX_BOTRIGHT

    RECEIVER_TELEGRAM_ID        = input("Your telegram id: " )
    TASKS_CLEARALL_BUTTON_NOX   = measure("Clearall button bluestack!")
    NOTIFICATION_EXPECTED_NOX   = measure("Windows notification from bluestack, pixel color, point on colorful head")
    NOTIFICATION_PX             = pyautogui.pixel(NOTIFICATION_EXPECTED_NOX[0], NOTIFICATION_EXPECTED_NOX[1])
    NOTIFICATION_CLOSE          = measure("Close notification window (windows notification)")
    CITY_BUTTON                 = measure("City button NOX!")
    ALLIANCE_BUILDING           = measure("Alliance building!")
    CENTER_OF_SCREEN            = measure("Center of screen!")
    NEW_TROOPS                  = measure("New troops / HAS TO BE BLU! / fresh march!")
    NEW_TROOPS_PX               = pyautogui.pixel(NEW_TROOPS[0], NEW_TROOPS[1])
    REMOVE_COMMANDER            = measure("Remove commander!")
    LAUNCH_MISSION              = measure("Launch mission!")
    SEARCH_BUTTON               = measure(" Search button!")
    GOLDDEPO                    = measure("Cropland!")
    LOGGINGCAMP                 = measure("Logging camp!")
    OREDEPO                   = measure("Stone depo!")
    MANADEPO                    = measure("Gold depo!")
    SEARCH_DEPO_Y_OFFSET        = measureYoffset("Search resources button; y offset!")
    GATHER_BUTTON               = measure("Gather button!")
    BLACKSMITH_POSITION         = measure("Blacksmith position!")
    MATERIAL_PRODUCTION         = measure("Material production!")
    MAT_LEATHER_POSITION        = measure("Material leather position!")
    MAT_STONE_POSITION          = measure("Material stone position!")
    MAT_WOOD_POSITION           = measure("Material wood position!")
    MAT_BONE_POSITION           = measure("Material bone position!")
    TAVERN_POSITION             = measure("Tavern positiob!")
    TAVERN_OPEN_INFO_POSITION   = measure("Tavern open info position!")
    TAVERN_INFO_BACK_POSITION   = measure("Tavern go back position!")
    TAVERN_OPEN_SILVER_BOTTOM_RIGHT_CORNER_POSITION = measure("Tavern open silver chest bottom right corner position!")
    CURRENT_MARCHES_TOPLEFT     = measure("Current marches, top left, we going to create a box around the number!")
    CURRENT_MARCHES_BOTTOMRIGHT = measure("Current marches bottom right!")
    RESOURCE_OWNER_BOX_TOPLEFT  = measure("Resource owner box top left!")
    RESOURCE_OWNER_BOX_BOTRIGHT = measure("Resource owner box bottom right!")
    
    printMinimalMeasurementText()
    print("Disclaimer: check config.ini and fill the rest (e.g. game path)")
    input("Press enter to continue")

    
def measure(descriptor):
    printMinimalMeasurementText()
    input(descriptor)
    (x, y) = pyautogui.position()
    print("X: ", x," Y: ", y)
    time.sleep(MEASUREMENT_SLEEP_SECONDS)
    return (x,y)

def measureYoffset(descriptor):
    printMinimalMeasurementText()
    input(descriptor)
    (x, y) = pyautogui.position()
    print("Diff", y - GOLDDEPO[1])
    time.sleep(MEASUREMENT_SLEEP_SECONDS)
    return y - GOLDDEPO[1]
    
    
def saveMeasurementsToFile():
    config = configparser.ConfigParser()
    
    #TODO: SPLIT CATEGORIES
    config['GENERAL'] =  {
                        'RECEIVER_TELEGRAM_ID': str(RECEIVER_TELEGRAM_ID),
                        'CUSTOM_GAME_PATH': str(CUSTOM_GAME_PATH),
                        'CUSTOM_LAUNCH_SLEEPTIME': str(CUSTOM_LAUNCH_SLEEPTIME),
                       'TASKS_CLEARALL_BUTTON_NOX': str(TASKS_CLEARALL_BUTTON_NOX),
                       'NOTIFICATION_EXPECTED_NOX': str(NOTIFICATION_EXPECTED_NOX),
                       'NOTIFICATION_PX': str(NOTIFICATION_PX),
                       'NOTIFICATION_CLOSE': str(NOTIFICATION_CLOSE),
                       'CITY_BUTTON': str(CITY_BUTTON),
                       'ALLIANCE_BUILDING': str(ALLIANCE_BUILDING),
                       'SCOUT_BUILDING': str(SCOUT_BUILDING),
                        'SCOUT_BUTTON': str(SCOUT_BUTTON),
                       'CENTER_OF_SCREEN': str(CENTER_OF_SCREEN),
                       'NEW_TROOPS': str(NEW_TROOPS),
                       'NEW_TROOPS_PX': str(NEW_TROOPS_PX),
                       'REMOVE_COMMANDER': str(REMOVE_COMMANDER),
                       'LAUNCH_MISSION': str(LAUNCH_MISSION),
                       'SEARCH_BUTTON': str(SEARCH_BUTTON),
                       'CROPLAND': str(GOLDDEPO),
                       'LOGGINGCAMP': str(LOGGINGCAMP),
                       'STONEDEPO': str(OREDEPO),
                       'GOLDDEPO': str(MANADEPO),
                       'SEARCH_DEPO_Y_OFFSET': str(SEARCH_DEPO_Y_OFFSET),
                       'GATHER_BUTTON': str(GATHER_BUTTON),
                       'BLACKSMITH_POSITION': str(BLACKSMITH_POSITION),
                       'MATERIAL_PRODUCTION': str(MATERIAL_PRODUCTION),
                       'MAT_LEATHER_POSITION': str(MAT_LEATHER_POSITION),
                       'MAT_STONE_POSITION': str(MAT_STONE_POSITION),
                       'MAT_WOOD_POSITION': str(MAT_WOOD_POSITION),
                       'MAT_BONE_POSITION': str(MAT_BONE_POSITION),
                       'TAVERN_POSITION': str(TAVERN_POSITION),
                       'TAVERN_OPEN_INFO_POSITION': str(TAVERN_OPEN_INFO_POSITION),
                       'TAVERN_INFO_BACK_POSITION': str(TAVERN_INFO_BACK_POSITION),
                       'TAVERN_OPEN_SILVER_BOTTOM_RIGHT_CORNER_POSITION': str(TAVERN_OPEN_SILVER_BOTTOM_RIGHT_CORNER_POSITION),
                       'CURRENT_MARCHES_TOPLEFT': str(CURRENT_MARCHES_TOPLEFT),
                       'CURRENT_MARCHES_BOTTOMRIGHT': str(CURRENT_MARCHES_BOTTOMRIGHT),
                       'CLICK_TIME_MULTIPLIER': str(CLICK_TIME_MULTIPLIER),
                       'RESOURCE_OWNER_BOX_TOPLEFT': str(RESOURCE_OWNER_BOX_TOPLEFT),
                       'RESOURCE_OWNER_BOX_BOTRIGHT': str(RESOURCE_OWNER_BOX_BOTRIGHT)}
                       
    
    config['GAME'] =  {
                       'MAT_LEATHER_WEIGHT': str(MAT_LEATHER_WEIGHT),
                       'MAT_STONE_WEIGHT': str(MAT_STONE_WEIGHT),
                       'MAT_WOOD_WEIGHT': str(MAT_WOOD_WEIGHT),
                       'MAT_BONE_WEIGHT': str(MAT_BONE_WEIGHT),
                       'RES_FOOD_WEIGHT': str(RES_FOOD_WEIGHT),
                       'RES_WOOD_WEIGHT': str(RES_WOOD_WEIGHT),
                       'RES_STONE_WEIGHT': str(RES_STONE_WEIGHT),
                       'RES_GOLD_WEIGHT': str(RES_GOLD_WEIGHT),
                       'MAX_NUM_OF_MARCHES_TOTAL': str(MAX_NUM_OF_MARCHES_TOTAL),
                       'MAX_GATHERING_MARCHES_ALLOWED': str(MAX_GATHERING_MARCHES_ALLOWED)}
    
    
    with open('config_bot.ini', 'w') as configfile:
        config.write(configfile)
    
    clear = lambda: os.system('cls')
    clear()
    
def loadMeasurementsFromFile():
    
    global RECEIVER_TELEGRAM_ID
    global CUSTOM_GAME_PATH
    global CUSTOM_LAUNCH_SLEEPTIME
    global TASKS_CLEARALL_BUTTON_NOX
    global NOTIFICATION_EXPECTED_NOX
    global NOTIFICATION_PX
    global NOTIFICATION_CLOSE
    global CITY_BUTTON
    global ALLIANCE_BUILDING
    global SCOUT_BUILDING
    global SCOUT_BUTTON
    global CENTER_OF_SCREEN
    global NEW_TROOPS
    global NEW_TROOPS_PX
    global REMOVE_COMMANDER
    global LAUNCH_MISSION
    global SEARCH_BUTTON
    global GOLDDEPO
    global LOGGINGCAMP
    global OREDEPO

    global SWORDSMAN_CAMP
    global KNIGHT_CAMP
    global BALLISTA_FACTORY
    global ABBEY
    global TRAIN_OFFSET
    global SAFE_CITY_GOBACK

    global ALLIANCE_BUTTON
    global TERRITORY_BUTTON

    global MARCH_1_PRESET
    global MARCH_2_PRESET
    global MARCH_3_PRESET
    global MARCH_4_PRESET

    global TIER5_UNIT_POS

    global MANADEPO
    global SEARCH_DEPO_Y_OFFSET
    global GATHER_BUTTON
    global BLACKSMITH_POSITION
    global MATERIAL_PRODUCTION
    global MAT_LEATHER_POSITION
    global MAT_STONE_POSITION
    global MAT_WOOD_POSITION
    global MAT_BONE_POSITION
    
    global RESOURCE_OWNER_BOX_TOPLEFT
    global RESOURCE_OWNER_BOX_BOTRIGHT

    global MAT_LEATHER_WEIGHT
    global MAT_STONE_WEIGHT
    global MAT_WOOD_WEIGHT
    global MAT_BONE_WEIGHT

    global RES_FOOD_WEIGHT
    global RES_WOOD_WEIGHT
    global RES_STONE_WEIGHT
    global RES_GOLD_WEIGHT
    
    global MAX_NUM_OF_MARCHES_TOTAL
    global MAX_GATHERING_MARCHES_ALLOWED
    
    global TAVERN_POSITION
    global TAVERN_OPEN_INFO_POSITION
    global TAVERN_INFO_BACK_POSITION
    global TAVERN_OPEN_SILVER_BOTTOM_RIGHT_CORNER_POSITION
    
    global CURRENT_MARCHES_TOPLEFT
    global CURRENT_MARCHES_BOTTOMRIGHT
    
    global FREE_MARCHES_CALENDAR
    global CLICK_TIME_MULTIPLIER
    
    
    config = configparser.ConfigParser()
    config.read('config_bot.ini')
    
    RECEIVER_TELEGRAM_ID        = config['GENERAL']['RECEIVER_TELEGRAM_ID']
    CUSTOM_GAME_PATH            = config['GENERAL']['CUSTOM_GAME_PATH']
    CUSTOM_LAUNCH_SLEEPTIME     = int(config['GENERAL']['CUSTOM_LAUNCH_SLEEPTIME'])
    TASKS_CLEARALL_BUTTON_NOX   = strintToTouple(config['GENERAL']['TASKS_CLEARALL_BUTTON_NOX'])
    NOTIFICATION_EXPECTED_NOX   = strintToTouple(config['GENERAL']['NOTIFICATION_EXPECTED_NOX'])
    NOTIFICATION_PX             = strintToTouple(config['GENERAL']['NOTIFICATION_PX'])
    NOTIFICATION_CLOSE          = strintToTouple(config['GENERAL']['NOTIFICATION_CLOSE'])
    CITY_BUTTON                 = strintToTouple(config['GENERAL']['CITY_BUTTON'])
    ALLIANCE_BUILDING           = strintToTouple(config['GENERAL']['ALLIANCE_BUILDING'])
    SCOUT_BUILDING              = strintToTouple(config['GENERAL']['SCOUT_BUILDING'])
    SCOUT_BUTTON                = strintToTouple(config['GENERAL']['SCOUT_BUTTON'])

    SWORDSMAN_CAMP              = strintToTouple(config['GENERAL']['SWORDSMAN_CAMP'])
    KNIGHT_CAMP                 = strintToTouple(config['GENERAL']['KNIGHT_CAMP'])
    BALLISTA_FACTORY            = strintToTouple(config['GENERAL']['BALLISTA_FACTORY'])
    ABBEY                       = strintToTouple(config['GENERAL']['ABBEY'])
    TRAIN_OFFSET                = strintToTouple(config['GENERAL']['TRAIN_OFFSET'])
    SAFE_CITY_GOBACK            = strintToTouple(config['GENERAL']['SAFE_CITY_GOBACK'])

    CENTER_OF_SCREEN            = strintToTouple(config['GENERAL']['CENTER_OF_SCREEN'])
    NEW_TROOPS                  = strintToTouple(config['GENERAL']['NEW_TROOPS'])
    NEW_TROOPS_PX               = strintToTouple(config['GENERAL']['NEW_TROOPS_PX'])
    REMOVE_COMMANDER            = strintToTouple(config['GENERAL']['REMOVE_COMMANDER'])
    LAUNCH_MISSION              = strintToTouple(config['GENERAL']['LAUNCH_MISSION'])
    SEARCH_BUTTON               = strintToTouple(config['GENERAL']['SEARCH_BUTTON'])
    GOLDDEPO                    = strintToTouple(config['GENERAL']['CROPLAND'])
    LOGGINGCAMP                 = strintToTouple(config['GENERAL']['LOGGINGCAMP'])
    OREDEPO                   = strintToTouple(config['GENERAL']['STONEDEPO'])
    MANADEPO                    = strintToTouple(config['GENERAL']['GOLDDEPO'])

    MARCH_1_PRESET              = strintToTouple(config['GENERAL']['MARCH_1_PRESET'])
    MARCH_2_PRESET              = strintToTouple(config['GENERAL']['MARCH_2_PRESET'])
    MARCH_3_PRESET              = strintToTouple(config['GENERAL']['MARCH_3_PRESET'])
    MARCH_4_PRESET              = strintToTouple(config['GENERAL']['MARCH_4_PRESET'])

    ALLIANCE_BUTTON             = strintToTouple(config['GENERAL']['ALLIANCE_BUTTON'])
    TERRITORY_BUTTON            = strintToTouple(config['GENERAL']['TERRITORY_BUTTON'])

    TIER5_UNIT_POS              = strintToTouple(config['GENERAL']['TIER5_UNIT_POS'])

    SEARCH_DEPO_Y_OFFSET        = config['GENERAL']['SEARCH_DEPO_Y_OFFSET']
    GATHER_BUTTON               = strintToTouple(config['GENERAL']['GATHER_BUTTON'])
    BLACKSMITH_POSITION         = strintToTouple(config['GENERAL']['BLACKSMITH_POSITION'])
    MATERIAL_PRODUCTION         = strintToTouple(config['GENERAL']['MATERIAL_PRODUCTION'])
    CLICK_TIME_MULTIPLIER       = float(config['GENERAL']['CLICK_TIME_MULTIPLIER'])
    RESOURCE_OWNER_BOX_TOPLEFT  =strintToTouple(config['GENERAL']['RESOURCE_OWNER_BOX_TOPLEFT'])
    RESOURCE_OWNER_BOX_BOTRIGHT = strintToTouple(config['GENERAL']['RESOURCE_OWNER_BOX_BOTRIGHT'])
    
    MAT_LEATHER_POSITION        = strintToTouple(config['GENERAL']['MAT_LEATHER_POSITION'])
    MAT_STONE_POSITION          = strintToTouple(config['GENERAL']['MAT_STONE_POSITION'])
    MAT_WOOD_POSITION           = strintToTouple(config['GENERAL']['MAT_WOOD_POSITION'])
    MAT_BONE_POSITION           = strintToTouple(config['GENERAL']['MAT_BONE_POSITION'])
    
    MAT_LEATHER_WEIGHT          = int(config['GAME']['MAT_LEATHER_WEIGHT'])
    MAT_STONE_WEIGHT            = int(config['GAME']['MAT_STONE_WEIGHT'])
    MAT_WOOD_WEIGHT             = int(config['GAME']['MAT_WOOD_WEIGHT'])
    MAT_BONE_WEIGHT             = int(config['GAME']['MAT_BONE_WEIGHT'])

    RES_FOOD_WEIGHT             = int(config['GAME']['RES_FOOD_WEIGHT'])
    RES_WOOD_WEIGHT             = int(config['GAME']['RES_WOOD_WEIGHT'])
    RES_STONE_WEIGHT            = int(config['GAME']['RES_STONE_WEIGHT'])
    RES_GOLD_WEIGHT             = int(config['GAME']['RES_GOLD_WEIGHT'])
    
    TAVERN_POSITION             = strintToTouple(config['GENERAL']['TAVERN_POSITION'])
    TAVERN_OPEN_INFO_POSITION   = strintToTouple(config['GENERAL']['TAVERN_OPEN_INFO_POSITION'])
    TAVERN_INFO_BACK_POSITION   = strintToTouple(config['GENERAL']['TAVERN_INFO_BACK_POSITION'])
    TAVERN_OPEN_SILVER_BOTTOM_RIGHT_CORNER_POSITION = strintToTouple(config['GENERAL']['TAVERN_OPEN_SILVER_BOTTOM_RIGHT_CORNER_POSITION'])
    
    CURRENT_MARCHES_TOPLEFT   = strintToTouple(config['GENERAL']['CURRENT_MARCHES_TOPLEFT'])
    CURRENT_MARCHES_BOTTOMRIGHT   = strintToTouple(config['GENERAL']['CURRENT_MARCHES_BOTTOMRIGHT'])
    
    MAX_NUM_OF_MARCHES_TOTAL    = int(config['GAME']['MAX_NUM_OF_MARCHES_TOTAL'])
    MAX_GATHERING_MARCHES_ALLOWED = int(config['GAME']['MAX_GATHERING_MARCHES_ALLOWED'])
    
    reservedMarches = config.items("FREE_MARCHES_CALENDAR")
    for it, reservation in reservedMarches:
        FREE_MARCHES_CALENDAR.append(strintToTouple(reservation))
        
    
    
    
def strintToTouple(stringInput):
    stringInput1 = stringInput[1:-1]
    return tuple(map(int, stringInput1.split(', ')))

def printMinimalMeasurementText():
    clear = lambda: os.system('cls')
    clear()
    print("--------------------------")
    print("-- TAKING MEASUREMENTS! --")
    print("--------------------------\n")
    print("# Hover your mouse over, and press enter with proper position: \n")
    
    
def reportMousePosition(seconds=5000):
    for i in range(seconds):
        clear = lambda: os.system('cls')
        clear()
        
        print(pyautogui.position())
        x, y = pyautogui.position()
        px = pyautogui.pixel(getAdjustedX(x),y)
        print(type(px))
        print(px)
        time.sleep(1)
    
def getAdjustedX(xReq):
    # :) FIX FOR DISPLAY PORT DISCONNECTING MONITOR FROM OS WHEN TURNED OFF FOR SOME TIME
    # TODO: fix this like normal person, but not now
    #maxXStart = -1
    #maxXEnd = 0
    
    #pyautogui.size()[0]
    
    #for m in get_monitors():
    #    if m.x > maxXStart:
    #        maxXStart = m.x
    #        maxXEnd = m.width + maxXStart
    #        
    # maybe save monitor configuration to save file and calculate from that? for now constant
    #print(pyautogui.onScreen(xReq, y))
    
    #print(pyautogui.onScreen(xReq, 1))
    
    if pyautogui.onScreen(xReq, 1):
        return xReq
    return xReq - 1920

PRESTON_GARVEY_LIB = [
"Another settlement needs your help, I'll mark on your map.", 
"A month ago, there were twenty of us. Yesterday there were eight. Now, we're five.",
"Man, I don't know who you are, but your timing's impeccable.",
"Protect the people at a minute's notice.",
"The one good thing about being the last Minuteman is there's no one to argue with me when I say you're the new General.",
"I just saw you go toe-to-toe with a twenty foot tall irradiated lizard. You telling me you can't keep an open mind after that?",
"I had to put on a brave face as long as there were still people counting on me. That the only reason I kept going.",
"At least it's not raining.",
"There's another settlement that needs our help. I hope you can get to them quickly. We need to show people that the Minutemen are back.",
"This is going to be a black mark on the Minutemen forever. As glad as I am that the Institute is gone, this wasn't the plan. Dammit, General. You've dragged us down to their level. It didn't have to be this way.",
"Damn right. You don't go killing your friends without some better reason than they might be a synth.",
"These guys know how to make an entrance, no doubt about that. I wonder what they want?",
"I kind of doubt the Brotherhood's intentions are peaceful.",
"Is this...? Oh. I'm really sorry, General. Take all the time you need.",
"Selfish Bastards. They don't care about anybody except themselves.",
"I was having the best dream.",
"That was nice.",
"Good morning, love.",
"Time to get back to the real world, huh?",
"I never expected to fall in love with my commanding officer.",
"It's a little distracting, having you so close all the time.",
"I'm not sure if Minutemen regulations cover our situation.",
"Good lord... you people were savages.",
"That's it? Just gonna walk away?",
"Hey, up here! On the balcony!",
"Take it easy, Mama. You okay?",
"Take care of yourself.",
"Everybody just calm down.",
"We won't let anything happen to you.",
"You can't eat fresh air, after all."]   

def prestonGarveySaySomething():
    idx = random.randint(0, len(PRESTON_GARVEY_LIB) - 1)
    return PRESTON_GARVEY_LIB[idx]
    
if __name__ == "__main__":
    main()
    

    

    
    


