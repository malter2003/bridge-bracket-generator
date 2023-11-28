import math
from PIL import Image, ImageDraw, ImageFont

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Generator:
    def __init__(self, width, height, padding, player_list, pk, is_testing=False):     
        self.is_testing = is_testing 
        self.width = width
        self.height = height
        self.padding = padding
        self.player_list = player_list
        self.list_size = len(player_list)
        self.num_columns = 1 + math.ceil(math.log2(self.list_size))
        self.entry_width = (width - (padding * 2)) // self.num_columns
        self.entry_height = width // self.list_size
        self.font_size = self.entry_width // 6
        self.pk = pk

    def draw(self):
        image = Image.new("RGB", (self.width, self.width), "white")
        draw = ImageDraw.Draw(image)
        nodes = []
        for i, entry in enumerate(self.player_list):
            offset = self.entry_height // 2
            y_pos = offset + (i * self.entry_height)
            nodes.append(Node(self.padding, y_pos))

        self.draw_horizontal_lines(draw, nodes, self.entry_width)
        self.draw_text_above_lines(draw, nodes, self.entry_width, self.font_size)

        self.path = "bracket_app/static/bracket_images/" + str(self.pk) + "_bracket.png"

        if (self.is_testing):
            image.close()
        else:    
            image.save(self.path)


    def draw_horizontal_lines(self, draw, nodes, x_length):
        nodes_size = len(nodes)
        flag = False
        extra_future_horizontal_nodes = []
        future_vertical_nodes = []
        for i, node in enumerate(nodes):
            draw.line([(node.x, node.y), (node.x + x_length, node.y)], fill="black")

            if (i % 2 == 0):
                if (i < nodes_size - 1):
                    future_vertical_nodes.append(Node(node.x + x_length, node.y))
                elif (nodes_size > 1):
                    extra_future_horizontal_nodes.append(Node(node.x + x_length, node.y))
                    draw.line([(node.x + x_length, node.y), (node.x + x_length * 2, node.y)], fill="black")

        backup_dy = 0
        if (nodes_size > 3):            
            if (nodes[nodes_size - 1].y - nodes[nodes_size - 2].y != nodes[1].y - nodes[0].y and nodes_size % 2 == 0):
                flag = True
                backup_dy = nodes[nodes_size - 1].y - nodes[nodes_size - 2].y

        if (nodes_size > 1):
            y_length = nodes[1].y - nodes[0].y
            self.draw_vertical_lines(draw, future_vertical_nodes, y_length, extra_future_horizontal_nodes, flag, backup_dy)

    def draw_vertical_lines(self, draw, nodes, y_length, extra_horizontal_nodes, flag, backup_dy):
        future_horizontal_nodes = []
        for i, node in enumerate(nodes):
            dy = y_length
            if (i == len(nodes) - 1 and flag):
                dy = backup_dy

            y = node.y + (dy // 2)
            future_horizontal_nodes.append(Node(node.x, y))
            draw.line([(node.x, node.y), (node.x, node.y + dy)], fill="black")
                
        future_horizontal_nodes.extend(extra_horizontal_nodes)
        self.draw_horizontal_lines(draw, future_horizontal_nodes, self.entry_width)
        
    def draw_text_above_lines(self, draw, nodes, x_length, font_size):
        for i, node in enumerate(nodes):
            if (i < self.list_size):
                text_pos_x = node.x
                text_pos_y = node.y - font_size
                player_name = self.player_list[i]
                font = ImageFont.truetype('FreeMono.ttf', font_size)

                draw.text((text_pos_x, text_pos_y), player_name, font=font, fill="black")
