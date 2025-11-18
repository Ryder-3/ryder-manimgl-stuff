from __future__ import annotations
from manimlib import *
import numpy as np

class BarGraph(VGroup):

    def __init__(self, values, bar_names=None, y_range=[0, 1, 1], width=12, height=5, bar_colors=None, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.values = list(values)
        self.bar_names = list(bar_names) if bar_names is not None else [str(i) for i in range(len(values))]
        self.bar_colors = bar_colors
        y_min, y_max, y_step = y_range

        if len(self.values) == 0:
            return

        total_width = width
        bar_slot = total_width / len(self.values)
        bar_width = bar_slot * 0.6

        default_colors = [BLUE, RED, GREEN, YELLOW, PURPLE, ORANGE, TEAL, MAROON, PINK, GOLD]

        bars = VGroup()
        labels = VGroup()
        value_labels = VGroup()

        y_axis = Line(
            start=np.array([-total_width / 2 - 0.5, -height / 2, 0]),
            end=np.array([-total_width / 2 - 0.5, height / 2, 0]),
            color=WHITE,
            stroke_width=2
        )

        y_axis_labels = VGroup()
        num_ticks = int((y_max - y_min) / y_step) + 1

        for i in range(num_ticks):
            tick_value = y_min + i * y_step
            tick_y = -height / 2 + (i * y_step / (y_max - y_min)) * height

            tick = Line(
                start=np.array([-total_width / 2 - 0.5, tick_y, 0]),
                end=np.array([-total_width / 2 - 0.3, tick_y, 0]),
                color=WHITE,
                stroke_width=2
            )
            y_axis_labels.add(tick)

            # Tick label
            tick_label = TexText(str(tick_value)).scale(0.4)
            tick_label.next_to(tick, LEFT, buff=0.1)
            y_axis_labels.add(tick_label)

        for i, val in enumerate(self.values):

            height_scaled = 0
            if (y_max - y_min) != 0:
                height_scaled = (val - y_min) / (y_max - y_min) * height

            if self.bar_colors and i < len(self.bar_colors):
                color = self.bar_colors[i]
            else:
                color = default_colors[i % len(default_colors)]

            bar = Rectangle(width=bar_width, height=height_scaled, fill_color=color, fill_opacity=0.8, stroke_width=2, stroke_color=WHITE)
            x = (-total_width / 2) + (bar_slot * i) + (bar_slot / 2)
            bar.move_to(np.array([x, -height / 2 + height_scaled / 2, 0]))
            bars.add(bar)

            name = TexText(str(self.bar_names[i])).scale(0.5)
            name.next_to(bar, DOWN, buff=0.1)
            labels.add(name)

            if isinstance(val, float):
                val_str = f"{val:.3f}"  
            else:
                val_str = str(val)
            vlabel = TexText(val_str).scale(0.5)
            vlabel.next_to(bar, UP, buff=0.15)
            value_labels.add(vlabel)

        self.bars = bars
        self.labels = labels
        self.value_labels = value_labels
        self.y_axis = y_axis
        self.y_axis_labels = y_axis_labels
        self.add(bars, labels, value_labels, y_axis, y_axis_labels)

    def get_bar_labels(self):
        return self.value_labels
    
class Key(VGroup):
    def __init__(self, brands, brand_colors, **kwargs):
        VGroup.__init__(self, **kwargs)
        rows_1 = VGroup()
        rows_2 = VGroup()
        color_box_size = 0.3
        spacing = 0.4

        for i, brand in enumerate(brands):
            color = brand_colors[brand]

            color_box = Square(side_length=color_box_size, fill_color=color, fill_opacity=0.8, stroke_color=WHITE, stroke_width=2)
 
            name = TexText(brand).scale(0.4)
            name.next_to(color_box, RIGHT, buff=0.2)

            row = VGroup(color_box, name)
            if i <= (len(brands) / 2):
                rows_1.add(row)
            else:
                rows_2.add(row)

        # Arrange all rows vertically
        rows_1.arrange(DOWN, aligned_edge=LEFT, buff=spacing)
        rows_2.arrange(DOWN, aligned_edge=LEFT, buff=spacing)
        rows_2.next_to(rows_1, RIGHT, buff=1.0)

        self.add(rows_1,rows_2)

class LineChart(VGroup):

    def __init__(self, times, values, y_range=[0, 5, 1], width=12, height=5, line_color=BLUE, show_axes=True, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.times = list(times)
        self.values = list(values)
        self.line_color = line_color
        y_min, y_max, y_step = y_range

        if len(self.values) == 0:
            return

        total_width = width
        num_points = len(self.values)

        if show_axes == True:
            
            y_axis = Line(
                start=np.array([-total_width / 2 - 0.5, -height / 2, 0]),
                end=np.array([-total_width / 2 - 0.5, height / 2, 0]),
                color=WHITE,
                stroke_width=2
            )

            x_axis = Line(
                start=np.array([-total_width / 2 - 0.5, -height / 2, 0]),
                end=np.array([total_width / 2, -height / 2, 0]),
                color=WHITE,
                stroke_width=2
            )

            y_axis_labels = VGroup()
            num_ticks = int((y_max - y_min) / y_step) + 1

            for i in range(num_ticks):
                tick_value = y_min + i * y_step
                tick_y = -height / 2 + (i * y_step / (y_max - y_min)) * height

                tick = Line(
                    start=np.array([-total_width / 2 - 0.5, tick_y, 0]),
                    end=np.array([-total_width / 2 - 0.3, tick_y, 0]),
                    color=WHITE,
                    stroke_width=2
                )
                y_axis_labels.add(tick)

                tick_label = TexText(str(tick_value)).scale(0.4)
                tick_label.next_to(tick, LEFT, buff=0.1)
                y_axis_labels.add(tick_label)

            x_axis_labels = VGroup()
            label_frequency = max(1, num_points // 10)

            for i in range(0, num_points, label_frequency):
                x_pos = -total_width / 2 + (i / (num_points - 1)) * total_width
                tick = Line(
                    start=np.array([x_pos, -height / 2, 0]),
                    end=np.array([x_pos, -height / 2 - 0.2, 0]),
                    color=WHITE,
                    stroke_width=2
                )
                x_axis_labels.add(tick)

                time_label = TexText(self.times[i]).scale(0.35)
                time_label.next_to(tick, DOWN, buff=0.1)
                time_label.rotate(-45 * DEGREES) 
                x_axis_labels.add(time_label)
            self.y_axis = y_axis
            self.x_axis = x_axis
            self.y_axis_labels = y_axis_labels
            self.x_axis_labels = x_axis_labels

        points = []
        dots = VGroup()

        for i, val in enumerate(self.values):

            x_pos = -total_width / 2 + (i / (num_points - 1)) * total_width
            height_scaled = 0

            if (y_max - y_min) != 0:
                height_scaled = (val - y_min) / (y_max - y_min) * height
            y_pos = -height / 2 + height_scaled

            point = np.array([x_pos, y_pos, 0])
            points.append(point)

            dot = Dot(point, color=self.line_color, radius=0.06)
            dots.add(dot)

        if len(points) > 1:
            line = VMobject(color=self.line_color, stroke_width=3)
            line.set_points_as_corners(points)
        else:
            line = VGroup()

        self.line = line
        self.dots = dots
        
        if show_axes == True:
            self.add(y_axis, x_axis, y_axis_labels, x_axis_labels, line)
        else:
            self.add(line)

class Icosohedron(VGroup3D):

    # TODO make this scalable if wanted
    # TODO make option for fill color to be different from stroke color

    def __init__(self,
        stroke_color=BLACK,
        fill_color=BLUE,
        size=1,
        **kwargs,
    ):
        # One can make an Icosohedron by making three "golden rectangles"
        # (rectangles with height = 1 and width = golden ratio),
        # rotating each so their short sides are all on different planes,
        # then conecting the corners that are all 1 unit away.

        # we can scale this by scaling the size of the rectangles and the
        # distence condition for coneecting them by the desired scalar

        golden_ratio = (1 + np.sqrt(5))/2


        # Making all three rectangles and rotating them into place
        rectangle_1 = Rectangle(width=golden_ratio*size,
                                height=1*size,
                                color=RED,
                                fill_color=RED,
                                fill_opacity=0,
                                stroke_color=BLACK,
                                )
        

        rectangle_2 = Rectangle(width=1*size,
                                height=golden_ratio*size,
                                color=GREEN,
                                fill_color=GREEN,
                                fill_opacity=0,
                                stroke_color=BLACK,
                                )
        rectangle_2.rotate(90*DEGREES, Y_AXIS)


        rectangle_3 = Rectangle(width=1*size,
                                height=golden_ratio*size,
                                color=BLUE,
                                fill_color=BLUE,
                                fill_opacity=0,
                                stroke_color=BLACK,
                                )
        rectangle_3.rotate(90*DEGREES, X_AXIS)

        rectangles = VGroup()
        rectangles.add(rectangle_1,
                       rectangle_2,
                       rectangle_3,
                       )


        
       
        corner_points = VGroup()
        for rectangle in rectangles:
            corners = rectangle.get_all_corners()
            corners = corners.tolist()
            new_corners = []
            for i, el in enumerate(corners):
                if i % 2 == 1:
                    new_corners.append(el)

            
            

            
            seen_corners = []
            for corner in corners:
                if corner not in seen_corners:
                    seen_corners.append(corner)
            corners = seen_corners
            

            for corner in corners:
                point = Dot((corner[0],corner[1],corner[2]))
                corner_points.add(point)
        self.test_dots = corner_points
        
    
        corner_positions = []

        for rectangle in rectangles:

            corners = rectangle.get_all_corners()   
            corners = corners.tolist()
            
            
            
            for corner in corners:
                corner_positions.append(corner)

        # All of the corners are now in a list, we now need to make the actual faces
        # We'll make all of the posible equalateral triangles with side length 1, then get rid of all of them with duplicate centers
        
        
        

        
        triangle_points = []
        error = 0.000001
        for point_1 in corner_positions:
            for point_2 in corner_positions:
                for point_3 in corner_positions:
                    if (self.distenceFormula(point_1,point_2) < (1 + error)*size and
                        self.distenceFormula(point_1, point_2) > (1 - error)*size and
                        self.distenceFormula(point_2, point_3) < (1 + error)*size and
                        self.distenceFormula(point_2, point_3) > (1 - error)*size and
                        self.distenceFormula(point_1,point_3) < (1 + error)*size and
                        self.distenceFormula(point_1, point_3) > (1 - error)*size
                    ):
                        triangle_points.append([point_1,point_2,point_3])



        # now we get rid of all duplicates
        seen_triangle_centers = []
        shortend_triangle_points = []
        for triangle in triangle_points:
            if self.getCenter(triangle) not in seen_triangle_centers:
                seen_triangle_centers.append(self.getCenter(triangle))
                shortend_triangle_points.append(triangle)
        


        
        faces = VGroup()
        for face in triangle_points:
            poly = Polygon(
                np.array([face[0][0],face[0][1],face[0][2]]),
                np.array([face[1][0],face[1][1],face[1][2]]),
                np.array([face[2][0],face[2][1],face[2][2]]),
            )
            faces.add(poly)
        
        self.verticies = corner_points
        self.triangle_points = triangle_points
        self.faces = faces
        self.corner_positions = corner_positions
        self.rectangles = rectangles

    def distenceFormula(self, point_1, point_2):
        return (np.sqrt(
            ((point_1[0] - point_2[0]) ** 2) +
            ((point_1[1] - point_2[1]) ** 2) +
            ((point_1[2] - point_2[2]) ** 2)))
    
    def getCenter(self, points):
        point_1, point_2, point_3 = points
        center = [((point_1[0] + point_2[0] + point_3[0])/3), ((point_1[1] + point_2[1] + point_3[1])/3), ((point_1[2] + point_2[2] + point_3[2])/3)]
        return center
    def facesCreation(self):
        creation_animations = []
        for triangle in self.faces:
            creation_animations.append(ShowCreation(triangle))
        return creation_animations


        

class ThreeDTesting(ThreeDScene):
    def construct(self):
        test = Icosohedron()
        self.wait(2)
        self.play(*test.facesCreation(),run_time = 5)
        
        


