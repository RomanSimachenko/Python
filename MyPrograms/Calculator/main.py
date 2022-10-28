import random
import colorama
from colorama import Fore,Back,Style,init
import datetime
from datetime import datetime

init(autoreset=True)
Act=True
on=True
active=True
s=0
a=0
b=0
k=0
search=0
dii=['+','-','*','/']

print("")
print(Style.BRIGHT + Back.RED + "Привiт. Тебе вiтає калькулятор Роми.")
print(Style.BRIGHT + Back.GREEN + "Щоб подивитись функцiї введiть - 'help'.")
print(Style.BRIGHT + Back.BLUE + "Перейти до калькулятора - 'continue'.")
n=input()
while on:
	if n=="help" or n=="con" or n=="cont" or n=="continue":
		on=False
	else:
		k+=1
		print(Style.BRIGHT + Fore.RED + "Невiрна команда!")
		print("")
		print(Style.BRIGHT + "Тiльки 'help' або 'continue':",end="")
		n=input()
		if k==3:
			print(Style.BRIGHT + Fore.RED + "Да скiльки можна?? Обираю команду автоматично!")
			n='help'
			on=False
			k=0
k=0
on=True
print("")
n=n.lower()

if n=="help":
	print(Style.BRIGHT + Fore.GREEN + "Всi можливi дiї:")
	print(Style.BRIGHT + Fore.GREEN + "'+' - Додавання.")
	print(Style.BRIGHT + Fore.GREEN + "'-' - Вiднiмання.")
	print(Style.BRIGHT + Fore.GREEN + "'*' - Множення.")
	print(Style.BRIGHT + Fore.GREEN + "'/' - Дiлення.")
	print(Style.BRIGHT + Fore.GREEN + "Щоб перейти до калькулятору введiть - 'continue'.")
	n1=input()
	while on:
		if n1=="continue" or n1=="cont" or n1=="con":
			on=False
		else:
			k+=1
			print(Style.BRIGHT + Fore.RED + "Невiрна команда!")
			print("")
			print(Style.BRIGHT + "Тiльки 'continue':",end="")
			n1=input()
			n1=n1.lower()
			if k==3:
				print(Style.BRIGHT + Fore.RED + "Да скiльки можна?? Обираю команду автоматично!")
				n1='continue'
				on=False
				k=0
on=True
k=0

print(Style.BRIGHT + Fore.BLUE + "Калькулятор:")
print(Style.BRIGHT + Fore.BLUE + "Введiть перше число:",end="")
a=input()
while on:
	try:
		a==int(a)
	except ValueError:
		k+=1
		print(Style.BRIGHT + Fore.RED + "Це не число!")
		if k==5:
			print(Style.BRIGHT + Fore.RED + "Да скiльки можна?? Обираю число автоматично!")
			a=random.randint(1,100)
			print(Style.BRIGHT + Fore.BLUE + "Перше число -",a)
			on=False
			k=0
		elif k!=5:
			print("")
			print(Style.BRIGHT + Fore.BLUE + "Введiть перше число:",end="")
			a=input()
	else:
		on=False
k=0
on=True

print(Style.BRIGHT + Fore.BLUE + "Дiя:",end="")
dia=input()
search=dii.count(dia)
while on:
	if search==1:
		on=False
	else:
		k+=1
		print(Style.BRIGHT + Fore.RED + "Невiрна дiя!")
		if k==5:
			print(Style.BRIGHT + Fore.RED + "Да скiльки можна?? Обираю дiю автоматично!")
			dia=random.choice(dii)
			print(Style.BRIGHT + Fore.BLUE + "Дiя -",dia)
			on=False
			k=0
		elif k!=5:
			print("")
			print(Style.BRIGHT + Fore.BLUE + "Перше число -",a)
			print(Style.BRIGHT + Fore.BLUE + "Введiть дiю:",end="")
			dia=input()
			search=dii.count(dia)
k=0
on=True

