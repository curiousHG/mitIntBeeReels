from manim import *
from sympy import symbols, integrate
from ..stepstack import StepStack

class ComplexIntegralReel(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        x = symbols("x")
        expr = (2*x + 3) / (x**2 + 3*x + 2)

        question = MathTex(
            r"Q:\ \int \frac{2x+3}{x^2+3x+2}\,dx",
            color=BLACK
        ).scale(0.85).to_corner(UL)

        self.add(question)

        steps = StepStack(self)

        steps.add(r"x^2 + 3x + 2 = (x+1)(x+2)")
        steps.add(r"\frac{2x+3}{(x+1)(x+2)}")
        steps.add(r"= \frac{1}{x+1} + \frac{1}{x+2}")
        steps.add(r"\int \frac{1}{x+1}\,dx + \int \frac{1}{x+2}\,dx")

        final = integrate(expr, x)

        final_tex = r"\ln|x+1| + \ln|x+2| + C"
        answer = MathTex(final_tex, color=BLACK).scale(1.1)
        answer.to_edge(DOWN)

        self.play(Write(answer))
        self.wait(2)
