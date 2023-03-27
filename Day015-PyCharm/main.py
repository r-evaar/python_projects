# TODO: [Func] Check sufficient resources
# TODO: [Func] Process coins
# TODO: -- How many pennies/nickels/dimes/quarters?
# TODO: -- Refund or return change based on value and sufficiency
# TODO: # [Func] Make a coffee and deduct resources
from time import sleep

def validated_input(prompt, condition, fail_prompt='INVALID INPUT', apply=None):
    while True:
        test = input(prompt)
        if condition(test):
            break
        else:
            print(fail_prompt)
    return test if apply is None else apply(test)


class CoffeeMachine:

    def __init__(self):
        self.resources = {'water': 300, 'milk': 200, 'coffee': 100, 'money': 0}
        self.options = ['espresso', 'latte', 'cappuccino']
        self.commands = ['report', 'exit']
        self.requirements = [
            {'water': 50,   'milk': 0,      'coffee': 18, 'money': 1.5},
            {'water': 200,  'milk': 150,    'coffee': 24, 'money': 2.5},
            {'water': 250,  'milk': 100,    'coffee': 24, 'money': 3.0}
        ]
        self.acceptedNames = ['Quarters', 'Dimes', 'Nickels', 'Pennies']
        self.acceptedValues = [.25, .1, .05, .01]

    @staticmethod
    def resource_string(resource, value):
        if resource in ['water', 'milk', 'coffee', 'report']:
            b = ''
            a = 'g' if resource == 'coffee' else 'ml'
        else:
            b = '$'
            a = ''

        resource = resource.capitalize()
        dash = '\t' * (2 - int((len(resource) + 2) / 4))

        value = f'{dash}{b}{value}{a}'

        return resource, value

    def print_resources(self):
        for resource, value in self.resources.items():
            resource, value = CoffeeMachine.resource_string(resource, value)
            print(f"{resource}: {value}")

    def prompt_coffee(self):
        prompt = '## Menu '+'#'*20+'\n'
        for option in self.options:
            price = self.requirements[self.options.index(option)]['money']
            dash = '\t' * (6 - int((len(option)) / 4))
            prompt += f' {option.capitalize()}{dash}${price}\n'
        prompt += '#' * 28 + '\n'
        prompt += '## What would you like to drink? '
        def condition(x): return x.lower() in self.options+self.commands
        def apply(x): return x.lower()

        return validated_input(prompt, condition, apply=apply)

    def prompt_payment(self):
        def condition(x): return x.isdigit()
        def apply(x): return float(x)

        payment = 0
        for i, coin in enumerate(self.acceptedNames):
            prompt = f'Please insert {coin}: '
            payment += self.acceptedValues[i] * validated_input(prompt, condition, apply=apply)

        print(f'Payment = ${payment:.2f}')
        return payment

    def process_coffee(self, requirements):
        for key in requirements:
            if key == 'money':
                self.resources[key] += requirements[key]
            else:
                self.resources[key] -= requirements[key]

    def process_response(self, response):
        requirements = self.requirements[self.options.index(response)]
        keys = requirements.keys()

        price = 0
        for key in keys:
            resource = self.resources[key]
            if key != 'money':
                if resource < requirements[key]:
                    print(f'Sorry: insufficient {key}' +
                          '. Please collect your money back.')
                    return
            else:
                price = requirements[key]

        payment = self.prompt_payment()
        if payment < price:
            print(f'Sorry: insufficient money' +
                  f'. ${price} is required for {response}' +
                  '. Please collect your money back.')
        else:
            print(f'Preparing {response} ..')
            self.process_coffee(requirements)
            sleep(1)
            print('Your coffee is ready!')
            remaining = payment-price
            if remaining > 0:
                print(f'Please take your change (${remaining:.2f}).')

    def run(self):
        while True:
            response = self.prompt_coffee()
            if response == 'report':
                self.print_resources()
            elif response == 'exit':
                break
            else:
                self.process_response(response)


if __name__ == "__main__":
    machine = CoffeeMachine()
    machine.run()
