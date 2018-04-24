class Dog:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print("Woof! My name is", self.name)


dog_one = Dog('Rover')
dog_two = Dog('Rex')

dog_one.speak()
dog_two.speak()
