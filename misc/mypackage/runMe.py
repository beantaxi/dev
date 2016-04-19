from mypackage import api
from mypackage._HelperClass import HelperClass

a = api.createA()
a.test()

b = api.createB()
b.test()

c = api.createC()
c.test()

hc = HelperClass("I'm reachable too!")
hc.printMessage()

