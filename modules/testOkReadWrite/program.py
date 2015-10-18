import sys

if (len(sys.argv) == 3):
   arg = open(sys.argv[1], 'r')
   result = open(sys.argv[2], 'w')
   result.write('This is a test.\n')
   sys.exit(0)
else:
   sys.exit(-1)
