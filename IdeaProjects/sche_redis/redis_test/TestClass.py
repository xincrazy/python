__author__ = 'root'

#!/usr/bin/env python

class A(object):
    def __init__(self,a):
        self.a=a
    def speak(self):
        print self.a

if __name__ == '__main__':
    a=A(1)
    a.speak()