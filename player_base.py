from abc import ABC, abstractmethod
import glossary


def retry_fail(func):
    def inner(self, *args, **kwargs):
        while True:
            ans = func(self, *args, **kwargs)
            if ans:
                return ans
            self.print("There was a problem with the input. Please try again.")

    return inner

class PlayerBase(ABC):

    def verify_gestures(self, gest, num):
        if len(gest) != num:
            return False
        if any([x.lower() not in glossary.GESTURES for x in gest]):
            return False
        return gest

    def verify_list_item(self, choice, choices_list):
        if choice > len(choices_list):
            return False
        return choices_list[choice-1]

    @retry_fail
    def get_gestures(self, prompt, num):
        gest = self.get_input(prompt)
        gest = [x.strip().upper() for x in gest.split(',')]
        return self.verify_gestures(gest, num)

    @retry_fail
    def get_list_item(self, prompt, choices_list):
        self.print(prompt)
        for num, item in enumerate(choices_list):
            self.print('{}. {}'.format(num + 1, item))
        selection = int(self.get_input(""))
        return self.verify_list_item(selection, choices_list)

    @abstractmethod
    def get_input(self, prompt):
        pass

    @abstractmethod
    def print(self, prompt):
        pass