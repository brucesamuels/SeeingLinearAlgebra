"""CP90: computing a cross product by cofactor expansion."""

from __future__ import annotations

import numpy as np

from manim import (
    Arrow3D,
    BLUE,
    Create,
    DashedLine,
    DEGREES,
    DOWN,
    FadeIn,
    FadeOut,
    GREEN,
    LEFT,
    Line,
    MathTex,
    ORANGE,
    RED,
    ReplacementTransform,
    RIGHT,
    SurroundingRectangle,
    Text,
    ThreeDAxes,
    ThreeDScene,
    Transform,
    TransformFromCopy,
    UP,
    VGroup,
    WHITE,
    YELLOW,
)

from engine.cross_product_computation import CrossProductComputation


class CrossProductComputationPresentation(ThreeDScene):
    TITLE = "How Do We Compute a Cross Product?"

    def construct(self) -> None:
        s = CrossProductComputation().snapshot()

        title = Text(self.TITLE, font_size=40).to_edge(UP)
        subtitle = Text(
            "We know what it represents. Now let us calculate it.",
            font_size=24,
        ).next_to(title, DOWN, buff=0.16)

        self.add_fixed_in_frame_mobjects(title, subtitle)
        self.play(FadeIn(title), FadeIn(subtitle))

        vectors = self._vector_display()
        prompt = Text(
            "Can the perpendicular vector be computed from coordinates?",
            font_size=26,
            color=YELLOW,
        ).to_edge(DOWN).shift(UP * 0.28)

        self.add_fixed_in_frame_mobjects(vectors, prompt)
        self.play(FadeIn(vectors), FadeIn(prompt))
        self.wait(1.1)
        self.play(FadeOut(prompt))

        determinant = self._determinant_display()
        determinant.shift(DOWN * 0.10)
        self.add_fixed_in_frame_mobjects(determinant)

        self.play(ReplacementTransform(vectors, determinant))
        self.wait(0.8)

        i_term = self._show_minor_step(
            determinant,
            component=r"\mathbf{i}",
            minor_tex=r"\begin{vmatrix}1&3\\4&2\end{vmatrix}",
            work_tex=r"(1)(2)-(3)(4)=-10",
            result_tex=r"-10\mathbf{i}",
            color=RED,
            box_index=0,
        )

        j_term = self._show_minor_step(
            determinant,
            component=r"-\mathbf{j}",
            minor_tex=r"\begin{vmatrix}2&3\\1&2\end{vmatrix}",
            work_tex=r"-\big((2)(2)-(3)(1)\big)=-1",
            result_tex=r"-\mathbf{j}",
            color=GREEN,
            box_index=1,
            emphasize_minus=True,
        )

        k_term = self._show_minor_step(
            determinant,
            component=r"\mathbf{k}",
            minor_tex=r"\begin{vmatrix}2&1\\1&4\end{vmatrix}",
            work_tex=r"(2)(4)-(1)(1)=7",
            result_tex=r"7\mathbf{k}",
            color=BLUE,
            box_index=2,
        )

        assembled = MathTex(
            r"-10\mathbf{i}-\mathbf{j}+7\mathbf{k}",
            font_size=42,
        ).shift(DOWN * 1.00)

        vector_form_label = Text(
            "Vector form",
            font_size=27,
            color=YELLOW,
        ).next_to(assembled, UP, buff=0.28)

        self.add_fixed_in_frame_mobjects(assembled, vector_form_label)
        self.play(
            FadeOut(determinant),
            ReplacementTransform(VGroup(i_term, j_term, k_term), assembled),
            FadeIn(vector_form_label),
        )
        self.wait(1.2)

        # Remove both mobjects completely before creating the coordinate form.
        self.play(FadeOut(assembled), FadeOut(vector_form_label))
        self.remove_fixed_in_frame_mobjects(assembled, vector_form_label)
        self.remove(assembled, vector_form_label)
        self.wait(0.25)

        coordinate = MathTex(
            r"\begin{bmatrix}-10\\-1\\7\end{bmatrix}",
            font_size=48,
        ).shift(DOWN * 0.20)
        coordinate_label = Text(
            "Coordinate form",
            font_size=27,
            color=YELLOW,
        ).next_to(coordinate, UP, buff=0.28)

        self.add_fixed_in_frame_mobjects(coordinate, coordinate_label)
        self.play(FadeIn(coordinate), FadeIn(coordinate_label))
        self.wait(1.2)
        self.play(FadeOut(coordinate), FadeOut(coordinate_label))
        self.remove_fixed_in_frame_mobjects(coordinate, coordinate_label)
        self.remove(coordinate, coordinate_label)
        self.play(FadeOut(subtitle))
        self.remove_fixed_in_frame_mobjects(subtitle)
        self.remove(subtitle)
        self.wait(0.25)

        self._show_cross_hatch_shortcut(s)
        self._show_dot_product_verification(s)
        self._show_geometry(s)
        self._show_reflection()
        self.wait(1.4)

    def _show_minor_step(
        self,
        determinant,
        *,
        component,
        minor_tex,
        work_tex,
        result_tex,
        color,
        box_index,
        emphasize_minus=False,
    ):
        boxes = [
            SurroundingRectangle(determinant[0], color=RED, buff=0.10),
            SurroundingRectangle(determinant[1], color=GREEN, buff=0.10),
            SurroundingRectangle(determinant[2], color=BLUE, buff=0.10),
        ]

        heading = MathTex(component, font_size=40, color=color)
        minor = MathTex(minor_tex, font_size=44, color=color)
        work = MathTex(work_tex, font_size=34)
        result = MathTex(result_tex, font_size=40, color=color)

        group = VGroup(heading, minor, work, result).arrange(
            DOWN,
            buff=0.22,
        ).to_edge(RIGHT).shift(LEFT * 0.35 + DOWN * 0.18)

        if emphasize_minus:
            minus_note = Text(
                "The middle cofactor carries a minus sign.",
                font_size=23,
                color=YELLOW,
            ).next_to(group, DOWN, buff=0.18)
            group.add(minus_note)

        self.add_fixed_in_frame_mobjects(boxes[box_index], group)

        self.play(FadeIn(boxes[box_index]), FadeIn(heading))
        self.play(FadeIn(minor))
        self.play(FadeIn(work))
        if emphasize_minus:
            self.wait(0.6)
        self.play(FadeIn(result))
        self.wait(0.8)
        self.play(FadeOut(boxes[box_index]), FadeOut(group[:-1] if emphasize_minus else group))
        if emphasize_minus:
            self.play(FadeOut(group[-1]))

        compact = MathTex(result_tex, font_size=36, color=color)
        compact_positions = [LEFT * 2.1, np.zeros(3), RIGHT * 2.1]
        compact.move_to(DOWN * 2.10 + compact_positions[box_index])
        self.add_fixed_in_frame_mobjects(compact)
        self.play(FadeIn(compact))
        return compact


    def _show_cross_hatch_shortcut(self, s) -> None:
        self._show_cofactor_derivation()
        self._show_cross_hatch_computation()

    @staticmethod
    def _manual_grid(rows, *, column_spacing, row_spacing):
        row_groups = []
        entry_rows = []
        for row in rows:
            entries = [MathTex(value, font_size=38) for value in row]
            entry_rows.append(entries)
            row_groups.append(VGroup(*entries).arrange(RIGHT, buff=column_spacing))
        grid = VGroup(*row_groups).arrange(DOWN, buff=row_spacing, aligned_edge=LEFT)
        widest = max(group.width for group in row_groups)
        for group in row_groups:
            group.shift(LEFT * (group.width - widest) / 2)
        return grid, entry_rows

    def _show_cofactor_derivation(self) -> None:
        heading = Text("Where Do the Cofactors Come From?", font_size=35, color=YELLOW).to_edge(UP).shift(DOWN * 0.65)
        grid, entry_rows = self._manual_grid([
            [r"\mathbf{i}", r"\mathbf{j}", r"\mathbf{k}"],
            ["2", "1", "3"],
            ["1", "4", "2"],
        ], column_spacing=0.82, row_spacing=0.34)
        grid.scale(1.05).shift(UP * 0.52)
        entry_rows[0][0].set_color(RED); entry_rows[0][1].set_color(GREEN); entry_rows[0][2].set_color(BLUE)
        top = grid.get_top() + UP * 0.15; bottom = grid.get_bottom() + DOWN * 0.15
        left_bar = Line([grid.get_left()[0]-0.36, top[1], 0], [grid.get_left()[0]-0.36, bottom[1], 0], stroke_width=5)
        right_bar = Line([grid.get_right()[0]+0.36, top[1], 0], [grid.get_right()[0]+0.36, bottom[1], 0], stroke_width=5)
        determinant = VGroup(left_bar, grid, right_bar)
        signs = MathTex(r"+\qquad-\qquad+", font_size=36, color=YELLOW).next_to(grid, UP, buff=0.22)
        directions = Text("Delete one column. The four remaining numbers form the minor.", font_size=24).next_to(grid, DOWN, buff=0.34)
        self.add_fixed_in_frame_mobjects(heading, determinant, signs, directions)
        self.play(FadeIn(heading), FadeIn(determinant)); self.play(FadeIn(signs), FadeIn(directions)); self.wait(0.8)
        columns=[VGroup(entry_rows[0][c], entry_rows[1][c], entry_rows[2][c]) for c in range(3)]
        data=(
            (0,RED,r"+\mathbf{i}",[["1","3"],["4","2"]],r"(1)(2)-(3)(4)=-10",r"-10\mathbf{i}"),
            (1,GREEN,r"-\mathbf{j}",[["2","3"],["1","2"]],r"-\big((2)(2)-(3)(1)\big)=-1",r"-\mathbf{j}"),
            (2,BLUE,r"+\mathbf{k}",[["2","1"],["1","4"]],r"(2)(4)-(1)(1)=7",r"7\mathbf{k}"),
        )
        compact_terms=[]
        for c,color,basis_tex,minor_rows,work_tex,result_tex in data:
            deleted=columns[c]
            col_box=SurroundingRectangle(deleted,color=color,buff=0.10,stroke_width=4)
            surviving=[entry_rows[r][col] for r in (1,2) for col in range(3) if col!=c]
            surviving_group=VGroup(*surviving)
            surviving_boxes=VGroup(*[SurroundingRectangle(e,color=color,buff=0.07,stroke_width=3) for e in surviving])
            basis=MathTex(basis_tex,font_size=40,color=color).to_edge(LEFT).shift(RIGHT*1.12+DOWN*1.62)
            arrow=MathTex(r"\Longrightarrow",font_size=42,color=color).next_to(basis,RIGHT,buff=0.25)
            minor_grid,_=self._manual_grid(minor_rows,column_spacing=0.54,row_spacing=0.26)
            minor_grid.scale(0.92).next_to(arrow,RIGHT,buff=0.32)
            mt=minor_grid.get_top()+UP*0.10; mb=minor_grid.get_bottom()+DOWN*0.10
            ml=Line([minor_grid.get_left()[0]-0.25,mt[1],0],[minor_grid.get_left()[0]-0.25,mb[1],0],color=color,stroke_width=4)
            mr=Line([minor_grid.get_right()[0]+0.25,mt[1],0],[minor_grid.get_right()[0]+0.25,mb[1],0],color=color,stroke_width=4)
            minor=VGroup(ml,minor_grid,mr)
            work=MathTex(work_tex,font_size=31,color=color).to_edge(DOWN).shift(UP*0.30)
            result=MathTex(result_tex,font_size=36,color=color).next_to(work,RIGHT,buff=0.45)
            self.add_fixed_in_frame_mobjects(col_box,surviving_boxes,basis,arrow,minor,work,result)
            self.play(Create(col_box), *[Create(box) for box in surviving_boxes]); self.wait(0.45)
            self.play(deleted.animate.set_opacity(0.16), FadeIn(basis), FadeIn(arrow), TransformFromCopy(surviving_group,minor_grid), FadeIn(ml), FadeIn(mr)); self.wait(0.55)
            self.play(FadeIn(work),FadeIn(result)); self.wait(0.95)
            compact=MathTex(result_tex,font_size=34,color=color).move_to(DOWN*2.15+[LEFT*2.15,0,RIGHT*2.15][c])
            self.add_fixed_in_frame_mobjects(compact); self.play(FadeIn(compact)); compact_terms.append(compact)
            self.play(FadeOut(col_box),FadeOut(surviving_boxes),FadeOut(basis),FadeOut(arrow),FadeOut(minor),FadeOut(work),FadeOut(result),deleted.animate.set_opacity(1.0))
            self.remove_fixed_in_frame_mobjects(col_box,surviving_boxes,basis,arrow,minor,work,result)
            self.remove(col_box,surviving_boxes,basis,arrow,minor,work,result)
        assembled=MathTex(r"-10\mathbf{i}-\mathbf{j}+7\mathbf{k}",font_size=43).shift(DOWN*1.00)
        assembled.set_color_by_tex(r"\mathbf{i}",RED); assembled.set_color_by_tex(r"\mathbf{j}",GREEN); assembled.set_color_by_tex(r"\mathbf{k}",BLUE)
        self.add_fixed_in_frame_mobjects(assembled)
        self.play(ReplacementTransform(VGroup(*compact_terms),assembled),FadeOut(directions),FadeOut(signs),FadeOut(determinant),FadeOut(heading)); self.wait(1.1)
        self.play(FadeOut(assembled)); self.remove_fixed_in_frame_mobjects(assembled); self.remove(assembled)

    def _show_cross_hatch_computation(self) -> None:
        heading=Text("The Cross-Hatch Shortcut",font_size=35,color=YELLOW).to_edge(UP).shift(DOWN*1.05)
        shortcut,entry_rows=self._manual_grid([
            [r"\mathbf{i}",r"\mathbf{j}",r"\mathbf{k}",r"\mathbf{i}",r"\mathbf{j}"],
            ["2","1","3","2","1"],
            ["1","4","2","1","4"],
        ],column_spacing=0.76,row_spacing=0.34)
        shortcut.scale(1.02).shift(UP*0.28)
        for idx in (0,3): entry_rows[0][idx].set_color(RED)
        for idx in (1,4): entry_rows[0][idx].set_color(GREEN)
        entry_rows[0][2].set_color(BLUE)
        note=Text("Repeat the first two columns. Each dashed diagonal joins one product pair.",font_size=23).next_to(shortcut,DOWN,buff=0.24)
        self.add_fixed_in_frame_mobjects(heading,shortcut,note); self.play(FadeIn(heading),FadeIn(shortcut),FadeIn(note)); self.wait(0.8)
        def center(r,c): return entry_rows[r][c].get_center()
        def product_line(ra,ca,rb,cb,color):
            return DashedLine(center(ra,ca),center(rb,cb),color=color,stroke_width=6,dash_length=0.12,dashed_ratio=0.58)
        data=(
            ("i-component",RED,(1,1,2,2),(1,2,2,1),r"(1)(2)=2",r"(3)(4)=12",r"2-12=-10"),
            ("j-component",GREEN,(1,2,2,3),(1,3,2,2),r"(3)(1)=3",r"(2)(2)=4",r"3-4=-1"),
            ("k-component",BLUE,(1,3,2,4),(1,4,2,3),r"(2)(4)=8",r"(1)(1)=1",r"8-1=7"),
        )
        for label_text,color,pos_pair,neg_pair,pos_tex,neg_tex,res_tex in data:
            pl=product_line(*pos_pair,color); nl=product_line(*neg_pair,color)
            label=Text(label_text,font_size=28,color=color).to_edge(LEFT).shift(RIGHT*0.55+DOWN*1.72)
            pos=MathTex(pos_tex,font_size=31,color=color).next_to(label,RIGHT,buff=0.34)
            neg=MathTex(neg_tex,font_size=31,color=color).next_to(pos,RIGHT,buff=0.58)
            sub=MathTex(res_tex,font_size=34,color=color).to_edge(DOWN).shift(UP*0.18)
            self.add_fixed_in_frame_mobjects(pl,nl,label,pos,neg,sub)
            self.play(Create(pl),FadeIn(label),FadeIn(pos)); self.wait(0.65)
            self.play(Create(nl),FadeIn(neg)); self.wait(0.65)
            self.play(FadeIn(sub)); self.wait(0.90)
            self.play(FadeOut(pl),FadeOut(nl),FadeOut(label),FadeOut(pos),FadeOut(neg),FadeOut(sub))
            self.remove_fixed_in_frame_mobjects(pl,nl,label,pos,neg,sub); self.remove(pl,nl,label,pos,neg,sub)
        self.wait(0.75); self.play(FadeOut(shortcut),FadeOut(note),FadeOut(heading)); self.remove_fixed_in_frame_mobjects(shortcut,note,heading); self.remove(shortcut,note,heading)
        vf=MathTex(r"-10\mathbf{i}-\mathbf{j}+7\mathbf{k}",font_size=43)
        vf.set_color_by_tex(r"\mathbf{i}",RED); vf.set_color_by_tex(r"\mathbf{j}",GREEN); vf.set_color_by_tex(r"\mathbf{k}",BLUE)
        vh=Text("Shortcut result",font_size=34,color=YELLOW).next_to(vf,UP,buff=0.30)
        self.add_fixed_in_frame_mobjects(vf,vh); self.play(FadeIn(vh),FadeIn(vf)); self.wait(1.2)
        self.play(FadeOut(vf),FadeOut(vh)); self.remove_fixed_in_frame_mobjects(vf,vh); self.remove(vf,vh); self.wait(0.25)
        cf=MathTex(r"\begin{bmatrix}-10\\-1\\7\end{bmatrix}",font_size=49)
        ch=Text("Coordinate form",font_size=28,color=YELLOW).next_to(cf,UP,buff=0.30)
        self.add_fixed_in_frame_mobjects(cf,ch); self.play(FadeIn(ch),FadeIn(cf)); self.wait(1.2)
        self.play(FadeOut(ch),FadeOut(cf)); self.remove_fixed_in_frame_mobjects(cf,ch); self.remove(cf,ch)

    def _show_dot_product_verification(self, s) -> None:
        heading = Text(
            "Verify the geometry",
            font_size=34,
            color=YELLOW,
        ).shift(UP * 1.65)

        first = MathTex(
            r"\mathbf{u}\cdot(\mathbf{u}\times\mathbf{v})"
            r"="
            r"2(-10)+1(-1)+3(7)=0",
            font_size=34,
        )
        second = MathTex(
            r"\mathbf{v}\cdot(\mathbf{u}\times\mathbf{v})"
            r"="
            r"1(-10)+4(-1)+2(7)=0",
            font_size=34,
        )
        conclusion = Text(
            "The computed vector is perpendicular to both inputs.",
            font_size=26,
            color=GREEN,
        )

        group = VGroup(heading, first, second, conclusion).arrange(
            DOWN,
            buff=0.30,
        )
        self.add_fixed_in_frame_mobjects(group)
        self.play(FadeIn(heading), FadeIn(first))
        self.wait(0.6)
        self.play(FadeIn(second))
        self.wait(0.6)
        self.play(FadeIn(conclusion))
        self.wait(1.0)
        self.play(FadeOut(group))

    def _show_geometry(self, s) -> None:
        axes = ThreeDAxes(
            x_range=(-4, 4, 1),
            y_range=(-3, 5, 1),
            z_range=(-4, 8, 1),
            x_length=6.8,
            y_length=5.0,
            z_length=5.8,
        ).shift(DOWN * 0.55)

        self.set_camera_orientation(
            phi=68 * DEGREES,
            theta=-48 * DEGREES,
            zoom=0.88,
        )

        u_arrow = self._arrow(axes, s.vector_u, BLUE)
        v_arrow = self._arrow(axes, s.vector_v, YELLOW)
        result_arrow = self._arrow(axes, s.result, GREEN)

        labels = VGroup(
            self._label(r"\mathbf{u}", axes, s.vector_u, BLUE),
            self._label(r"\mathbf{v}", axes, s.vector_v, YELLOW),
            self._label(
                r"\mathbf{u}\times\mathbf{v}",
                axes,
                s.result,
                GREEN,
            ),
        )

        note = Text(
            "The coordinates reproduce the perpendicular vector.",
            font_size=26,
            color=GREEN,
        ).to_edge(DOWN).shift(UP * 0.28)
        self.add_fixed_in_frame_mobjects(note)

        self.play(Create(axes))
        self.play(Create(u_arrow), Create(v_arrow))
        self.play(Create(result_arrow), FadeIn(labels), FadeIn(note))
        self.begin_ambient_camera_rotation(rate=0.16)
        self.wait(2.8)
        self.stop_ambient_camera_rotation()
        self.play(
            FadeOut(axes),
            FadeOut(u_arrow),
            FadeOut(v_arrow),
            FadeOut(result_arrow),
            FadeOut(labels),
            FadeOut(note),
        )

    def _show_reflection(self) -> None:
        heading = Text(
            "The determinant is not merely a trick.",
            font_size=35,
            color=YELLOW,
        )
        line1 = Text(
            "Each component comes from a 2×2 minor.",
            font_size=28,
        )
        line2 = Text(
            "The alternating signs preserve orientation.",
            font_size=28,
        )
        line3 = Text(
            "The result is perpendicular to both inputs.",
            font_size=28,
        )

        group = VGroup(heading, line1, line2, line3).arrange(
            DOWN,
            buff=0.34,
        )
        self.add_fixed_in_frame_mobjects(group)
        self.play(FadeIn(group))

    @staticmethod
    def _vector_display():
        u = MathTex(
            r"\mathbf{u}=\begin{bmatrix}2\\1\\3\end{bmatrix}",
            font_size=44,
            color=BLUE,
        )
        v = MathTex(
            r"\mathbf{v}=\begin{bmatrix}1\\4\\2\end{bmatrix}",
            font_size=44,
            color=YELLOW,
        )
        return VGroup(u, v).arrange(RIGHT, buff=1.15).shift(DOWN * 0.25)

    @staticmethod
    def _determinant_display():
        i_part = MathTex(
            r"\mathbf{i}\begin{vmatrix}1&3\\4&2\end{vmatrix}",
            font_size=42,
            color=RED,
        )
        j_part = MathTex(
            r"-\mathbf{j}\begin{vmatrix}2&3\\1&2\end{vmatrix}",
            font_size=42,
            color=GREEN,
        )
        k_part = MathTex(
            r"+\mathbf{k}\begin{vmatrix}2&1\\1&4\end{vmatrix}",
            font_size=42,
            color=BLUE,
        )
        return VGroup(i_part, j_part, k_part).arrange(RIGHT, buff=0.30)

    @staticmethod
    def _arrow(axes, vector, color):
        return Arrow3D(
            start=axes.c2p(0, 0, 0),
            end=axes.c2p(
                float(vector[0]),
                float(vector[1]),
                float(vector[2]),
            ),
            color=color,
            thickness=0.035,
            height=0.20,
            base_radius=0.09,
        )

    @staticmethod
    def _label(tex, axes, vector, color):
        label = MathTex(tex, font_size=27, color=color)
        label.move_to(
            axes.c2p(
                float(vector[0]),
                float(vector[1]),
                float(vector[2]),
            )
            + 0.22 * RIGHT
            + 0.18 * UP
        )
        return label
