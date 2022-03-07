import sys

# Local import
from Sorter import Sorter

def main():
    # instance class
    s = Sorter()

    # if there is more than on arg in command line
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = input('Enter path: ')  # ask to enter path

    #  if there is a tick -sf, do subfolder
    if len(sys.argv) > 2 and sys.argv[2] == '-s':
        s = s.SubfolderSort(path)
    else:
        s = s.Sort(path)


    # print sorter message if there is a return
    if not s == None: print(s)
        
    

# start the program
if __name__ == '__main__':
    main()