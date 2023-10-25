from PIL import Image, ImageDraw, ImageFont
import math
from scipy.spatial import Voronoi
import numpy as np
import random
import matplotlib.pyplot as plt





class Rainbow:
    def __init__(self, stakeholders=None):
        # image parameters
        self.height = 330
        self.width = 600
        self.line_colour = "black"
        self.bg_colour = "white"
        self.diagram_output_name = "rainbow_diagram.png"
        
        # diagram line parameters
        self.center = (self.width // 2, self.height)
        self.radius = (self.width - 2) // 2
        self.radial_lines_angles = [
            60, 
            120
        ] # angle in degrees for radial lines starting from semi-circle bottom left
    
        # stakeholder parameters
        self.stakeholder_input_type = "attribute" # [exact, attribute]
        self.point_diameter = 10
        if stakeholders == None:
            self.stakeholders = [
                ("Google", 0.7, 0.7, "#FF0000"),
                ("Facebook", 0.7, 0.7, "#00FFFF"),
                ("Twitter", 0.7, 0.7, "#0000FF"),
                ("Netflix", 0.7, 0.7, "#0BBBFF"),
            ] # if exact: (angle placement from left (0-1), depth placement from center (0-1), colour (hex))
            # if attribute: (amount affecting (0-1), amount affected (0-1), colour(hex))
        else:
            self.stakeholders = stakeholders
        # angle label parameters
        self.angle_label_font_type = "arial.ttf"
        self.angle_label_font_size = 14
        self.angle_label_font_colour = "black"
        self.radius_label_buffer = 20
        self.angle_labels = [
            "Influence",
            "Affected"
        ] # in order from left to right
        
        # depth label parameters
        self.depth_label_font_type = "arial.ttf"
        self.depth_label_font_size = 12
        self.depth_label_font_colour = "black"
        self.depth_labels = [
            "Least",
            "Moderately",
            "Most",
        ] # in order from top to bottom
        
        # legend label parameters
        self.legend_label_font_type = "arial.ttf"
        self.legend_label_font_size = 18
        
        # uninitialised parameters
        self.diagram = Image.new("RGB", (self.width, self.height), self.bg_colour)
    
    def build(self):
        
        self.build_diagram()
        self.place_stakeholders()
        self.add_legend_and_title()
        
        self.diagram.save(self.diagram_output_name)
        self.diagram.show()
    
    def build_diagram(self):
        draw = ImageDraw.Draw(self.diagram)
        
        # define circle parameters
        circle_center = self.center
        radius_1 = self.radius
        rad_width = radius_1 // 3
        radius_2 = radius_1 - rad_width
        radius_3 = radius_2 - rad_width
        
        # add angle labels
        label_font = ImageFont.truetype(
            self.angle_label_font_type, 
            self.angle_label_font_size
        )
        lab_dist = self.radius + self.radius_label_buffer
        # add mixed label
        
        final_labels = [
            (self.angle_labels[0], 140, 50),
            (self.angle_labels[1], 40, -50),
        ]  # (label_text, angle_from_circle_left, text_tilt_from_horizontal)
        mixed_label = (self.angle_labels[0] + " and " +
                       self.angle_labels[1], 90, 0)
        final_labels.append(mixed_label)
        for label, angle, tilt in final_labels:
            angle = 360 - angle

            x = self.center[0] + int(lab_dist * math.cos(math.radians(angle)))
            y = self.center[1] + int(lab_dist * math.sin(math.radians(angle)))

            text_img = Image.new("RGBA", (250, 100), self.bg_colour)
            image1 = ImageDraw.Draw(text_img)

            text_width, text_height = image1.textsize(label, font=label_font)
            text_position = ((text_img.width - text_width) / 2,
                             (text_img.height - text_height) / 2)

            image1.text(text_position, label,
                        fill=self.angle_label_font_colour, font=label_font)

            rotated_text = text_img.rotate(tilt, expand=True)

            sx, sy = rotated_text.size
            px, py = x - sx // 2, y - sy // 2

            self.diagram.paste(
                rotated_text, (px, py, px + sx, py + sy), rotated_text)
        
        # draw each circle
        circle_radiuses = [radius_1, radius_2, radius_3]
        for r in circle_radiuses:
            draw.ellipse(
                (circle_center[0] - r, 
                circle_center[1] - r, 
                circle_center[0] + r, 
                circle_center[1] + r),
                self.bg_colour,
                self.line_colour
            )
        
        # draw each wedge
        for r in self.radial_lines_angles:
            r = 360 - r
            x = circle_center[0] + int(radius_1 * math.cos(math.radians(r)))
            y = circle_center[1] + int(radius_1 * math.sin(math.radians(r)))
            
            draw.line(
                (circle_center[0], circle_center[1], x, y),
                self.line_colour
            )
        
        # add depth labels
        bump = radius_3 // 2
        depth_font = ImageFont.truetype(
            self.depth_label_font_type, 
            self.depth_label_font_size,
        )
        text_width = self.center[0]
        
        for i in range(len(circle_radiuses)):
            text_height = circle_radiuses[i] - bump
            label = self.depth_labels[i]
            
            text_height = self.height - text_height
            
            draw.text(
                (text_width, text_height),
                label,
                fill=self.depth_label_font_colour,
                font=depth_font,
                anchor="mm",
                align="center",
            )
        
    def place_stakeholders(self):
        
        draw = ImageDraw.Draw(self.diagram)
        
        base_degrees = 180
        
        # list of points as (x, y, colour)
        stakeholder_points = []
        
        # calc stakeholder initial point
        for elem in self.stakeholders:
            stake = elem[0]
            values = (elem[1], elem[2], elem[3])
            
            # adjust according to stakeholder type
            if self.stakeholder_input_type == "exact":
                # get angle percentage from left edge, get depth percentage from top edge
                angle, depth, colour = values[0], values[1], values[2]
            
            elif self.stakeholder_input_type == "attribute":
                # get left attribute percentage value, right attribute percentage, colour
                val1, val2, colour = values[0], values[1], values[2]
                
                max_val = max(val1, val2)
                diff = abs(val1 - val2)
                
                base_bonus_angle = 90
                diff_perc = diff / max_val
                bonus_angle = base_bonus_angle * diff_perc
                
                if val1 > val2:
                    final_angle_perc = (90 - bonus_angle) / 180
                else:
                    final_angle_perc = (90 + bonus_angle) / 180
                
                # placeholder
                angle, depth = final_angle_perc, max_val
            else:
                raise Exception("not a valid stakeholder_input_type.")
            
            angle = - 180 + (base_degrees * angle)
            depth = self.radius - self.radius * depth
            
            x = self.center[0] + int(depth * math.cos(math.radians(angle)))
            y = self.center[1] + int(depth * math.sin(math.radians(angle)))

            stakeholder_points.append((x, y, colour))
        
        # jitter points to prevent overlap
        stakeholder_points = self.jitter(stakeholder_points, self.point_diameter, 100)
        
        # place jittered stakeholder points
        for x, y, colour in stakeholder_points:
            # Calculate the coordinates of the bounding box for the circle
            x1 = x - self.point_diameter // 2
            y1 = y - self.point_diameter // 2
            x2 = x + self.point_diameter // 2
            y2 = y + self.point_diameter // 2
            
            draw.ellipse([(x1, y1), (x2, y2)], fill=colour, outline=colour)
    
    # unfinished do not use (consider importin lloyd from https://github.com/duhaime/lloyd)
    def jitter(self, points, min_distance, max_iterations=100, learning_rate=0.1):
        
        def distance(point1, point2):
            return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
        
        temp_points = [(x + random.uniform(-0.001, 0.001), y +
                   random.uniform(-0.001, 0.001)) for x, y, col in points]

        num_points = len(temp_points)

        for iteration in range(max_iterations):
            for i in range(num_points):
                for j in range(i + 1, num_points):
                    point1 = np.array(temp_points[i])
                    point2 = np.array(temp_points[j])
                    current_distance = distance(point1, point2)

                    if current_distance < min_distance:
                        move_vector = (point1 - point2) / np.linalg.norm(point1 -
                                                                         point2) * (min_distance - current_distance) / 2
                        temp_points[i] = tuple(point1 + learning_rate * move_vector)
                        temp_points[j] = tuple(point2 - learning_rate * move_vector)

        # rebuild points
        final_points = []
        for idx, row in enumerate(temp_points):
            final_points.append((row[0], row[1], points[idx][2]))
        
        return final_points
        
        """# construct np array of points
        just_points = []
        for x, y, col in points:
            #noise_magnitude = 0.1  # Adjust this value as needed
            #x = x + random.uniform(-noise_magnitude, noise_magnitude)
            #y = y + random.uniform(-noise_magnitude, noise_magnitude)
            just_points.append((x, y))
        # add 3 dummy points
        dummy_points = [(-500, -500), (-250, -500), (-500, -250)]
        for d in dummy_points:
            just_points.append(d)
        just_points = np.array(just_points)
        
        print(just_points)
        # iterate
        for epoch in range(max_iterations):
            vor = Voronoi(just_points)
            
            # iterate through each point
            for i in range(len(just_points)):
                region = vor.regions[vor.point_region[i]]
                region_vertices = [vor.vertices[j] for j in region if j != -1]
                
                if not region_vertices:
                    continue
                
                # Calculate the centroid of the region
                centroid = np.mean(region_vertices, axis=0)
                
                # Calculate the vector from the current point to the centroid
                vector = centroid - just_points[i]
                
                # If the vector length is greater than d, scale it to d
                if np.linalg.norm(vector) > min_distance:
                    vector = min_distance * vector / np.linalg.norm(vector)
                
                # Move the point to the new location
                just_points[i] = just_points[i] + vector
        
        # convert back to list of tuples
        out_points = []
        for i in range(len(points)):
            tup = (just_points[i, 0], just_points[i, 1], points[i][2])
            out_points.append(tup)
        
        return out_points"""
    
    
    def add_legend_and_title(self):
        
        font = ImageFont.truetype(
            self.legend_label_font_type,
            self.legend_label_font_size
        )
        
        line_height = font.getsize("Tg")[1]
        legend_height = len(self.stakeholders) * line_height
        
        legend = Image.new("RGB", (self.width, legend_height), self.bg_colour)
        draw = ImageDraw.Draw(legend)   

        for i, stake in enumerate(self.stakeholders):
            name, _, _, colour = stake
            #_, _, colour = self.stakeholders[name]
            y = (i) * line_height  # Start from 2nd line
            point = "• " + name  # Add a bullet point
            draw.text((10, y), point, fill=colour, font=font)
        
        
        # combine images
        final_image = Image.new("RGB", (self.width, self.height + legend.height), self.bg_colour)
        final_image.paste(legend, (0, 0))
        final_image.paste(self.diagram, (0, legend.height))

        self.diagram = final_image



if __name__ == "__main__":
    r = Rainbow()
    
    r.build()
    

