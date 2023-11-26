from PIL import Image, ImageDraw

def draw_squares(num_squares, pk):
    square_size = 50  # Adjust the size of the square
    distance_between_squares = 60  # Adjust the distance between squares

    # Calculate the image size based on the number of squares
    image_width = (num_squares + 1) * distance_between_squares
    image_height = square_size + 20  # Add some padding at the top

    # Create a new image with a white background
    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)

    # Draw the squares
    x = 10  # Start drawing from a little padding on the left
    y = 10  # Start drawing from a little padding at the top
    for _ in range(num_squares):
        draw.rectangle([x, y, x + square_size, y + square_size], outline="black")
        x += distance_between_squares

    # Save the image as a PNG file

    image.save("bracket_app/bracket_images/" + str(pk) + "_bracket.png")
