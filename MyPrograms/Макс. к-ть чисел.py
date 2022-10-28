n=str(input())
l=len(n)
start=int('1'+'0'*(l-1))
end=int('1'+'0'*l)
numbers=list(list(map(int,n)))
print(numbers)
m=[]
for number in range(start,end):
	number=str(number)
	temp=list(map(int,number))
	run=True
	for element in temp:
		if element not in numbers:
			run=False
	if run:
		m.append(int(number))
print(m)