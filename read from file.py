def readfromfile():
    fo = open("count.txt")
    line = fo.read(10)
    fo.close()
    return int(line)


def writetofile(text):
    f = open('count.txt','w')
    f.write(str(text))
    f.close()


i = readfromfile()
print(i)
i+=1

print(i)

writetofile(i)
