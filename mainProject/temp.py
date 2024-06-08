file = open("requirements.txt" , 'r')

lines = file.readlines()

for i in lines : 
    print ( i.split('=')[0] , end=' ')
