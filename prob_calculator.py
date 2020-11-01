import copy
import random


class Hat:
    def __init__(self, **kwargs):
        self.balls = kwargs
        self.contents = []
        for key, value in kwargs.items():
            for i in range(value):
                self.contents.append(key)

    def draw(self, balls_to_draw, experimenting=False) -> [list, dict]:
        """
        Draws a random ball from the hat a given number of times.
        @param balls_to_draw: The number of times to draw a ball.
        @param experimenting: A boolean flag that controls the changes of the function based on whether or not it's
        being called from expiriment().
        @return: If experimenting=False, a string list of drawn balls if experimenting=True, a dictionary of drawn balls
        in the format {color: quantity}.
        """
        if experimenting:
            removed_balls = {}
            copied_contents_list = list(copy.deepcopy(self.contents))

            for i in range(balls_to_draw):
                try:
                    selected_ball = \
                        copied_contents_list.pop(copied_contents_list.index(random.choice(copied_contents_list)))
                except IndexError:
                    return removed_balls

                try:
                    removed_balls[selected_ball]
                except KeyError:
                    removed_balls[selected_ball] = 0
                finally:
                    removed_balls[selected_ball] += 1

            return removed_balls
        else:
            removed_balls = []
            copied_contents = copy.deepcopy(self.contents)

            if balls_to_draw <= len(copied_contents):

                for i in range(balls_to_draw):
                    removed_balls.append(copied_contents.pop(copied_contents.index(random.choice(copied_contents))))
                    self.contents = copied_contents

                return removed_balls

            else:
                return self.contents


def experiment(hat, expected_balls, num_balls_drawn, num_experiments) -> float:
    """
    Determines the probability of getting at least a given number of balls of any amount of given colors in at least
    one of a given number of hat draws.
    @param hat: The instance of class Hat from which to draw balls.
    @param expected_balls: A dictionary in the form {color: quantity} containing the ball color/quantity combinations
    being tested.
    @param num_balls_drawn: The number of times to draw a ball per experiment.
    @param num_experiments: The number of experiments to run.
    @return: A float representation of the probability.
    """
    matches = 0
    for i in range(num_experiments):
        actual_balls = hat.draw(num_balls_drawn, experimenting=True)
        actual_balls = {key: value for key, value in actual_balls.items() if key in expected_balls.keys()}
        if set(actual_balls.keys()) == set(expected_balls.keys()):
            for ball in actual_balls.keys():
                if actual_balls[ball] < expected_balls[ball]:
                    break
            else:
                matches += 1
        else:
            continue
    return matches / num_experiments
