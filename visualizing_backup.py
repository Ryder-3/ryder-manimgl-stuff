from manimlib import *
import json
import csv
import operator
import sys
from pathlib import Path

# Add parent directory to Python path to import customMobject
sys.path.insert(0, str(Path(__file__).parent.parent))
import customMobject as cm

import datetime

PROJECT_PATH = r".\Prog-2-Data-Structures-Project"

class Main(ThreeDScene):
    def construct(self):
        #formating()
        with open(r".\formatted.json", 'r') as formatted_json:
            data = json.load(formatted_json)
        self.frame.set_euler_angles(0,0,0)

        averaged_scores = {}
        for brand in data:
            if brand != 'brand':
                average_score = getAverageReviewScore(brand, data)
                averaged_scores[brand] = average_score

        presentation_title = TexText("Comparing Phone Reveiws to Date and Brand")


        first_analysis_title = TexText("Average Score of Different Brands")
        first_analysis_title.to_edge(UP)


        # getting the data for the bars in the unsorted graph
        brands = averaged_scores.keys()
        scores = averaged_scores.values()


        scores = list(scores)
        brands = list(brands)

        # Store original brand names before renaming
        original_brand_at_0 = brands[0]
        brands[0] = 'Unknown'


        color_palette = [BLUE, RED, GREEN, YELLOW, WHITE, ORANGE, TEAL, MAROON, PINK, GOLD]
        brand_colors = {brand: color_palette[i % len(color_palette)] for i, brand in enumerate(brands)}
        colors = [brand_colors[brand] for brand in brands]

        # making the unsorted graph
        average_score_chart = cm.BarGraph(values=scores, bar_names=brands, y_range=[0,5,1], bar_colors=colors)


        # getting the data for the sorted graph

        sorted_averaged_scores = dict(sorted(averaged_scores.items(), key=operator.itemgetter(1)))
        sorted_scores = sorted_averaged_scores.values()

            #sorting the brands and scores


        sorted_scores = list(sorted_scores)
        sorted_scores.sort()
        sorted_scores.reverse()

        sorted_brands = []
        reference_items = averaged_scores.items()
        for score in sorted_scores:
            for pair in reference_items:
                pair = list(pair)
                if score == pair[1]:
                    sorted_brands.append(pair[0])

        # Replace the same original brand with 'Unknown' in sorted list
        # (it will be at a different index than in the unsorted list)
        for i, brand in enumerate(sorted_brands):
            if brand == original_brand_at_0:
                sorted_brands[i] = 'Unknown'
                break


        sorted_colors = [brand_colors[brand] for brand in sorted_brands]

        # making the sorted bar graph
        sorted_score_chart = cm.BarGraph(values=sorted_scores, bar_names=sorted_brands, y_range=[0,5,1], bar_colors=sorted_colors)


        average_score = getPopulationMean(data)
        


        average_score_text = TexText("Average score of all phones: " + str(average_score))
        average_score_text.to_edge(UP)
        
        

        self.play(Write(presentation_title))
        self.wait()
        self.play(FadeOut(presentation_title))
        self.play(Write(first_analysis_title))
        self.wait()
        self.play(ShowCreation(average_score_chart.bars),
                  Write(average_score_chart.labels),
                  Write(average_score_chart.value_labels),
                  ShowCreation(average_score_chart.y_axis),
                  FadeIn(average_score_chart.y_axis_labels))
        self.wait()

        
        animations = []
        for i, sorted_brand in enumerate(sorted_brands):
            
            original_index = brands.index(sorted_brand)

    
            original_bar = average_score_chart.bars[original_index]
            original_label = average_score_chart.labels[original_index]
            original_value = average_score_chart.value_labels[original_index]

            
            target_bar = sorted_score_chart.bars[i]
            target_label = sorted_score_chart.labels[i]
            target_value = sorted_score_chart.value_labels[i]

            
            animations.append(original_bar.animate.move_to(target_bar.get_center()))
            animations.append(original_label.animate.move_to(target_label.get_center()))
            animations.append(original_value.animate.move_to(target_value.get_center()))

        self.play(*animations)
        self.wait()
        self.play(FadeOut(average_score_chart), FadeOut(first_analysis_title))
        

        # Part 2
        # Graphing reviews over time

        # Create title for time series
        time_series_first_title = TexText("Average Review Score Over Time (Samsung)")
        time_series_first_title.to_edge(UP)

        time_series_second_title = TexText("Average Review Score Over Time (All Brands at once)")
        time_series_second_title.to_edge(UP)


        # Create mapping from display names to original data keys
        brand_name_mapping = {}
        for i, brand in enumerate(brands):
            if brand == 'Unknown' and i == 0:
                brand_name_mapping['Unknown'] = original_brand_at_0
            else:
                brand_name_mapping[brand] = brand

        review_over_time_graphs = {}
        chart_lines = VGroup()
        for brand in brands:
            # Use original brand name for data lookup
            data_brand = brand_name_mapping[brand]
            time_data = getAverageReviewsByTimePeriod(data, data_brand)
            times = list(time_data.keys())
            average_scores = list(time_data.values())
            if brand == "Samsung":
                review_timeline = cm.LineChart(
                    times,
                    average_scores,
                    [0,5,1],
                    line_color = brand_colors[brand]
                )
            else:
                review_timeline = cm.LineChart(
                    times,
                    average_scores,
                    [0,5,1],
                    line_color = brand_colors[brand],
                    show_axes=False
                )
            try:
                chart_lines.add(review_timeline.line)
            except AttributeError:
                continue

            review_over_time_graphs[brand] = review_timeline



        # Animate the time series chart
        self.play(
            Write(time_series_first_title)
        )
        self.wait()
        self.play(
            ShowCreation(review_over_time_graphs["Samsung"].y_axis),
            ShowCreation(review_over_time_graphs["Samsung"].x_axis),
            FadeIn(review_over_time_graphs["Samsung"].y_axis_labels),
            FadeIn(review_over_time_graphs["Samsung"].x_axis_labels),
            
        )
        self.wait()
        self.play(
            ShowCreation(review_over_time_graphs["Samsung"].line),
        )
        self.wait()
        # Create and position the key/legend
        legend = cm.Key(brands, brand_colors)
        legend.to_edge(RIGHT, buff=0.5)
        legend.scale(0.7)
        legend.shift(DOWN*0.7)

        creation_animations = []
        for brand in brands:
            if brand != "Samsung":
                creation_animations.append(ShowCreation(review_over_time_graphs[brand].line))

        self.play(
            *creation_animations,
            ReplacementTransform(time_series_first_title, time_series_second_title),
            ShowCreation(legend)
        )
        self.wait()


        # Animate positioning each graph at different depths in 3D space
        depth_spacing = 0.5  
        shift_animations = []
        for i, brand in enumerate(brands):
            # Calculate Z position for each graph
            z_position = i * depth_spacing - (len(brands) - 1) * depth_spacing / 2
            shift_animations.append(
                review_over_time_graphs[brand].animate.shift(OUT * z_position)
            )

        
        self.play(
            *shift_animations,
            self.frame.animate.set_euler_angles(80*DEGREES,-70*DEGREES,-85*DEGREES).scale(1.5),
            run_time=2
        )
        self.wait()


        return_animations = []
        for i, brand in enumerate(brands):
            z_position = i * depth_spacing - (len(brands) - 1) * depth_spacing / 2
            return_animations.append(
                review_over_time_graphs[brand].animate.shift(OUT * -z_position)
            )

        self.play(
            *return_animations,
            self.frame.animate.set_euler_angles(0,0,0).scale(2/3),
            run_time=2
        )
        self.wait()

        # Create the average line for all brands
        all_time_data = getAverageReviewsByTimePeriod(data)
        times = list(all_time_data.keys())
        scores = list(all_time_data.values())
        average_line_chart = cm.LineChart(times, scores, [0,5,1], line_color=WHITE, show_axes=False)
   
        merge_title = TexText("All Brands Merge to Overall Average")
        merge_title.to_edge(UP)

        self.play(
            FadeOut(legend),
            ReplacementTransform(time_series_second_title, merge_title),
            run_time=1
        )
        self.wait()

        removal_animations = []
        for brand in brands:
            line = review_over_time_graphs[brand].line
            removal_animations.append(
                ShowPassingFlash(
                    line.copy().set_color(BLACK).set_stroke(width=8),
                    time_width=0.5,
                    run_time=3
                )
            )
            removal_animations.append(FadeOut(line))

        self.play(*removal_animations, ShowCreation(average_line_chart.line), run_time = 3)
        self.wait()
        self.play(Uncreate(average_line_chart.line),
                  Uncreate(merge_title),
                  Uncreate(review_over_time_graphs['Samsung'].y_axis),
                  Uncreate(review_over_time_graphs['Samsung'].x_axis),
                  FadeOut(review_over_time_graphs['Samsung'].y_axis_labels),
                  FadeOut(review_over_time_graphs['Samsung'].x_axis_labels),
        )
    def on_mouse_press(self, point, button, modifiers):
        print('Click')
        return super().on_mouse_press(point, button, modifiers)

