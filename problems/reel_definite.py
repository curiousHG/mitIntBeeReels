import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from manim import *
from sympy import symbols, exp, integrate
from stepstack import StepStack

class DefiniteIntegralReel(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # Question
        question = MathTex(
            r"Q:\ \int_0^1 x e^{x^2}\,dx",
            color=BLACK
        ).scale(1.5)

        question.move_to(UP*10 + LEFT*3)
        self.add(question)

        

        right_stack = StepStack(
            self,
            start_anchor=ORIGIN + UP*6 + RIGHT*4,
            align_edge=RIGHT,
            scale=1.05
        )

        left_stack = StepStack(
            self,
            start_anchor=ORIGIN + UP*6 + LEFT*3.5,
            scale=1.4
        )

        # --- Substitution appears (center-ish)
        sub_u = MathTex(r"u = x^2", color=BLACK).scale(1.05)
        sub_du = MathTex(r"du = 2x\,dx", color=BLACK).scale(1.05)

        sub_u.move_to(ORIGIN + UP*5)
        sub_du.next_to(sub_u, DOWN, buff=0.4)

        self.play(Write(sub_u), Write(sub_du))
        self.wait(0.4)

        # Group substitution steps
        sub_group = VGroup(sub_u, sub_du)

        # Animate the whole group to the right stack
        self.play(
            sub_group.animate.move_to(right_stack.anchor),
            run_time=0.8
        )

        # Re-align inside the group AFTER move (important)
        sub_du.next_to(sub_u, DOWN, buff=0.5)

        # Lock into stack
        right_stack.steps.extend([sub_u, sub_du])

        left_stack.add(r"\int_0^1 x e^{x^2}\,dx")
        self.wait(0.3)

        left_stack.add(r"\frac{1}{2}\int_0^1 e^{u}\,du")
        self.wait(0.3)

        left_stack.add(r"\frac{1}{2} e^u \Big|_0^1")

        final = MathTex(
            r"\frac{1}{2}\left(e - 1\right)",
            color=BLACK
        ).scale(1.3)

        final.to_edge(DOWN, buff=0.7)
        self.play(Write(final))
        self.wait(2)
