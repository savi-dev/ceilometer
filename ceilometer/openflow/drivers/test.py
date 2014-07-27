from ceilometer.openflow import drivers

class TestDriver(drivers.DriversBase):

    def __init__(self, abc):
        print "GOOD"
        print abc

    def testfunction(self, text):
        print text
        return text
