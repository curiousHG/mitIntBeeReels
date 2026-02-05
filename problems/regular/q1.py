import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[2]))

from manim import *

from stepstack import StepStack

SCRIPT= """
Solve this MIT Integration Bee Regular Season 2026 Problem 1.

Focus on the summation it is the e to the x to the 2026 in disguise.

Recognize this as x to the 2025 times e to the x to the 2026.

Substitute u equals x to the 2026.

The integral becomes one over 2026 times e to the u from 0 to 2026 to the 2026.

Final answer: one over 2026 times quantity e to the 2026 to the 2026 minus 1.
"""

class Q1Integral(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Voiceover sync timings (seconds)
        w_question = 2.4
        w_hint = 2.4
        w_s1 = 1.4
        w_s2 = 1.4
        w_s3 = 1.0
        w_int1 = 0.6
        w_sub = 1.0
        w_int2 = 0.8
        w_int3 = 0.8
        w_final = 7.9

        heading = Text(
            "MIT Integration Bee Regular Season 2026 Problem 1",
            color=WHITE,
        ).scale(0.6)
        heading.to_edge(UP, buff=0.28)
        self.play(FadeIn(heading, shift=DOWN * 0.2), run_time=0.6)

        # Question - appears immediately (0-2s)
        question = MathTex(
            r"Q:\ \int_{0}^{2026} \left( \sum_{k=0}^{\infty} \frac{x^{2026k+2025}}{k!} \right)\, dx",
            color=WHITE,
        ).scale(1.0)

        question.move_to(ORIGIN)
        self.play(Write(question), run_time=1.5)
        self.wait(w_question)

        self.play(question.animate.scale(0.9).next_to(heading, DOWN, buff=0.18), run_time=0.6)

        # Show the e^x series hint (2-5s)
        e_series = MathTex(
            r"e^x = \sum_{k=0}^{\infty} \frac{x^k}{k!}",
            color=YELLOW,
        ).scale(0.9)
        e_series.next_to(question, DOWN, buff=0.5)
        
        self.play(FadeIn(e_series), run_time=0.8)
        self.wait(w_hint)

        # Series rewriting (5-10s)
        s1 = MathTex(
            r"\sum_{k=0}^{\infty} \frac{x^{2026k+2025}}{k!}",
            color=WHITE,
        ).scale(0.95)
        
        s2 = MathTex(
            r"= x^{2025} \sum_{k=0}^{\infty} \frac{x^{2026k}}{k!}",
            color=WHITE,
        ).scale(0.95)
        
        s3 = MathTex(
            r"= x^{2025} e^{x^{2026}}",
            color=GREEN,
        ).scale(1.0)

        s1.next_to(e_series, DOWN, buff=0.5)
        self.play(Write(s1), run_time=0.8)
        self.wait(w_s1)
        
        s2.next_to(s1, DOWN, buff=0.35)
        self.play(Write(s2), run_time=0.8)
        self.wait(w_s2)
        
        s3.next_to(s2, DOWN, buff=0.35)
        self.play(Write(s3), run_time=1.0)
        self.wait(w_s3)

        # Fade out algebra, show integral steps (10-20s)
        self.play(
            FadeOut(e_series),
            FadeOut(s1),
            FadeOut(s2),
            run_time=1.5
        )


        # Rewrite integral
        int1 = MathTex(
            r"\int_{0}^{2026} x^{2025} e^{x^{2026}}\, dx",
            color=WHITE,
        ).scale(1.0)
        int1.move_to(ORIGIN)
        
        self.play(
            s3.animate.move_to(int1.get_center() - UP * 2),
            run_time=2.5
        )
        self.play(Transform(s3, int1), run_time=2.5)
        self.wait(w_int1)

        # Substitution (12.5-17s)
        sub = MathTex(
            r"u = x^{2026},\quad du = 2026 x^{2025}\, dx",
            color=BLUE,
        ).scale(0.9)
        sub.next_to(int1, DOWN, buff=0.6)
        self.play(Write(sub), run_time=2)
        self.wait(w_sub)

        # Transformed integral (15-20s)
        int2 = MathTex(
            r"= \frac{1}{2026} \int_{0}^{2026^{2026}} e^{u}\, du",
            color=WHITE,
        ).scale(1.0)
        int2.next_to(sub, DOWN, buff=0.6)
        self.play(Write(int2), run_time=1.2)
        self.wait(w_int2)

        # Evaluation (17.5-22s)
        int3 = MathTex(
            r"= \frac{1}{2026} \left[ e^{u} \right]_{0}^{2026^{2026}}",
            color=WHITE,
        ).scale(1.0)
        int3.next_to(int2, DOWN, buff=0.5)
        self.play(Write(int3), run_time=1.2)
        self.wait(w_int3)

        # Final answer (20-28s)
        self.play(
            FadeOut(s3),
            FadeOut(sub),
            FadeOut(int2),
            FadeOut(int3),
            run_time=0.5
        )
        
        final = MathTex(
            r"\boxed{\frac{1}{2026}\left(e^{2026^{2026}} - 1\right)}",
            color=YELLOW,
        ).scale(1.4)
        final.move_to(ORIGIN)
        
        self.play(Write(final), run_time=1.8)
        self.wait(w_final)