"""Creates mana icons for each color combination.

Using the color_palette.yaml file, draws circles using 
mana colors and characters. For multi-color combinations, 
each color is a circle sector (i.e. pizza slice).  
The circles are saved as PNG.
"""

import matplotlib.pyplot as plt
import numpy as np
import yaml


def get_circle_sector_points(rotation=45, extend=180):
    """Defines the geometric points of the circle sector."""

    # Define the partial circle points
    theta = np.linspace(0, np.deg2rad(extend), 100)
    x = np.cos(theta)
    y = np.sin(theta)

    # Rotate the points by 45 degrees
    t = np.deg2rad(rotation)
    x_rotated = x * np.cos(t) - y * np.sin(t)
    y_rotated = x * np.sin(t) + y * np.cos(t)

    # Center the semicircle in the 100x100 image with center at (50, 50)
    x_centered = 50 + 40 * x_rotated
    y_centered = 50 + 40 * y_rotated

    # Add lines to form the complete shape
    x_full = np.concatenate(([50], x_centered, [50]))
    y_full = np.concatenate(([50], y_centered, [50]))
    return {"x": x_full, "y": y_full}


def plot_circle_sector(char, fill_color, sector_lines, text_pos, fontsize):
    """Plots the circle sector, including lines, fill, and text."""
    ax.fill(sector_lines["x"], sector_lines["y"], color=fill_color)
    ax.text(
        text_pos["x"],
        text_pos["y"],
        char,
        fontsize=fontsize,
        color="#130c0e",
        ha="center",
        va="center",
        fontname="monospace",
        weight="bold",
    )

def save_plot():
    """Clean up and save plot."""
    ax.set_aspect("equal")
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.axis("off")
    plt.savefig(
        f"images/mana_symbols/png/{name}.png",
        bbox_inches="tight",
        pad_inches=0,
        transparent=True,
    )
    plt.close()

# Read configs
with open("src/graphics/color_palette.yml", "r", encoding="utf-8") as file:
    color_config = yaml.safe_load(file)
color_palette = color_config["colors"]
text_configs = color_config["text_positions"]
start_angles = color_config["start_angles"]

# Draw mana symbols
for name, colors in color_config["pairs"].items():
    n_colors = len(colors)
    text_config = text_configs[n_colors]
    sector_angle = 360 / n_colors
    fig, ax = plt.subplots(figsize=(1, 1), dpi=100)
    for i, color in enumerate(colors):
        rotation_angle = start_angles[n_colors] - i * sector_angle
        lines = get_circle_sector_points(rotation=rotation_angle, extend=sector_angle)

        plot_circle_sector(
            char=color,
            fill_color=color_palette[color],
            sector_lines=lines,
            text_pos=text_config["text_pos"][i],
            fontsize=text_config["size"],
        )

    save_plot()