def getPopulationMean(data):
    mean = []
    for brand in data:
        if brand != 'brand':
            for product in data[brand]:
                for review in data[brand][product]:
                    score = review[0]
                    mean.append(int(score))
    mean = sum(mean) / len(mean)
    mean = round(mean, 3)
    return mean

def getAverageReviewScore(brand, data):
    temp_scores = []
    for product in data[brand]:
        for review in data[brand][product]:
            score = review[0]
            temp_scores.append(int(score))
    mean = sum(temp_scores) / len(temp_scores)
    mean = round(mean, 3)
    return mean

def getAverageReviewsByTimePeriod(data, brand=None):
    reviews_by_date = {}

    for brand_name in data:
        if brand_name == 'brand':
            continue
        if brand is not None and brand_name != brand:
            continue

        for product in data[brand_name]:
            for review in data[brand_name][product]:
                score = int(review[0])
                date_str = review[1]

            
                try:
                    date_obj = datetime.datetime.strptime(date_str, "%B %d, %Y")
                    period = date_obj.strftime("%Y-%m")  # Group by year-month

                    if period not in reviews_by_date:
                        reviews_by_date[period] = []
                    reviews_by_date[period].append(score)
                except ValueError:
    
                    continue

    # Calculate averages
    averages_over_time = {}
    for period, scores in sorted(reviews_by_date.items()):
        averages_over_time[period] = round(sum(scores) / len(scores), 3)

    return averages_over_time

