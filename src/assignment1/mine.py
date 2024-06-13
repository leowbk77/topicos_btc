import hashlib

pre = "10;leonardoferreira;;0000000ce5815cda4d32d7240e29daae39632ff58b1b511cf7b36cd90ec55002;"
x = 1

mined = False

while not mined:
	temp = pre + str(x)
	h = hashlib.sha256(temp.encode()).hexdigest()
	if h[:7] == '0000000':
		mined = True
	x+=1
print(h)
print(x)