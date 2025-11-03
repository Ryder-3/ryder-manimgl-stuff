from manimlib import *

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