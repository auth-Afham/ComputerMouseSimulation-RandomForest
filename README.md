# Cursor Control and Prediction

![Project Image](https://media.licdn.com/dms/image/sync/D5627AQEGcYDpr7U6vw/articleshare-shrink_480/0/1704080717753?e=1704794400&v=beta&t=sU2vkllTktipTRm8c12l-WmHMMkE1O8d084NDtpsqZw)

This Python script demonstrates cursor control and prediction using machine learning models. It captures cursor movement, mouse clicks, and screen pixels to train and predict cursor angle, speed, and button clicks.

## Requirements

Ensure you have the following Python libraries installed:

```bash
pip install pyautogui
pip install pynput
pip install pillow
pip install pandas
pip install numpy
pip install scikit-learn
```

## Usage

1. **Define Screen Size**: Set the `SCREEN_WIDTH` and `SCREEN_HEIGHT` variables according to your screen dimensions.

2. Download Pre-built Executable:

- You can download the pre-built executable version of this script from [this link](https://drive.google.com/drive/folders/1MCnatHxJNPOmy1-nLrXWj7jebzb7EKd9).
- Install the executable locally.

3. **Run the Script**: Execute the script using Python:

   ```bash
   python ComputerMouseSimulation.py
   ```

4. **Cursor Movement and Prediction**: The script will capture cursor movement and screen pixels, predict cursor angle, speed, and button clicks using trained models, and simulate cursor movement accordingly.

5. **Keyboard Interrupt (Ctrl+C)**: To stop the script, use a keyboard interrupt (Ctrl+C). The script will print non-RGB data collected during execution.

**Note:** This script uses machine learning models to predict cursor behavior. Make sure to train the models before running the script for accurate predictions.

## Additional Information

- The `initialize_dataset` function sets up the initial dataset structure.
- RandomForest models are initialized using the `initialize_randomforest_models` function.
- Cursor movement and screen pixels are captured in the `get_cursor_position_and_movement` and `get_screenshot` functions.
- The `train_randomforest_models` function trains the Random Forest models using the dataset.
- Prediction functions (`predict_cursor_angle`, `predict_cursor_speed`, `predict_cursor_button`) predict cursor behavior based on the captured data.
- The `set_cursor_movement` and `set_cursor_button` functions simulate cursor movement and button clicks.

Feel free to modify the script according to your requirements and integrate it into your projects.
