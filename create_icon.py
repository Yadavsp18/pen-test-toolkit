#!/usr/bin/env python3
"""
Create a simple icon for the Penetration Testing Toolkit
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

def create_icon(output_path="icon.ico", size=(256, 256)):
    """Create a simple icon for the toolkit"""
    # Create a new image with a black background
    img = Image.new('RGBA', size, color=(0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    # Draw a red shield
    shield_points = [
        (size[0] * 0.2, size[1] * 0.2),  # Top left
        (size[0] * 0.8, size[1] * 0.2),  # Top right
        (size[0] * 0.8, size[1] * 0.6),  # Bottom right
        (size[0] * 0.5, size[1] * 0.8),  # Bottom center
        (size[0] * 0.2, size[1] * 0.6),  # Bottom left
    ]
    draw.polygon(shield_points, fill=(180, 0, 0, 255))

    # Draw a white border around the shield
    draw.polygon(shield_points, outline=(255, 255, 255, 255), width=3)

    # Draw a white lock symbol in the center
    lock_center = (size[0] * 0.5, size[1] * 0.45)
    lock_size = size[0] * 0.2

    # Lock body
    lock_left = lock_center[0] - lock_size/2
    lock_right = lock_center[0] + lock_size/2
    lock_top = lock_center[1]
    lock_bottom = lock_center[1] + lock_size

    # Draw rectangle with two points: top-left and bottom-right
    draw.rectangle([(lock_left, lock_top), (lock_right, lock_bottom)], fill=(255, 255, 255, 255))

    # Lock shackle
    shackle_width = lock_size * 0.6
    shackle_height = lock_size * 0.6
    shackle_top = lock_center[1] - shackle_height
    shackle_left = lock_center[0] - shackle_width/2
    shackle_right = lock_center[0] + shackle_width/2

    # Draw the shackle as a U shape
    draw.arc(
        [(shackle_left, shackle_top), (shackle_right, lock_center[1])],
        180, 0, fill=(255, 255, 255, 255), width=int(lock_size * 0.15)
    )
    draw.line(
        [(shackle_left, lock_center[1]), (shackle_left, shackle_top + shackle_height * 0.5)],
        fill=(255, 255, 255, 255), width=int(lock_size * 0.15)
    )
    draw.line(
        [(shackle_right, lock_center[1]), (shackle_right, shackle_top + shackle_height * 0.5)],
        fill=(255, 255, 255, 255), width=int(lock_size * 0.15)
    )

    # Draw a keyhole
    keyhole_center = (lock_center[0], lock_center[1] + lock_size * 0.5)
    keyhole_radius = lock_size * 0.15
    draw.ellipse(
        [(keyhole_center[0] - keyhole_radius, keyhole_center[1] - keyhole_radius),
         (keyhole_center[0] + keyhole_radius, keyhole_center[1] + keyhole_radius)],
        fill=(0, 0, 0, 255)
    )

    # Save the icon
    try:
        img.save(output_path)
        print(f"Icon saved to {output_path}")
        return True
    except Exception as e:
        print(f"Error saving icon: {str(e)}")
        return False

if __name__ == "__main__":
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, "icon.ico")

    create_icon(icon_path)
