from manim import *

class StepStack:
    def __init__(
        self,
        scene,
        start_anchor=ORIGIN,
        step_gap=0.65,
        align_edge=LEFT,
        scale=1.2

    ):
        self.scene = scene
        self.anchor = start_anchor
        self.step_gap = step_gap
        self.align_edge = align_edge
        self.steps = []
        self.scale = scale

    def add(self, tex, animate=True):
        obj = MathTex(tex, color=BLACK).scale(self.scale)

        if not self.steps:
            obj.move_to(self.anchor)
        else:
            obj.next_to(self.steps[-1], DOWN, buff=self.step_gap)
            obj.align_to(self.steps[0], self.align_edge)

        if animate:
            self.scene.play(Write(obj))
        else:
            self.scene.add(obj)

        self.steps.append(obj)
        return obj

