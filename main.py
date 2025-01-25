# Add the directory containing the control module to the PYTHONPATH
import control
from control import servo, calculations
print(control.VERSION)

sum_result = calculations.add_numbers(2, 3)
print("Sum:", sum_result)

product_result = calculations.multiply_numbers(4, 5)
print("Product:", product_result)

servo.greet_user("allli")

#control.servo.func2()