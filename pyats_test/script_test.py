# Example
# -------
#
#   looping on container class instances

from pyats import aetest

# define a container & some inhabitants
class MyCommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def subsection_one(self):
        self.a = 1
        print('hello world')

    @aetest.subsection
    def subsection_two(self):
        assert self.a == 1

# let's instantiate the class
common_setup = MyCommonSetup()

# loop through to see what we get:
for i in common_setup:
    print(i)
    print(type(i))
# subsection_one
# subsection_two

result = common_setup()

print(result)
