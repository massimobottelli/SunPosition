import pygame
import sys
import math
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz, get_sun
from datetime import datetime
import pytz
import time as systime
import os
import json

# Initialize Pygame
pygame.init()

# Define window dimensions
screen_width = 500
screen_height = 700  # Increased height for both views (350 + 350 + 30)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SunPosition")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
GRAY = (169, 169, 169)

# Dimensions of the objects
house_size = 90
roof_height = 18
sun_radius = 15
ray_length = 5
sun_path_radius = 200

# Position of the house
house_x = (screen_width - house_size) // 2
house_y_side = screen_height - house_size - 30
house_y_top = (screen_height // 2 - house_size // 2) - 80
house_direction = 165  # 0 in North, 90 Est, 180 South, 270 West

# Position of the sun
sun_path_center_x = screen_width // 2
sun_path_center_y_side = house_y_side
sun_path_center_y_top = house_y_top + house_size // 2


# Load configuration from file
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')
try:
    with open(CONFIG_PATH, 'r') as config_file:
        config = json.load(config_file)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Errore nella lettura della configurazione: {e}")
    sys.exit(1)

# House configuration
house_config = config.get("house", {})
house_direction = house_config.get("direction", 165)
myLat = house_config.get("latitude", 45.0)
myLon = house_config.get("longitude", 9.0)
timezone = house_config.get("timezone", "UTC")

# Use configuration
location = EarthLocation(lat=myLat * u.deg, lon=myLon * u.deg, height=0 * u.m)
local_tz = pytz.timezone(timezone)


# Global variable to store the current altitude (to be used in graphical simulation)
current_altitude = 45  # Initial altitude (degrees)
current_azimuth = 0  # Initial azimuth (degrees)


def draw_house_side():
    """Draws the house in side view with a square base and a triangular roof."""
    pygame.draw.rect(screen, BLACK, (house_x, house_y_side, house_size, house_size), 2)
    pygame.draw.polygon(screen, BLACK, [(house_x, house_y_side),
                                        (house_x + house_size, house_y_side),
                                        (screen_width // 2, house_y_side - roof_height)], 2)


def draw_house_top():
    """Draws the house in top view with a square base."""
    pygame.draw.rect(screen, BLACK, (house_x, house_y_top, house_size / 2, house_size), 2)
    pygame.draw.rect(screen, BLACK, (house_x + house_size / 2 - 2, house_y_top, house_size / 2, house_size), 2)


def draw_sun_side(sun_angle):
    """Draws the sun and its rays in side view."""
    # Calculate the position of the sun
    sun_position_x = sun_path_center_x - sun_path_radius * math.cos(math.radians(sun_angle))
    sun_position_y = sun_path_center_y_side - sun_path_radius * math.sin(math.radians(sun_angle))

    # Draw the sun
    pygame.draw.circle(screen, ORANGE, (int(sun_position_x), int(sun_position_y)), sun_radius)

    # Draw sun rays
    for i in range(8):
        ray_angle = math.radians(45 * i)
        ray_start_x = sun_position_x + sun_radius * math.cos(ray_angle)
        ray_start_y = sun_position_y + sun_radius * math.sin(ray_angle)
        ray_end_x = sun_position_x + (sun_radius + ray_length) * math.cos(ray_angle)
        ray_end_y = sun_position_y + (sun_radius + ray_length) * math.sin(ray_angle)
        pygame.draw.line(screen, ORANGE, (int(ray_start_x), int(ray_start_y)),
                         (int(ray_end_x), int(ray_end_y)), 2)

    return sun_position_x, sun_position_y


def draw_sun_top(sun_angle):
    """Draws the sun and its rays in top view."""
    # Calculate the position of the sun
    sun_position_x = sun_path_center_x - sun_path_radius * math.cos(math.radians(sun_angle))
    sun_position_y = sun_path_center_y_top - sun_path_radius * math.sin(math.radians(sun_angle))

    # Draw the sun
    pygame.draw.circle(screen, ORANGE, (int(sun_position_x), int(sun_position_y)), sun_radius)

    # Draw sun rays
    for i in range(8):
        ray_angle = math.radians(45 * i)
        ray_start_x = sun_position_x + sun_radius * math.cos(ray_angle)
        ray_start_y = sun_position_y + sun_radius * math.sin(ray_angle)
        ray_end_x = sun_position_x + (sun_radius + ray_length) * math.cos(ray_angle)
        ray_end_y = sun_position_y + (sun_radius + ray_length) * math.sin(ray_angle)
        pygame.draw.line(screen, ORANGE, (int(ray_start_x), int(ray_start_y)),
                         (int(ray_end_x), int(ray_end_y)), 2)

    # Draw the "S" direction
    sun_position_x_S = sun_path_center_x - sun_path_radius * math.cos(math.radians(180 - house_direction))
    sun_position_y_S = sun_path_center_y_top - sun_path_radius * math.sin(math.radians(180 - house_direction))
    font = pygame.font.Font(None, 24)
    s_text = font.render("S", True, GRAY)
    screen.blit(s_text, (int(sun_position_x_S) + 10, int(sun_position_y_S) - 10))

    return sun_position_x, sun_position_y


def draw_sun_path_line(sun_position_x, sun_position_y, path_center_x, path_center_y):
    """Draws the line connecting the center of the sun with the center of the sun path."""
    pygame.draw.line(screen, GRAY, (int(sun_position_x), int(sun_position_y)),
                     (int(path_center_x), int(path_center_y)), 2)


def draw_angle_text(sun_angle, house_x, house_y):
    """Displays the angle near the house."""
    font = pygame.font.Font(None, 24)
    angle_text = font.render(f"{sun_angle:.2f}°", True, GRAY)
    screen.blit(angle_text, (house_x - house_size // 2 + 20, house_y - 30))


def track_and_update_sun():
    """Tracks the sun's position and updates the graphical simulation."""
    global current_altitude, current_azimuth
    clock = pygame.time.Clock()

    while True:
        try:
            # Get the current time in the local timezone
            dt = datetime.now(local_tz)
            time = Time(dt)

            # Set up the horizontal coordinate frame
            altaz_frame = AltAz(obstime=time, location=location)

            # Get the sun's position in AltAz coordinates
            sun = get_sun(time).transform_to(altaz_frame)

            # Update the global altitude and azimuth
            current_altitude = sun.alt.deg
            current_azimuth = sun.az.deg

            # Print results with timestamp
            print(f"[{dt.strftime('%Y-%m-%d %H:%M:%S')}] Altitude: {sun.alt:.2f}, Azimuth: {sun.az:.2f}")

        except Exception as e:
            print(f"An error occurred: {e}")

        # Handle events (like quitting the program)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        # Fill the screen with white color
        screen.fill(WHITE)

        # Draw the side view
        draw_house_side()
        sun_position_x, sun_position_y = draw_sun_side(current_altitude)
        draw_sun_path_line(sun_position_x, sun_position_y, sun_path_center_x, sun_path_center_y_side)
        draw_angle_text(current_altitude, house_x, house_y_side)

        # Draw the top view
        draw_house_top()
        sun_position_x, sun_position_y = draw_sun_top(current_azimuth - house_direction)
        draw_sun_path_line(sun_position_x, sun_position_y, sun_path_center_x, sun_path_center_y_top)
        draw_angle_text(current_azimuth, house_x, house_y_top)

        # Update the screen
        pygame.display.flip()

        # Wait for five seconds before the next update
        clock.tick(1)  # Ensure that the graphical loop updates once per second
        systime.sleep(1)


# Run the combined loop (track sun position and update graphics)
track_and_update_sun()
