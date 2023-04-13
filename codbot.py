import pyautogui
import time
import os
import configparser
import datetime
import random
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

END_STATE = 0
RESTART_REQUIRED = 0

def main():

    while 1:

        try:

            pyautogui.FAILSAFE = True
            printMirkoBotHead()
            print("1. Run MirkoBot and launch game.")
            print("2. Manual helper; print pos and color.\n")

            val1 = input("Continue with: ")
            clear = lambda: os.system('cls')
            clear()

            if val1 == "1":
                while 1:
                    loadConfigAndRun()

                    if isGameStateValid():
                        notificationListenerLoop()

            if val1 == "2":
                reportMousePosition()

        except:
            print('\n')
            logging.error(traceback.format_exc())
            val1 = input("\n Press enter to exit. :(")

#
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
    global CUSTOM_LAUNCH_SLEEPTIME

    DATE_LAST_ACTION = datetime.datetime.now()
    EXECUTION_START = datetime.datetime.now()

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

def doWork():

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

    if err >= 1:
        return 0

    return 1

def tryHelpAlliance():

    global CITY_BUTTON
    global ALLIANCE_BUTTON
    global TERRITORY_BUTTON

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
    global SWORDSMAN_CAMP
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
                time.sleep(0)
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

def click(xpos,ypos,length):
    
    #time.sleep(0.1)
    (x, y) = pyautogui.position()
    #time.sleep(0.1)

    pyautogui.click(getAdjustedX(xpos),ypos)
    # Move back to where the mouse was before click
    pyautogui.moveTo(x, y)
    
    time.sleep(length * CLICK_TIME_MULTIPLIER)


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

    time.sleep(2)
    
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
    print("-------", colored('OSKAR BOT', 'yellow'), "--------")
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

def forceLaunchGame():
    
    global RESTART_REQUIRED
    
    if RESTART_REQUIRED == 1:
        RESTART_REQUIRED = 0
        print(colored("> Game restarting.", 'red'))
        launchGame()
        
def isGameStateValid():
    return not RESTART_REQUIRED

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

    global RES_ORE_WEIGHT
    global RES_WOOD_WEIGHT
    global RES_MANA_WEIGHT
    global RES_GOLD_WEIGHT

    global CLICK_TIME_MULTIPLIER

    config = configparser.ConfigParser()
    config.read('config_bot.ini')

    CLICK_TIME_MULTIPLIER       = float(config['GENERAL']['CLICK_TIME_MULTIPLIER'])

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

    RES_ORE_WEIGHT             = int(config['GAME']['RES_ORE_WEIGHT'])
    RES_WOOD_WEIGHT             = int(config['GAME']['RES_WOOD_WEIGHT'])
    RES_MANA_WEIGHT            = int(config['GAME']['RES_MANA_WEIGHT'])
    RES_GOLD_WEIGHT             = int(config['GAME']['RES_GOLD_WEIGHT'])
    
def strintToTouple(stringInput):
    stringInput1 = stringInput[1:-1]
    return tuple(map(int, stringInput1.split(', ')))

    
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
    

    

    
    


