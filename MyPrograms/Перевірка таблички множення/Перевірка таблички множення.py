import random
import math
import colorama
from colorama import Fore,Style,Back,init
init(autoreset=True)
bal=0
d=True
print(Style.BRIGHT + Fore.BLUE + "Перевiрка таблички множення:")
for i in range(12):
	a=random.randint(1,9)
	b=random.randint(1,9)
	x=int(a)*int(b)
	c=str(a)+"*"+str(b)+":"
	n=input(c)
	try:
    		n=int(n)
	except ValueError:
    		print(Style.BRIGHT + Fore.RED + "Це не число!")
    		n=input(c)
	if x==int(n):
		bal+=1
		print(Style.BRIGHT + Fore.GREEN + "Вiрно!")
	else:
		print(Style.BRIGHT + Fore.RED + "Невiрно!")
print(Style.BRIGHT + Fore.BLUE + "Вашi бали - ",bal)

h=input("Натисніть будь-яку клавішу для виходу")
