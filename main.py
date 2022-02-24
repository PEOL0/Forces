import os
import math as m
from pyfiglet import Figlet
from alive_progress import alive_bar
import random

randomFlag = False
debugFlag = False

forceDict = {}
radDict = {}
forceKey = "force{}"
radKey = "angle{}"

xDict = {}
yDict = {}
xKey = "x{}"
yKey = "y{}"

forceSum = 0.0
forceSumAngle = 0.0

xSum = 0.0
ySum = 0.0

global xDictValues
global yDictValues


def defAndClear():
    global forceDict
    global radDict
    global forceKey
    global radKey

    global xDict
    global yDict
    global xKey
    global yKey

    global forceSum
    global forceSumAngle

    global xSum
    global ySum

    global xDictValues
    global yDictValues

    forceDict = {}
    radDict = {}
    forceKey = "force{}"
    radKey = "angle{}"

    xDict = {}
    yDict = {}
    xKey = "x{}"
    yKey = "y{}"

    forceSum = 0.0
    forceSumAngle = 0.0

    xSum = 0.0
    ySum = 0.0

    xDictValues = {}
    yDictValues = {}


def renderAscii(msg):
    terminal = os.get_terminal_size()
    welcome_fig = Figlet(
        font="kban", justify="left", width=getattr(terminal, "columns")
    )
    print()
    print(welcome_fig.renderText(msg))
    print('By: PEOL0', end='\n\n')
    print('Remember the math!', end='\n\n')


def inputForces():
    forces = input("Antal krafter: ").split()

    if "d" in forces:
        global debugFlag
        debugFlag = True

    if "r" in forces:
        global randomFlag
        randomFlag = True

    if randomFlag == True:
        with alive_bar(int(forces[0]) * 2) as bar:
            for each in range(int(forces[0])):
                updateForce(each)
                bar()
                updateAngle(each)
                bar()
    else:
        for each in range(int(forces[0])):
            updateForce(each)
            updateAngle(each)

    if debugFlag == True:
        print(forceDict)
        print(radDict)


def updateForce(each):
    newforce = random.uniform(-100, 100)
    if randomFlag != True:
        promt = "Storlek{}: "
        newforce = float(eval(input(promt.format(each + 1))))
    forceDict.update({forceKey.format(each + 1): newforce})
    if debugFlag == True:
        print(
            "Uppdaterat " +
            forceKey.format(each + 1) + " med värdet: " + str(newforce)
        )


def updateAngle(each):
    newangle = m.radians(random.uniform(0, 360))
    if randomFlag != True:
        prompt = "Vinkel{}: "
        newangle = m.radians(float(eval(input(prompt.format(each + 1)))))

    if newangle < 0:
        newangle = m.radians(360 + m.degrees(newangle))

    radDict.update({radKey.format(each + 1): newangle})
    if debugFlag == True:
        print("Uppdaterat " + radKey.format(each + 1) +
              " med värdet: " + str(newangle))


def split():
    with alive_bar(len(forceDict) * 2) as bar:
        for each in range(len(forceDict)):
            forceDictValues = list(forceDict.values())
            angleDictValues = list(radDict.values())
            xComponentSplit(each, forceDictValues[each], angleDictValues[each])
            bar()
            yComponentSplit(each, forceDictValues[each], angleDictValues[each])
            bar()


def xComponentSplit(index, force, rad):
    xComponent = round(abs(force * m.cos(rad)), 12)
    if m.degrees(rad) > 90 and m.degrees(rad) < 270:
        xComponent = round(-abs(xComponent), 12)
    xDict.update({xKey.format(index + 1): xComponent})
    if debugFlag == True:
        print("Uppdaterat " + xKey.format(index) +
              " med värdet: " + str(xComponent))


def yComponentSplit(index, force, rad):
    yComponent = round(abs(force * m.sin(rad)), 12)
    if m.degrees(rad) > 180 and m.degrees(rad) < 360:
        yComponent = round(-abs(yComponent), 12)
    yDict.update({yKey.format(index + 1): yComponent})
    if debugFlag == True:
        print("Uppdaterat " + yKey.format(index) +
              " med värdet: " + str(yComponent))


def method():
    method = input("Välj operation: ")
    if method == "" or method == "+":
        sum()


def sum():
    global forceSum
    global xSum
    global ySum
    global forceSumAngle

    xDictValues = list(xDict.values())
    yDictValues = list(yDict.values())

    xSum = m.fsum(xDictValues)
    ySum = m.fsum(yDictValues)

    forceSum = round(m.sqrt((xSum**2) + (ySum**2)), 12)

    if xSum != 0.0 and ySum != 0.0:
        forceSumAngle = m.atan(abs(ySum) / abs(xSum))
        if xSum < 0 and ySum > 0:
            forceSumAngle = m.radians(180) - forceSumAngle
        elif xSum < 0 and ySum < 0:
            forceSumAngle = m.radians(180) + forceSumAngle
        elif xSum > 0 and ySum < 0:
            forceSumAngle = m.radians(360) - forceSumAngle
    elif xSum == 0.0 and ySum != 0.0:
        if ySum > 0.0:
            forceSumAngle = m.radians(90)
        elif ySum < 0.0:
            forceSumAngle = m.radians(270)
    elif ySum == 0.0 and xSum != 0.0:
        if xSum > 0.0:
            forceSumAngle = m.radians(0.0)
        elif xSum < 0.0:
            forceSumAngle = m.radians(180.0)


def presentResults():
    print("Summa x: " + str(xSum))
    print("Summa y: " + str(ySum))
    print("Kraft: " + str(forceSum))
    print("Vinkel: " + str(m.degrees(forceSumAngle)))
    print()


renderAscii("Forces")
while True:
    defAndClear()

    inputForces()

    split()

    method()

    presentResults()
    if input() == "b":
        break
