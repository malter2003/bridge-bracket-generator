from PIL import Image, ImageDraw

def draw_squares(player_list, pk):
    # Set up the image size based on the number of entries
    image_width = 500
    image_height = 500

    # Create a new image with a white background
    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)

    # Draw rectangles for each entry
    entry_width = image_width // (len(player_list) + 1)
    entry_height = image_height // len(player_list)

    for i, entry in enumerate(player_list):
        x = 0
        y = i * entry_height
        draw.line([(x, y), (entry_width, y + entry_height // 2)], fill="black")
        draw.line([(x, y + entry_height), (entry_width, y + entry_height // 2)], fill="black")
        draw.rectangle([entry_width, y, image_width, y + entry_height], outline="black")

    # Draw a rectangle for the winner
    winner_x = image_width - entry_width
    winner_y = (image_height - entry_height) // 2
    draw.rectangle([winner_x, winner_y, winner_x + entry_width, winner_y + entry_height], outline="black", fill="lightgreen")

    image.save("bracket_app/static/bracket_images/" + str(pk) + "_bracket.png")
