from pprint import pprint
from LL1 import LL1
from read import readGrammer, readInput

myLL1 = LL1(*readGrammer('grammer1.txt'))
codes = myLL1.getThreeAddressCode(readInput('input.txt'))
#print("wdwad", codes)
print("\n\n\n")
for code in codes:
    print(code)