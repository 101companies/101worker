import sys

if (len(sys.argv) == 2):
   result = open(sys.argv[1], 'w')
   result.write('This is a test.\n')
   sys.exit(0)
else:
   sys.exit(-1)
