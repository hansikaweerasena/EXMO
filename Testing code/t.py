from Final_2 import senseTicTacBoard



def show(aa):
        print('-------------------')
        print(' ' + str(aa[6]) + ' | ' + str(aa[7]) + ' | ' + str(aa[8]))
        print('-------------------')
        print(' ' + str(aa[3]) + ' | ' + str(aa[4]) + ' | ' + str(aa[5]))
        print('-------------------')
        print(' ' + str(aa[0]) + ' | ' + str(aa[1]) + ' | ' + str(aa[2]))
        print('-------------------')

a = senseTicTacBoard()


show(a)