"""
Support for input such that
X (number) V0 (number) T (number) A (number) VX (number)
You only need to give 3 of them. Order doesn't matter
Only one problem solvable at a time.
No need to put all givens on the same line, but
DO NOT leave blank lines in between givens

Ex:
X 25 V0 0 A 10

Ex:
X -79 V0 0 A -9.81

Ex:
T 3 V0 22 VX 2
"""

# equations:
# (v_x)^2 = (v_0)^2 + 2ax
# x = (v_0)t + (1/2)a(t^2)
# v_x = v_0 + at
# x = (v_avg)t = (v_0 + v_x)/2 * t

import math as m


class One_D_Solver:
    def __init__(self, inputFileLocat: str):
        inputFile = open(inputFileLocat)
        inputLst = ""
        temp = inputFile.readline()
        while temp != "" and temp != "\n":
            inputLst += temp.strip("\n").strip()
            temp = inputFile.readline()
        inputFile.close()

        # process inputLst
        inputLst = inputLst.split(" ")

        givens = []
        for given in inputLst:
            # because we want to allow V0 even though 0 isn't alpha
            if given[0].isalpha():
                givens.append(given)

        self.givenDict = {}
        self.missingVars = ["X", "V0", "VX", "T", "A"]
        for given in givens:
            self.givenDict[given] = float(inputLst[inputLst.index(given) + 1])
            if self.missingVars.index(given) != -1:
                self.missingVars.pop(self.missingVars.index(given))

        print(self.givenDict)
        print(self.missingVars)

        self.solve()

    def solve(self):
        if len(self.missingVars) > 2:
            print("impossible to solve. Must have 3 givens.")
            return
        while len(self.missingVars) > 0:
            self.solveForX()
            self.solveForV0()
            self.solveForVX()
            self.solveForT()
            self.solveForA()
        print(self.givenDict)

    def solveForX(self):
        if "X" in self.givenDict:
            return
        keys = self.givenDict.keys()
        retVal = None
        if "V0" in keys and "VX" in keys and "T" in keys:
            # x = (v_0 + v_x)/2 * t
            retVal = (
                (self.givenDict["V0"] + self.givenDict["VX"])
                / 2
                * self.givenDict["T"]
            )
        elif "V0" in keys and "T" in keys and "A" in keys:
            # x = (v_0)t + (1/2)a(t^2)
            retVal = (
                self.givenDict["V0"] * self.givenDict["T"]
                + (self.givenDict["A"] * self.givenDict["T"] ** 2) / 2
            )
        elif "V0" in keys and "VX" in keys and "A" in keys:
            # (v_x)^2 = (v_0)^2 + 2ax
            # x = ((v_x)^2 - (v_0)^2)/2a
            retVal = (
                self.givenDict["VX"] ** 2 - self.givenDict["V0"] ** 2
            ) / (2 * self.givenDict["A"])

        if retVal:
            self.givenDict["X"] = retVal
            self.missingVars.remove("X")
        return retVal

    def solveForV0(self):
        if "V0" in self.givenDict:
            return
        keys = self.givenDict.keys()
        retVal = None
        if "VX" in keys and "A" in keys and "X" in keys:
            # (v_x)^2 = (v_0)^2 + 2ax
            # v_0 = sqrt(v_x^2 - 2ax)
            retVal = m.sqrt(
                self.givenDict["VX"] ** 2
                - (2 * self.givenDict["A"] * self.givenDict["X"])
            )
        if "X" in keys and "T" in keys and "A" in keys:
            # x = (v_0)t + (1/2)a(t^2)
            # v_0 = (x - (1/2)a(t^2))/t
            retVal = (
                self.givenDict["X"]
                - (self.givenDict["T"] ** 2 * self.givenDict["A"]) / 2
            ) / self.givenDict["T"]
        if "VX" in keys and "A" in keys and "T" in keys:
            # v_x = v_0 + at
            # v_0 = v_x - at
            retVal = (
                self.givenDict["VX"]
                - self.givenDict["A"] * self.givenDict["T"]
            )
        if "X" in keys and "V_X" in keys and "T" in keys:
            # x = (v_avg)t = (v_0 + v_x)/2 * t
            # v_0 = ((x/t) * 2) - v_x
            retVal = (
                self.givenDict["X"] / self.givenDict["T"] * 2
            ) - self.givenDict["VX"]
        if retVal:
            self.givenDict["V0"] = retVal
            self.missingVars.remove("V0")
        return retVal

    def solveForVX(self):
        if "VX" in self.givenDict:
            return
        keys = self.givenDict.keys()
        retVal = None
        if "V0" in keys and "A" in keys and "X" in keys:
            # (v_x)^2 = (v_0)^2 + 2ax
            retVal = m.sqrt(
                self.givenDict["V0"] ** 2
                + 2 * self.givenDict["X"] * self.givenDict["A"]
            )
        if "V0" in keys and "A" in keys and "T" in keys:
            # v_x = v_0 + at
            retVal = (
                self.givenDict["V0"]
                + self.givenDict["A"] * self.givenDict["T"]
            )
        if "X" in keys and "V0" in keys and "T" in keys:
            # x = (v_avg)t = (v_0 + v_x)/2 * t
            # v_x = x/t * 2 -v_0
            retVal = (
                self.givenDict["X"] / self.givenDict["T"] * 2
                - self.givenDict["V0"]
            )
        if retVal:
            self.givenDict["VX"] = retVal
            self.missingVars.remove("VX")
        return retVal

    def solveForT(self):
        if "T" in self.givenDict:
            return
        keys = self.givenDict.keys()
        retVal = None
        if "X" in keys and "V0" in keys and "A" in keys:
            # x = (v_0)t + (1/2)a(t^2)
            # 0 = (a/2)(t^2) + (v_0)t - x
            # t = (-v_0 +- sqrt(v_0^2 - 4 * (a/2) * (-x)))/a
            temp1 = (
                -self.givenDict["V0"]
                - m.sqrt(
                    self.givenDict["V0"] ** 2
                    - (4 * self.givenDict["A"] / 2 * (-self.givenDict["X"]))
                )
            ) / self.givenDict["A"]
            temp2 = (
                -self.givenDict["V0"]
                + m.sqrt(
                    self.givenDict["V0"] ** 2
                    - (4 * self.givenDict["A"] / 2 * (-self.givenDict["X"]))
                )
            ) / self.givenDict["A"]
            print("temp1 is ", temp1, "temp2 is", temp2)
            retVal = temp1 if temp1 > 0 else temp2
        if "VX" in keys and "V0" in keys and "A" in keys:
            # v_x = v_0 + at
            # t = (v_x - v_0)/a
            retVal = (
                self.givenDict["VX"] - self.givenDict["V0"]
            ) / self.givenDict["A"]
        if "V0" in keys and "VX" in keys and "X" in keys:
            # x = (v_avg)t = (v_0 + v_x)/2 * t
            # t = x*2 / (v_0 + v_x)
            retVal = (
                self.givenDict["X"]
                * 2
                / (self.givenDict["V0"] + self.givenDict["VX"])
            )
        if retVal:
            self.givenDict["T"] = retVal
            self.missingVars.remove("T")
        return retVal

    def solveForA(self):
        if "A" in self.givenDict:
            return

        keys = self.givenDict.keys()
        retVal = None
        if "VX" in keys and "V0" in keys and "X" in keys:
            # (v_x)^2 = (v_0)^2 + 2ax
            # x = (v_x^2 - v_0 ^2) / (2*a)
            retVal = (
                self.givenDict["VX"] ** 2 - self.givenDict["V0"] ** 2
            ) / (2 * self.givenDict["A"])
        if "V0" in keys and "T" in keys and "X" in keys:
            # x = (v_0)t + (1/2)a(t^2)
            # a = (x - (v_0 * t)) * 2 / (t^2)
            retVal = (
                (
                    self.givenDict["X"]
                    - self.givenDict["V0"] * self.givenDict["T"]
                )
                * 2
                / (self.givenDict["T"] ** 2)
            )
        if "VX" in keys and "V0" in keys and "T" in keys:
            # v_x = v_0 + at
            # a = (v_x - v_0)/t
            retVal = (
                self.givenDict["VX"] - self.givenDict["V0"]
            ) / self.givenDict["T"]
        if retVal:
            self.givenDict["A"] = retVal
            self.missingVars.remove("A")
        return retVal


mySolver = One_D_Solver("./input.txt")
