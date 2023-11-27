from PIL import Image, ImageDraw

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def draw_squares(player_list, pk):
    # Set up the image size based on the number of entries
    image_width = 800
    image_height = 800

    # Create a new image with a white background
    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)

    # Draw rectangles for each entry
    list_size = len(player_list)
    entry_width = image_width // (list_size + 1)
    entry_height = image_height // list_size

    nodes = []
    for i, entry in enumerate(player_list):
        offset = entry_height // 2
        y_pos = offset + (i * entry_height)
        nodes.append(Node(0, y_pos))

    draw_horizontal_lines(draw, nodes, 140)


    image.save("bracket_app/static/bracket_images/" + str(pk) + "_bracket.png")


def draw_horizontal_lines(draw, nodes, x_length):
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
        draw_vertical_lines(draw, future_vertical_nodes, y_length, extra_future_horizontal_nodes, flag, backup_dy)

def draw_vertical_lines(draw, nodes, y_length, extra_horizontal_nodes, flag, backup_dy):
    future_horizontal_nodes = []
    for i, node in enumerate(nodes):
        dy = y_length
        if (i == len(nodes) - 1 and flag):
            dy = backup_dy

        y = node.y + (dy // 2)
        future_horizontal_nodes.append(Node(node.x, y))
        draw.line([(node.x, node.y), (node.x, node.y + dy)], fill="black")
            
    future_horizontal_nodes.extend(extra_horizontal_nodes)
    x_length = 140
    draw_horizontal_lines(draw, future_horizontal_nodes, x_length)
        
   