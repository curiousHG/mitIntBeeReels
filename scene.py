from manim import *

class IntegrationReel(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        problem = MathTex(
            r"\int \frac{x}{x^2 + 1} \, dx",
            color=BLACK
        ).scale(1.4)

        idea = Text(
            "Use substitution",
            color=BLACK,
            font_size=36
        ).to_edge(UP)

        substitution = MathTex(
            r"u = x^2 + 1",
            color=BLACK
        ).next_to(problem, DOWN)

        derivative = MathTex(
            r"du = 2x\,dx",
            color=BLACK
        ).next_to(substitution, DOWN)

        result = MathTex(
            r"\frac{1}{2}\ln(x^2 + 1) + C",
            color=BLACK
        ).scale(1.4)

        self.play(Write(problem))
        self.wait(1)

        self.play(FadeIn(idea))
        self.wait(0.5)

        self.play(Write(substitution))
        self.wait(0.5)

        self.play(Write(derivative))
        self.wait(1)

        self.play(
            Transform(problem, result),
            FadeOut(substitution),
            FadeOut(derivative),
            FadeOut(idea),
        )

        self.wait(2)
