import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[2]))
from manim import *

SCRIPT= """
Solve this MIT Integration Bee Regular Season 2026 Problem 2.

Split the integral into three separate parts.

Use the key formula: integral of one over a-e-to-the-x minus one equals log of a-e-to-the-x minus one, minus x.

Apply this formula to each term, with a equals 2 and a equals 3.

Evaluate at the bounds: log of 34 and 0.

Combine and simplify - notice the log 34 terms cancel out beautifully.

Final answer: log of 6767 over 2.
"""

class Q2Integral(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        
        # For vertical video (9:16 aspect ratio)
        config.frame_width = 7.5
        config.frame_height = 14
        
        # Voiceover sync timings (seconds) - ~45 sec total
        # Script breakdown: "Solve...Problem 2" (5s) + "Split..." (4s) + "Use formula..." (10s) 
        # + "Apply..." (5s) + "Evaluate..." (5s) + "Combine..." (6s) + "Final..." (10s)
        w_intro = 5.0      # "Solve this MIT..." (includes intro animation)
        w_split = 4.0      # "Split the integral into three separate parts"
        w_formula = 10.0   # "Use the key formula: integral of 1/(ae^x-1)..."
        w_apply = 5.0      # "Apply this formula to each term, with a=2 and a=3"
        w_evaluate = 5.0   # "Evaluate at the bounds: log(34) and 0"
        w_simplify = 6.0   # "Combine and simplify - notice the log 34 terms cancel"
        w_final = 10.0     # "Final answer: log of 6767 over 2" + viewing time
        
        # Heading - single line, starts centered
        heading = Text(
            "MIT Integration Bee Regular Season 2026 - Problem 2",
            color=WHITE,
            font_size=28
        )
        heading.move_to(UP * 1.5)
        
        # Question - starts centered
        question = MathTex(
            r"\int_{0}^{\log(34)} \left( 2 + \frac{1}{2e^{x}-1} + \frac{1}{3e^{x}-1} \right) dx",
            color=WHITE,
            font_size=60
        )
        question.next_to(heading, DOWN, buff=0.6)
        
        # Animate heading and question appearing in center
        self.play(
            FadeIn(heading, shift=DOWN * 0.2),
            run_time=0.8
        )
        self.play(Write(question), run_time=1.8)
        self.wait(1.2)  # Brief pause on question
        
        # Move both to top to make room for solution
        heading_final_pos = heading.copy().to_edge(UP, buff=0.25)
        question_final_pos = question.copy().next_to(heading_final_pos, DOWN, buff=0.4)
        
        self.play(
            heading.animate.move_to(heading_final_pos),
            question.animate.move_to(question_final_pos).scale(0.85),
            run_time=0.8
        )
        self.wait(w_intro - 4.6)
        
        # Split into three integrals - larger text
        split = VGroup(
            MathTex(r"= \int_{0}^{\log(34)} 2\, dx", color=BLUE, font_size=52),
            MathTex(r"+ \int_{0}^{\log(34)} \frac{1}{2e^{x}-1}\, dx", color=BLUE, font_size=52),
            MathTex(r"+ \int_{0}^{\log(34)} \frac{1}{3e^{x}-1}\, dx", color=BLUE, font_size=52),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        split.next_to(question, DOWN, buff=0.8)
        self.play(Write(split), run_time=2.0)
        self.wait(w_split - 2.0)
        
        # Show hint for 1/(ae^x - 1) integrals - larger
        hint_box = Rectangle(
            width=10.0, 
            height=1.3, 
            color=YELLOW,
            fill_opacity=0.15,
            stroke_width=3
        )
        hint = MathTex(
            r"\int \frac{1}{ae^{x}-1}\, dx = \log(ae^{x}-1) - x",
            color=YELLOW,
            font_size=54
        )
        hint_group = VGroup(hint_box, hint)
        hint_group.next_to(split, DOWN, buff=0.8)
        self.play(
            FadeIn(hint_box),
            Write(hint),
            run_time=2.0
        )
        self.wait(w_formula - 2.0)
        
        # Apply the formula to each term
        self.play(
            FadeOut(split), 
            FadeOut(hint_box),
            FadeOut(hint),
            run_time=0.6
        )
        
        applied = VGroup(
            MathTex(r"= \left[2x\right]_{0}^{\log(34)}", color=WHITE, font_size=54),
            MathTex(r"+ \left[\log(2e^{x}-1) - x\right]_{0}^{\log(34)}", color=WHITE, font_size=54),
            MathTex(r"+ \left[\log(3e^{x}-1) - x\right]_{0}^{\log(34)}", color=WHITE, font_size=54),
        ).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        applied.next_to(question, DOWN, buff=0.8)
        self.play(Write(applied), run_time=2.5)
        self.wait(w_apply - 2.5)
        
        # Evaluate at bounds
        self.play(FadeOut(applied), run_time=0.5)
        
        evaluation = VGroup(
            MathTex(r"= 2\log(34)", color=WHITE, font_size=52),
            MathTex(r"+ \left[\log(67) - \log(34)\right]", color=WHITE, font_size=52),
            MathTex(r"+ \left[\log(101) - \log(34) - \log(2)\right]", color=WHITE, font_size=52),
        ).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        evaluation.next_to(question, DOWN, buff=0.8)
        self.play(Write(evaluation), run_time=2.5)
        self.wait(w_evaluate - 2.5)
        
        # Simplify - show cancellation
        self.play(FadeOut(evaluation), run_time=0.5)
        
        simplified = MathTex(
            r"= \log(67) + \log(101) - \log(2)",
            color=GREEN,
            font_size=58
        )
        simplified.next_to(question, DOWN, buff=1.0)
        
        note = Text(
            "log(34) terms cancel!",
            color=YELLOW,
            font_size=38,
            slant=ITALIC
        )
        note.next_to(simplified, DOWN, buff=0.6)
        
        self.play(Write(simplified), run_time=2.0)
        self.play(FadeIn(note, shift=UP * 0.2), run_time=1.0)
        self.wait(w_simplify - 3.0)
        
        # Final answer - big and bold
        self.play(
            FadeOut(simplified),
            FadeOut(note),
            run_time=0.6
        )
        
        final = MathTex(
            r"\boxed{\log\left(\frac{6767}{2}\right)}",
            color=YELLOW,
            font_size=80
        )
        final.next_to(question, DOWN, buff=1.2)
        
        self.play(Write(final), run_time=2.5)
        self.wait(w_final - 2.5)