print(Style.BRIGHT + Fore.BLUE + "Введiть друге число:",end="")
b=input()
while on:
	try:
		b==int(b)
	except ValueError:
		k+=1
		print(Style.BRIGHT + Fore.RED + "Це не число!")
		if k==5:
			print(Style.BRIGHT + Fore.RED + "Да скiльки можна?? Обираю число автоматично!")
			b=random.randint(1,100)
			print(Style.BRIGHT + Fore.BLUE + "Друге число -",b)
			on=False
			k=0
		elif k!=5:
			print("")
			print(Style.BRIGHT + Fore.BLUE + "Перше число -",a)
			print(Style.BRIGHT + Fore.BLUE + "Дiя - '",dia,"'",sep="")
			print(Style.BRIGHT + Fore.BLUE + "Введiть друге число:",end="")
			b=input()
	else:
		on=False
k=0
on=True

while Act:
	if dia=="+":
		s=int(a)+int(b)
	if dia=="-":
		s=int(a)-int(b)
	if dia=="*":
		s=int(a)*int(b)
	if dia=="/":
		s=int(a)/int(b)
	print(a,dia,b,"=",s)
	a=s

	print(Style.BRIGHT + Fore.BLUE + "Для того, щоб вийти введiть - 'quit'. Iнакше, для продовження роботи, залиште поле пустим.")
	quit=input()
	if quit=="quit":
		Act=False
		print(Style.BRIGHT + Fore.RED + "До зустрiчi!")
		print("")
		print(Fore.RED + "    ##########")
		print(Fore.RED + "  ##############")
		print(Fore.RED + "  ################")
		print(Fore.RED + " ##################          ####")
		print(Fore.RED + "  ##################      ##########")
		print(Fore.RED + "  ##################    #############")
		print(Fore.RED + "   #################  ###############")
		print(Fore.RED + "    #################################")
		print(Fore.RED + "      ###############################")
		print(Fore.RED + "       #############################")
		print(Fore.RED + "        ##########################")
		print(Fore.RED + "          ########################")
		print(Fore.RED + "           #####################")
		print(Fore.RED + "            ##################")
		print(Fore.RED + "             ###############")
		print(Fore.RED + "               #############")
		print(Fore.RED + "                ##########")
		print(Fore.RED + "                 #######")
		print(Fore.RED + "                 ######")
		print(Fore.RED + "                  ####")
		print(Fore.RED + "                  ###")
		print(Fore.RED + "                   #")
		n=input("Натисніть 'Enter' для виходу.")

	else:
		on=True
		search=0
		print("")
		print(a)
		print(Style.BRIGHT + Fore.BLUE + "Дiя:",end="")
		dia=input()
		search=dii.count(dia)
		while on:
			if search==1:
				on=False
			else:
				k+=1
				print(Style.BRIGHT + Fore.RED + "Невiрна дiя!")
				if k==5:
					print(Style.BRIGHT + Fore.RED + "Да скiльки можна?? Обираю дiю автоматично!")
					dia=random.choice(dii)
					print(Style.BRIGHT + Fore.BLUE + "Дiя -",dia)
					on=False
					k=0
				elif k!=5:
					print("")
					print(Style.BRIGHT + Fore.BLUE + "Перше число -",a)
					print(Style.BRIGHT + Fore.BLUE + "Введiть дiю:")
					dia=input()
					search=dii.count(dia)
		on=True
		k=0

		print(Style.BRIGHT + Fore.BLUE + "Введiть друге число:",end="")
		b=input()
		while on:
			try:
				b==int(b)
			except ValueError:
				k+=1
				print(Style.BRIGHT + Fore.RED + "Це не число!")
				if k==5:
					print(Style.BRIGHT + Fore.RED + "Да скiльки можна?? Обираю число автоматично!")
					b=random.randint(1,100)
					print(Style.BRIGHT + Fore.BLUE + "Друге число -",b)
					on=False
					k=0
				elif k!=5:
					print("")
					print(Style.BRIGHT + Fore.BLUE + "Перше число -",a)
					print(Style.BRIGHT + Fore.BLUE + "Дiя - '",dia,"'",sep="")
					print(Style.BRIGHT + Fore.BLUE + "Введiть друге число:",end="")
					b=input()
			else:
				on=False