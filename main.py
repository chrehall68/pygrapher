from io import TextIOWrapper
import numpy as np
from matplotlib import pyplot as plt


def sequential_access(file: TextIOWrapper, *items):
    curLine = file.readline().strip("\n")
    vars = []
    for requestedItem in items:
        if curLine[0 : len(requestedItem)] == requestedItem:
            vars.append(float(curLine.strip(requestedItem).strip()))
            print("ppended")
        curLine = file.readline().strip("\n")
    return vars


def process_coordinate(coord: str) -> tuple:
    x = coord[1 : coord.index(",")]
    y = coord[coord.index(",") + 1 : len(coord) - 1]
    return x, y


def getPositionTimeInfo(file: TextIOWrapper):
    curLine = file.readline().strip("\n")
    x = []
    y = []
    while curLine != "STOP":
        tempx, tempy = process_coordinate(curLine)
        x.append(float(tempx))
        y.append(float(tempy))
        curLine = file.readline().strip("\n")
    return np.array(x), np.array(y)


def label_axes(xname, yname, axis: plt.Axes):
    axis.set_xlabel(xname), axis.set_ylabel(yname)


def configureFigure(x, y, xlabel: str, ylabel: str, axis: plt.Axes):
    axis.set_xticks(range(round(min(x)), round(max(x)) + 1), minor=True)
    axis.set_yticks(range(round(min(y)) - 1, round(max(y)) + 1), minor=True)
    # print(help(axis.set_yticks))
    label_axes(xlabel, ylabel, axis)


def readInputText():
    inputFile = open("C:/projects/pygrapher/input.txt", "r")
    inputType = inputFile.readline().strip("\n").upper()
    print(inputType)
    figure, axis = plt.subplots(2, 2, gridspec_kw={"hspace": 0.5})

    if inputType == "POSITION TIME":
        choseDegree1 = False
        x, y = getPositionTimeInfo(inputFile)
        axis[0, 0].scatter(x, y)
        print("x is", x)
        print("y is", y)
        configureFigure(x, y, "time", "position", axis[0, 0])

        # decide if is constant velocity or constant acceleration:
        m, b = np.polyfit(x, y, 1)  # like y=mx+b, m = slope, b = y-intercept
        a, b, c = np.polyfit(x, y, 2)  # like ax^2 + bx + c
        degree_1_dif = 0
        degree_2_dif = 0
        for i in range(len(x)):
            degree_1_dif += abs(y[i] - (m * i + b))
            degree_2_dif += abs(y[i] - (a * i * i + b * i + c))

        if degree_1_dif < degree_2_dif:
            axis[0, 0].plot(x, m * x + b)
            choseDegree1 = True
        else:
            axis[0, 0].plot(x, a * x * x + b * x + c)
        print(choseDegree1)

        # graph (v vs time)
        if choseDegree1:
            y2 = [m for i in x]
            axis[0, 1].plot(x, y2)
            # because velocity is the slope of the line
            configureFigure(x, y, "time", "velocity", axis[0, 1])
        else:
            # because ax^2 + bx + c has an instantaneous slope of
            # a*2x + b
            y2 = [a * 2 * i + b for i in x]
            axis[0, 1].plot(x, y2)
            configureFigure(
                x,
                [min(0, min(y2)), max(y2) + 1],
                "time",
                "velocity",
                axis[0, 1],
            )

        # because a*2 is the slope for a*2x+b
        y3 = [a * 2 for i in x]
        axis[1, 0].plot(x, y3)
        configureFigure(
            x,
            [min(0, min(y3)) - 1, max(y3) + 1],
            "time",
            "acceleration",
            axis[1, 0],
        )

        print("FINAL RESULTS:")
        print("acceleration average is", a * 2, "which is about", round(a * 2))

        # (v0 + v2)/2
        print(
            "velocity average is",
            (y2[0] + y2[-1]) / 2,
            "which is about",
            round((y2[0] + y2[-1]) / 2),
        )

    elif inputType == "VELOCITY CONSTANTACCELERATION":
        v0, a, t, start_x_pos = sequential_access(
            inputFile, "V0", "A", "TIME", "X"
        )
        t = int(t)
        vlist = []
        tlist = []
        poslist = []
        alist = []
        if t != -1:
            for curtime in range(t + 1):
                vlist.append(v0 + a * curtime)
                tlist.append(curtime)
                poslist.append(start_x_pos + vlist[curtime])
        else:
            pos = start_x_pos
            tempv = curtime = 0
            while pos >= 0:
                tlist.append(curtime)
                tempv = v0 + a * curtime
                pos += tempv
                curtime += 1
                vlist.append(tempv)
                poslist.append(pos)
        alist = [a for time in tlist]

        # plot acceleration
        configureFigure(tlist, alist, "time", "acceleration", axis[1, 0])

        # plot velocity
        configureFigure(tlist, vlist, "time", "position", axis[0, 1])

        # plot position
        axis[0, 0].scatter(tlist, poslist)  # points
        configureFigure(tlist, vlist, "time", "position", axis[0, 0])  # line
        axis[0, 0].plot(tlist, [0 for time in tlist], "red")  # line for 0

    # finally, no matter which was input,
    # show graphs
    plt.show()
    inputFile.close()


readInputText()
