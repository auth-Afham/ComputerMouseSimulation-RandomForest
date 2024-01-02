import pyautogui
import time
import math
from pynput.mouse import Listener as MouseListener, Button, Controller
from PIL import Image
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# Define SCREEN_WIDTH and SCREEN_HEIGHT before calling the function
SCREEN_WIDTH = 1920  # Change this value to your screen width
SCREEN_HEIGHT = 1080  # Change this value to your screen height

# Get the size of the resized screenshot
RESIZED_WIDTH, RESIZED_HEIGHT = 16, 9

# temp_data = [cursor_x, cursor_y, cursor_angle, cursor_speed, cursor_button] + [Each pixel's RGB values, ...]
full_data = []
temp_data = []

cursor_angle_model = None
cursor_speed_model = None
cursor_button_model = None

user_movement = False 

def print_non_rgb_data(data):
    # Print the non-rgb data from data
    non_rgb_data = []

    for temp in data:
        non_rgb_data.append(temp[:5])  # Extract the first five elements

    print("\nNon-RGB Data:", non_rgb_data)

def print_clean_2D_array(data):
    print("\nClean Data:")
    for count, temp in enumerate(data):
        print(f"\n{count}:\n", temp)

def initialize_dataset(RESIZED_WIDTH, RESIZED_HEIGHT, full_data, temp_data):
    temp_data = [0, 0, 0, 0, 0]

    # Iterate through each pixel and get its RGB values
    for y in range(RESIZED_HEIGHT):
        for x in range(RESIZED_WIDTH):
            temp_data.append(0) # Red
            temp_data.append(0) # Green
            temp_data.append(0) # Blue

    full_data.append(temp_data.copy())
    full_data.append(temp_data.copy())

    return full_data, temp_data

# Initialize RandomForest models
def initialize_randomforest_models():
    global cursor_angle_model, cursor_speed_model, cursor_button_model

    # Assuming cursor_angle_model and cursor_speed_model are RandomForest models
    cursor_angle_model = RandomForestRegressor()
    cursor_speed_model = RandomForestRegressor()
    cursor_button_model = RandomForestRegressor()

# Function to calculate speed and angle between two cursor positions
def get_cursor_position_and_movement(temp_data):
    # Get the current cursor position
    x1, y1 = pyautogui.position()
    temp_data[0], temp_data[1] = int(x1), int(y1)

    # Wait for a short period to get the next cursor position
    time.sleep(0.1)

    # Get the new cursor position
    x2, y2 = pyautogui.position()

    # Calculate the angle between the two points (in radians)
    angle = math.atan2(y2 - y1, x2 - x1)

    # Convert the angle to degrees and normalize it to the range [0, 360]
    y_angle = (math.degrees(angle) + 360) % 360
    print("y_angle:", y_angle)

    temp_data[2] = int(y_angle)

    # Calculate the distance between the two points (speed)
    y_speed = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    print("y_speed:", y_speed)

    temp_data[3] = int(y_speed)

    if temp_data[2] != 0 and temp_data[3] != 0:
        return True, temp_data
    else:
        return False, temp_data

# Callback function for mouse clicks
def get_cursor_click(x, y, button, pressed):
    global temp_data

    if pressed:
        if button == Button.left: 
            temp_data[4] = 1
            print(f"User pressed left mouse button at index {temp_data[4]}!")
        elif button == Button.right:
            temp_data[4] = 2
            print(f"User pressed right mouse button at index {temp_data[4]}!")
    else:
        temp_data[4] = 0

def get_screenshot(RESIZED_WIDTH, RESIZED_HEIGHT, temp_data):
    # Capture screenshot
    screenshot = pyautogui.screenshot()

    # Resize the screenshot to 16x9 pixels
    screenshot = screenshot.resize((RESIZED_WIDTH, RESIZED_HEIGHT), Image.Resampling.LANCZOS)

    count = 5

    # Iterate through each pixel and get its RGB values
    for y in range(RESIZED_HEIGHT):
        for x in range(RESIZED_WIDTH):
            try:
                pixel_rgb = screenshot.getpixel((x, y))
                temp_data[count] = pixel_rgb[0] # Red
                temp_data[count + 1] = pixel_rgb[1] # Green
                temp_data[count + 2] = pixel_rgb[2] # Blue

                count += 3
            except IndexError:
                print(f"Index out of bound error at count: {count}")
    
    return temp_data

