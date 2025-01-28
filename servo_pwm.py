import os
import time
import curses

# Correct PWM channel numbers
SERVO1_CHANNEL = 0  # PWM channel for Servo 1 on pwmchip0
SERVO2_CHANNEL = 0  # PWM channel for Servo 2 on pwmchip1

PWM_CHIP1 = "pwmchip0"  # PWM chip for Servo 1
PWM_CHIP2 = "pwmchip1"  # PWM chip for Servo 2

# Helper functions for PWM setup and control
def setup_pwm(chip, channel):
    try:
        # Export the PWM channel
        with open(f"/sys/class/pwm/{chip}/export", "w") as f:
            f.write(str(channel))

        # Set the period (20ms for 50Hz)
        with open(f"/sys/class/pwm/{chip}/pwm{channel}/period", "w") as f:
            f.write("20000000")

        # Enable the PWM output
        with open(f"/sys/class/pwm/{chip}/pwm{channel}/enable", "w") as f:
            f.write("1")
    except FileNotFoundError as e:
        print(f"Error: {e}. Check if {chip} is available.")
        exit(1)
    except PermissionError as e:
        print(f"Error: {e}. Run the script as root.")
        exit(1)

def set_duty_cycle(chip, channel, duty_cycle):
    try:
        # Set the duty cycle
        with open(f"/sys/class/pwm/{chip}/pwm{channel}/duty_cycle", "w") as f:
            f.write(str(duty_cycle))
    except FileNotFoundError as e:
        print(f"Error: {e}. Check if the PWM channel is exported and enabled.")

def cleanup_pwm(chip, channel):
    try:
        # Disable the PWM output
        with open(f"/sys/class/pwm/{chip}/pwm{channel}/enable", "w") as f:
            f.write("0")

        # Unexport the PWM channel
        with open(f"/sys/class/pwm/{chip}/unexport", "w") as f:
            f.write(str(channel))
    except FileNotFoundError as e:
        print(f"Error during cleanup: {e}")

def set_servo_angle(chip, channel, angle):
    # Map the angle (0-180 degrees) to duty cycle (1ms-2ms pulse width)
    duty_cycle = int(1000000 + (angle / 180.0) * 1000000)
    set_duty_cycle(chip, channel, duty_cycle)

def interactive_control(screen):
    curses.curs_set(0)
    screen.nodelay(True)
    screen.timeout(100)

    angle_servo1 = 90  # Default angle for Servo 1
    angle_servo2 = 90  # Default angle for Servo 2

    set_servo_angle(PWM_CHIP1, SERVO1_CHANNEL, angle_servo1)
    set_servo_angle(PWM_CHIP2, SERVO2_CHANNEL, angle_servo2)

    screen.addstr(0, 0, "Control Servos with Arrow Keys:")
    screen.addstr(1, 0, "Servo 1: Up/Down | Servo 2: Left/Right")
    screen.addstr(2, 0, "Press 'q' to quit.")

    while True:
        try:
            key = screen.getch()

            if key == ord('q'):
                break
            elif key == curses.KEY_UP:
                angle_servo1 = min(180, angle_servo1 + 5)
                set_servo_angle(PWM_CHIP1, SERVO1_CHANNEL, angle_servo1)
            elif key == curses.KEY_DOWN:
                angle_servo1 = max(0, angle_servo1 - 5)
                set_servo_angle(PWM_CHIP1, SERVO1_CHANNEL, angle_servo1)
            elif key == curses.KEY_LEFT:
                angle_servo2 = max(0, angle_servo2 - 5)
                set_servo_angle(PWM_CHIP2, SERVO2_CHANNEL, angle_servo2)
            elif key == curses.KEY_RIGHT:
                angle_servo2 = min(180, angle_servo2 + 5)
                set_servo_angle(PWM_CHIP2, SERVO2_CHANNEL, angle_servo2)

            # Update screen
            screen.clear()
            screen.addstr(0, 0, "Control Servos with Arrow Keys:")
            screen.addstr(1, 0, "Servo 1: Up/Down | Servo 2: Left/Right")
            screen.addstr(2, 0, "Press 'q' to quit.")
            screen.addstr(4, 0, f"Servo 1 Angle: {angle_servo1} degrees")
            screen.addstr(5, 0, f"Servo 2 Angle: {angle_servo2} degrees")

        except Exception as e:
            screen.addstr(7, 0, f"Error: {e}")

if __name__ == "__main__":
    try:
        # Setup PWM for both servos
        setup_pwm(PWM_CHIP1, SERVO1_CHANNEL)
        setup_pwm(PWM_CHIP2, SERVO2_CHANNEL)
        
        curses.wrapper(interactive_control)
    except KeyboardInterrupt:
        print("\nProgram terminated.")
    finally:
        # Cleanup PWM
        cleanup_pwm(PWM_CHIP1, SERVO1_CHANNEL)
        cleanup_pwm(PWM_CHIP2, SERVO2_CHANNEL)
