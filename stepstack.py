from manim import *

class StepStack:
    def __init__(
        self,
        scene,
        start_anchor=ORIGIN,
        step_gap=0.65,
        align_edge=LEFT,
        scale=1.2,
        max_chars=28   # 👈 NEW
    ):
        self.scene = scene
        self.anchor = start_anchor
        self.step_gap = step_gap
        self.align_edge = align_edge
        self.scale = scale
        self.max_chars = max_chars
        self.steps = []

    def add(self, tex, animate=True):
        # auto-scale for long expressions
        scale = self.scale
        if len(tex) > self.max_chars:
            scale *= 0.75

        obj = MathTex(tex, color=WHITE).scale(scale)

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


