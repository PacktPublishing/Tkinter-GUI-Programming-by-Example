class Dog:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print("Woof! My name is", self.name)


class Greyhound(Dog):
    def __init__(self, name):
        super().__init__(name)

    def speak(self):
        print("Zoom! My name is", self.name)

    def race(self, opponent):
        print(self.name, "is running faster than", opponent.name)

class JackRussell(Dog):
    def __init__(self, name, color):
        super().__init__(name)

        self.color = color

    def get_color(self):
        print(self.name, "is", self.color)


greyhound = Greyhound("Tessa")
jack_russell = JackRussell("Jack", "brown")
dog = Dog("Boris")

greyhound.speak()
jack_russell.speak()
dog.speak()

greyhound.race(jack_russell)
greyhound.race(dog)

jack_russell.get_color()