def formating():
    with open(fr'{PROJECT_PATH}\20191226-items.csv', 'r', encoding='utf-8') as item_csv:
        item_csv_reader = csv.reader(item_csv)

        with open(fr'{PROJECT_PATH}\20191226-reviews.csv', 'r', encoding='utf-8') as review_csv:
            review_csv_reader = csv.reader(review_csv)
            condenced_review_dict = {}

    

            for review in review_csv_reader:
                if review[0] not in condenced_review_dict.keys():
                    short_review = [review[2], review[3]]
                    condenced_review_dict[review[0]] = [short_review]
                else:
                    short_review = [review.copy()[2], review.copy()[3]]
                    condenced_review_dict[review[0]].append(short_review)

            to_json = {}
            for item in item_csv_reader:
                if item[1] not in to_json.keys():
                    to_json[item[1]] = {item[0] : 'temp'}
                else:
                    to_json[item[1]][item[0]] = 'temp'
            
            items = condenced_review_dict.keys()
            for brand in to_json:
                for asin in to_json[brand]:
                    for item in items:
                        if asin == item:
                            to_json[brand][asin] = condenced_review_dict[item]
                       
            with open(fr'{PROJECT_PATH}\formatted.json', 'w') as formmated_json:
                json.dump(to_json, formmated_json, indent=4)
          