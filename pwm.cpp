#include <wiringPi.h>
#include <iostream>
#include <unistd.h>
#include <ncurses.h>

// Use PWM1_M2 (WiringPi Pin 13 = BCM GPIO19 = Physical Pin 35)
// Use PWM0_M1 (WiringPi Pin 18 = BCM GPIO18 = Physical Pin 12)
#define SERVO1_PIN 0  // PWM1_M2 (Servo 1)
#define SERVO2_PIN 15  // PWM0_M1 (Servo 2)

// MG90S Servo min/max pulse width (in microseconds)
#define PWM_RANGE 2000  // Full range (20ms period, 50Hz)
#define MIN_DUTY 50  // 0.5ms pulse width (0°)
#define MAX_DUTY 250  // 2.5ms pulse width (180°)

void setup_pwm(int pin) {
    wiringPiSetup();  // Initialize WiringPi
    pinMode(pin, PWM_OUTPUT);
    pwmSetMode(pin, PWM_MODE_MS);   // Set PWM mode
    pwmSetClock(pin, 192);          // Set clock divisor for 50Hz PWM
    pwmSetRange(pin, PWM_RANGE);    // Set range for duty cycle
}

void set_servo_angle(int pin, int angle) {
    int duty_cycle = MIN_DUTY + (angle / 180.0) * (MAX_DUTY - MIN_DUTY);
    pwmWrite(pin, duty_cycle);
}

void cleanup_pwm(int pin) {
    pwmWrite(pin, 0);
}

void interactive_control() {
    initscr();
    cbreak();
    noecho();
    keypad(stdscr, TRUE);
    nodelay(stdscr, TRUE);
    curs_set(0);
    timeout(100);

    int angle_servo1 = 90;  // Default position for Servo 1
    int angle_servo2 = 90;  // Default position for Servo 2
    set_servo_angle(SERVO1_PIN, angle_servo1);
    set_servo_angle(SERVO2_PIN, angle_servo2);

    mvprintw(0, 0, "Control Servos with Arrow Keys:");
    mvprintw(1, 0, "Servo 1: Up/Down | Servo 2: Left/Right");
    mvprintw(2, 0, "Press 'q' to quit.");
    refresh();

    while (true) {
        int key = getch();

        if (key == 'q') {
            break;
        } else if (key == KEY_UP) {
            angle_servo1 = std::min(180, angle_servo1 + 1);
            set_servo_angle(SERVO1_PIN, angle_servo1);
        } else if (key == KEY_DOWN) {
            angle_servo1 = std::max(0, angle_servo1 - 1);
            set_servo_angle(SERVO1_PIN, angle_servo1);
        } else if (key == KEY_LEFT) {
            angle_servo2 = std::max(0, angle_servo2 - 1);
            set_servo_angle(SERVO2_PIN, angle_servo2);
        } else if (key == KEY_RIGHT) {
            angle_servo2 = std::min(180, angle_servo2 + 1);
            set_servo_angle(SERVO2_PIN, angle_servo2);
        }

        clear();
        mvprintw(0, 0, "Control Servos with Arrow Keys:");
        mvprintw(1, 0, "Servo 1: Up/Down | Servo 2: Left/Right");
        mvprintw(2, 0, "Press 'q' to quit.");
        mvprintw(4, 0, "Servo 1 Angle: %d°", angle_servo1);
        mvprintw(5, 0, "Servo 2 Angle: %d°", angle_servo2);
        refresh();
    }

    endwin();
}

int main() {
    try {
        setup_pwm(SERVO1_PIN);
        setup_pwm(SERVO2_PIN);
        interactive_control();
    } catch (...) {
        std::cerr << "\nProgram terminated." << std::endl;
    }
    cleanup_pwm(SERVO1_PIN);
    cleanup_pwm(SERVO2_PIN);
    return 0;
}