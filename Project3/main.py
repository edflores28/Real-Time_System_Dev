import motor

max_value = 2000
min_value = 700

# MAIN
motor1 = motor.Motor(4, min_value, max_value)
motor2 = motor.Motor(14, min_value, max_value)
motor3 = motor.Motor(24, min_value, max_value)
motor4 = motor.Motor(18, min_value, max_value)


print("Motors should not be spinning at this point")
print("Enter a value between", min_value, max_value)
print("Or just hit enter to stop the motors")

while True:
    userIn = input()
    print("Setting motors to", userIn)
    if userIn >= min_value and userIn <= max_value:
        motor1.set_pwn(userIn)
        motor2.set_pwn(userIn)
        motor3.set_pwn(userIn)
        motor4.set_pwn(userIn)
    else:
        break
