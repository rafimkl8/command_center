from abc import ABC, abstractmethod

class JuiceMaker(ABC):

    @abstractmethod
    def juice_size(self):
        pass

    @staticmethod
    def juice_name(name):
        print(name)

class JuiceOne(JuiceMaker):

    def juice_size(self):
        print("400ml")        

class JuiceTwo(JuiceMaker):

    def juice_size(self):
        print("700ml")

# juice = JuiceMaker() # TypeError: Can't instantiate abstract class JuiceMaker without an implementation for abstract method 'juice_size'

juice1 = JuiceOne()
juice2 = JuiceTwo()

juice_list = [juice1, juice2]
for item in juice_list: item.juice_size()

JuiceMaker.juice_name("Orange")
