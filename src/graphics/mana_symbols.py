import svgwrite
import cairosvg
import numpy as np

# Define the color palette
color_palette = {
    "W": "#fffbd5",  # Faint Yellow
    "U": "#aae0fa",  # Light Blue
    "B": "#cbc2bf",  # Gray
    "R": "#f9aa8f",  # Soft Red
    "G": "#9bd3ae",  # Light Green
}


def create_svg_circle(letter, color, filename):
    """Function to create SVG images of circles with specified colors"""
    dwg = svgwrite.Drawing(filename, profile="tiny", size=(100, 100))
    dwg.add(dwg.circle(center=(50, 50), r=40, fill=color))
    dwg.add(
        dwg.text(
            letter,
            insert=(50, 75),
            text_anchor="middle",
            font_size="70px",
            font_family="Arial",
            fill="#000000",
        )
    )
    dwg.save()

import svgwrite


def draw_semi_circle(rotation_angle=45, diam=100):

    # Define the semicircle points before rotation
    theta = np.linspace(0, np.pi, 100)
    x = np.cos(theta)
    y = np.sin(theta)

    # Rotate points
    t = np.deg2rad(rotation_angle)
    x_rotated = x * np.cos(t) - y * np.sin(t)
    y_rotated = x * np.sin(t) + y * np.cos(t)

    # Scale and translate points to fit in the SVG view
    s1 = 50 * diam / 100
    s2 = 100 * diam / 100
    return [(s1 + s2 * x, s1 - s2 * y) for x, y in zip(x_rotated, y_rotated)]


# Function to create SVG images with two half circles of different colors and characters
def create_svg_half_circle(letter1, color1, letter2, color2, filename):
    """Create an SVG with two half circles, each with a different color and character."""
    dwg = svgwrite.Drawing(filename, profile="tiny", size=(100, 100))
    # Draw the first semicircle (lower left to upper right split)

    points = draw_semi_circle(rotation_angle=0, diam=100)
    print(points)
    dwg.add(dwg.polyline(points=points, fill=color1))

    # Draw the second semicircle (upper right to lower left split)

    # dwg.add(dwg.path(d="M 50,50 L 100,0 A 50,50 0 0,1 0,100 Z", fill=color2))

    # Add text for the first character on the lower left
    dwg.add(
        dwg.text(
            letter1,
            insert=(30, 70),  # Adjust position to balance within the triangle
            text_anchor="middle",
            font_size="30px",
            font_family="Arial",
            fill="#000000",
        )
    )

    # Add text for the second character on the upper right
    dwg.add(
        dwg.text(
            letter2,
            insert=(70, 30),  # Adjust position to balance within the triangle
            text_anchor="middle",
            font_size="30px",
            font_family="Arial",
            fill="#000000",
        )
    )

    dwg.save()

def convert_svg_to_png(svg_filename, png_filename):
    """Function to convert SVG to PNG."""
    cairosvg.svg2png(url=svg_filename, write_to=png_filename)

file_paths = []
for letter, color in color_palette.items():
    filename = f"images/mana_symbols/svg/{letter}.svg"
    create_svg_circle(letter, color, filename)
    file_paths.append(filename)

filename = f"images/mana_symbols/svg/UR.svg"
create_svg_half_circle("U", "#aae0fa", "R", "#f9aa8f", filename)
file_paths.append(filename)

jpg_file_paths = []
for svg_path in file_paths:
    png_path = svg_path.replace("svg", "png")
    convert_svg_to_png(svg_path, png_path)
    jpg_file_paths.append(png_path)
