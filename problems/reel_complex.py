import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from manim import *
from sympy import symbols

from stepstack import StepStack

class ComplexIntegralReel(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # --------------------
        # Question
        # --------------------
        question = MathTex(
            r"Q:\ \int \frac{2x+3}{x^2+3x+2}\,dx",
            color=BLACK
        ).scale(1.5)

        question.move_to(UP*10 + LEFT*3)
        self.add(question)

        # --------------------
        # Right stack (ALGEBRA / DECOMPOSITION)
        # --------------------
        right_stack = StepStack(
            self,
            start_anchor=ORIGIN + UP*6 + RIGHT*4,
            align_edge=RIGHT,
            scale=1.05
        )

        # Start algebra steps centered
        fact = MathTex(r"x^2+3x+2 = (x+1)(x+2)", color=BLACK).scale(1.05)
        fact.move_to(ORIGIN + UP*5)
        self.play(Write(fact))

        pf = MathTex(
            r"\frac{2x+3}{(x+1)(x+2)} = \frac{1}{x+1} + \frac{1}{x+2}",
            color=BLACK
        ).scale(0.95)

        pf.next_to(fact, DOWN, buff=0.4)
        self.play(Write(pf))
        self.wait(0.3)

        # Move algebra to right stack
        alg_group = VGroup(fact, pf)
        self.play(
            alg_group.animate.move_to(right_stack.anchor),
            run_time=0.8
        )

        pf.next_to(fact, DOWN, buff=0.5)

        # Lock them into right stack
        right_stack.steps.extend([fact, pf])

        # --------------------
        # Left stack (INTEGRAL STEPS)
        # --------------------
        left_stack = StepStack(
            self,
            start_anchor=ORIGIN + UP*6 + LEFT*3.5,
            scale=1.35
        )

        left_stack.add(r"\int \frac{2x+3}{(x+1)(x+2)}\,dx")
        self.wait(0.3)

        left_stack.add(r"\int \frac{1}{x+1}\,dx + \int \frac{1}{x+2}\,dx")
        self.wait(0.3)

        # --------------------
        # Final answer (BOTTOM, PERSISTENT)
        # --------------------
        final = MathTex(
            r"\ln|x+1| + \ln|x+2| + C",
            color=BLACK
        ).scale(1.3)

        final.to_edge(DOWN, buff=0.7)
        self.play(Write(final))
        self.wait(2)
