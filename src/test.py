lines = open('res/locations.txt').readlines()

s = ''
for line in lines:
    s+=line.split('\t')[1]

print(s)
