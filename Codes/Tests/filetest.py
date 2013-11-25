f = open('polyline.html', 'r')
lines = list(f)
f.close()

f = open('polyline.html', 'w')
lines.insert(20, 'new line!!!!!!!!!!!\n')
for l in lines:
	f.write(l)
f.close()
