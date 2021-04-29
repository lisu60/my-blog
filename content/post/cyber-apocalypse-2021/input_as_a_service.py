#!/usr/bin/python2.7
from sys import version

'''
Descr:
In order to blend with the extraterrestrials, we need to talk and sound like them. Try some phrases in order to check if you can make them believe you are one of them. 
'''

def main():
    print version + '\nDo you sound like an alien?\n>>> \n'
    for _ in range(2):
        text = input(' ')
        print text

if __name__ == "__main__":
    main()

