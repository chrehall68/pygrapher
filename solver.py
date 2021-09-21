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


inputFile = open("./input.txt")
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

givenDict = {}
missingVars = ["X", "V0", "VX", "T", "A"]
for given in givens:
    givenDict[given] = inputLst[inputLst.index(given) + 1]
    if missingVars.index(given) != -1:
        missingVars.pop(missingVars.index(given))

print(givenDict)
print(missingVars)

# dependeing on what missingVars is, use the right equation
if "X" in missingVars:
    pass  # TODO


def solveForXNoA():
    #
    pass
