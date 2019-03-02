org = "primeanime.txt"
org2 = "primeeiga.txt"

#tgt = "arirkst.txt"
tgt = "ariyrkn.txt"
tgt2 = "arirkst.txt"
tgt3 = "ariyysk.txt"
tgt4 = "nasi2.txt"
tgt5 = "nasi3.txt"

rkst = open(tgt)
orglines = []
with open(org) as src:
    for line in src:
        orglines.append(line)
#print(orglines)
count = 0 
with open(tgt) as t:
    for line in t:
        if(line in orglines):
            count +=1

print(count)

count = 0 
with open(tgt2) as t:
    for line in t:
        if(line in orglines):
            count +=1

print(count)

count = 0 
with open(tgt3) as t:
    for line in t:
        if(line in orglines):
            count +=1

print(count)

count = 0 
with open(tgt4) as t:
    for line in t:
        if(line in orglines):
            count +=1

print(count)

count = 0 
with open(tgt5) as t:
    for line in t:
        if(line in orglines):
            count +=1

print(count)


#rkstlines = rkst.readlines()
#lines_strip = [line.strip() for line in lines]
#print(lines_strip)


