class Car:

    def __init__(self, **kw):
        self.make = kw["make"]
        self.model = kw.get('model')  # Using @get will return None if value does not exist

    def __str__(self):
        return ''.join([
            getattr(self, att)+' '
            for att in dir(self)
            if not att.startswith('__')
               and not callable(getattr(self, att))
               and getattr(self, att)  # if not None
        ])


car = Car(make="Nissan")
print(car)
print(car.model)
print(Car(make="Honda", model="Accord"))
# print(Car())  # Error