# Train RandomForest models
def train_randomforest_models(full_data):
    global cursor_angle_model, cursor_speed_model, cursor_button_model

    # Extract features (X) and targets (y_angle, y_speed)
    X_angle = [data[:2] + data[3:] for data in full_data]
    X_speed = [data[:3] + data[4:] for data in full_data]
    X_button = [data[:4] + data[5:] for data in full_data]

    y_angle = [data[2] for data in full_data]
    y_speed = [data[3] for data in full_data]
    y_button = [data[4] for data in full_data]

    # Train cursor angle model
    cursor_angle_model.fit(X_angle, y_angle)

    # Train cursor speed model
    cursor_speed_model.fit(X_speed, y_speed)

    cursor_button_model.fit(X_button, y_button)

def predict_cursor_angle(temp_data):
    global cursor_angle_model

    X_angle_temp = [temp_data[:2] + temp_data[3:]]
    
    # Make predictions on the test set
    y_angle_pred = cursor_speed_model.predict(X_angle_temp)[0]
    print('y_angle_pred:', y_angle_pred)

    temp_data[2] = int(max(0, min(y_angle_pred, 359)))

    return temp_data

def predict_cursor_speed(temp_data):
    global cursor_speed_model

    X_speed_temp = [temp_data[:3] + temp_data[4:]]
    
    # Make predictions on the test set
    y_speed_pred = cursor_speed_model.predict(X_speed_temp)[0]
    print('y_speed_pred:', y_speed_pred)

    temp_data[3] = int(max(0, min(y_speed_pred, 359)))

    return temp_data

def predict_cursor_button(temp_data):
    global cursor_button_model

    X_button_temp = [temp_data[:4] + temp_data[5:]]
    
    # Make predictions on the test set
    y_button_pred = cursor_button_model.predict(X_button_temp)[0]
    # print('y_speed_pred:', y_speed_pred)

    temp_data[4] = int(max(0, min(y_button_pred, 2)))

    return temp_data

def set_cursor_movement(SCREEN_WIDTH, SCREEN_HEIGHT, temp_data, steps=100, safety_margin=10):
    # Initialize the mouse controller
    mouse = Controller()

    # Convert the angle from degrees to radians
    angle_rad = math.radians(temp_data[2])

    # Calculate the change in x and y coordinates based on speed and angle
    delta_x = temp_data[3] * math.cos(angle_rad)
    delta_y = temp_data[3] * math.sin(angle_rad)

    # Get the current cursor position
    current_x, current_y = mouse.position

    # Calculate the step size for x and y coordinates
    step_x = delta_x / steps
    step_y = delta_y / steps

    # Move the cursor smoothly
    for _ in range(steps):
        current_x += step_x
        current_y += step_y

        # Ensure the cursor stays within the screen boundaries
        current_x = max(safety_margin, min(current_x, SCREEN_WIDTH - safety_margin))
        current_y = max(safety_margin, min(current_y, SCREEN_HEIGHT - safety_margin))

        # Move the cursor to the new position
        mouse.position = (current_x, current_y)

        time.sleep(0.01)

def set_cursor_button(temp_data):
    mouse = Controller()

    button = temp_data[4] 

    if button == 1:
        mouse.click(Button.left)
        print(f"Machine pressed left mouse button at index {button}!")
    elif button == 2:
        mouse.click(Button.right)
        print(f"Machine pressed right mouse button at index {button}!")

full_data, temp_data = initialize_dataset(RESIZED_WIDTH, RESIZED_HEIGHT, full_data, temp_data)

# Initialize RandomForest models
initialize_randomforest_models()

# Set up mouse listener
with MouseListener(on_click=get_cursor_click) as mouse_listener:
    try:
        while True:
            # Example usage:
            # Capture cursor movement
            print('\ntemp_data:', temp_data[:5])

            user_movement, temp_data = get_cursor_position_and_movement(temp_data)
            temp_data = get_screenshot(RESIZED_WIDTH, RESIZED_HEIGHT, temp_data)

            # Train RandomForest models with full_data
            train_randomforest_models(full_data)

            if not user_movement:
                temp_data = predict_cursor_angle(temp_data)
                temp_data = predict_cursor_speed(temp_data)
                temp_data = predict_cursor_button(temp_data)

                print('Predict:', temp_data[:5])

                set_cursor_movement(SCREEN_WIDTH, SCREEN_HEIGHT, temp_data)
                set_cursor_button(temp_data)

            # Append temp_data to full_data (create a new copy using temp_data.copy())
            full_data.append(temp_data.copy())

            # Optional: Sleep to control the polling frequency
            time.sleep(0.1)
    except KeyboardInterrupt:
        # Stop the listener when interrupted
        mouse_listener.stop()
        mouse_listener.join()
    finally:
        print_non_rgb_data(full_data)
        # print_clean_2D_array(full_data)
        pass
