from manimlib import *

class Test(Scene):
    def construct(self):
        circle = Circle()
        self.play(ShowCreation(circle))
        self.wait(2)
        return super().construct()