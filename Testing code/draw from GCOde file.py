from draw import plot

parser = argparse.ArgumentParser(description='This is a basic gcode sender. http://crcibernetica.com')
parser.add_argument('-p','--port',help='Input USB port',required=True)
parser.add_argument('-f','--file',help='Gcode file name',required=True)
args = parser.parse_args()

# plot("1.g",port)
# plot("2.g",port)
# plot("3.g",port)
# plot("4.g",port)
# plot("5.g",port)
# plot("6.g",port)
# plot("7.g",port)
# plot("8.g",port)
plot(args.file,args.port)


