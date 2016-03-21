import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from firmware.firmwaretest import test
print "This is a test"


if __name__ == "__main__":

    print test()

