org = "arigtus.txt"
org2 = "ariach.txt"
org3 = "arigkugrs.txt"
org4 = "gimp.txt"
#tgt = "arirkst.txt"
#tgt = "arirkst.txt"
#tgt2 = "ari2kion.txt"

rkst = open(org)
orglines = []
with open(org) as src:
    for line in src:
        orglines.append(line)
#print(orglines)

org2lines = []
with open(org2) as t:
    for line in t:
        if(line in orglines):
            org2lines.append(line)

org3lines = []
with open(org3) as s:
    for line in s:
        if(line in org2lines):
            org3lines.append(line)
org4lines = []
with open(org4) as y:
    for line in y:
        if(line in org2lines):
            org4lines.append(line)

with open("primeanime.txt", mode='w') as f:
    for line in org3lines:
        f.write(line)

#rkstlines = rkst.readlines()
#lines_strip = [line.strip() for line in lines]
#print(lines_strip)


