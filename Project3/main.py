import motor

max_value = 2000
min_value = 800
default = 1000

# MAIN
print("Initializing motors")
motor1 = motor.Motor(4, min_value, max_value)
motor2 = motor.Motor(14, min_value, max_value)
motor3 = motor.Motor(23, min_value, max_value)
motor4 = motor.Motor(25, min_value, max_value)


print("Enter a value - a, d, q, e, or s")

while True:
    motor1.set_pwn(default)
    motor2.set_pwn(default)
    motor3.set_pwn(default)
    motor4.set_pwn(default)
    
    userIn = input()
    if userIn == "d":
        default += 10
    elif userIn == "e":
        default += 100
    elif userIn == "q":
        default -= 100
    elif userIn == "a":
        default -= 10
    elif userIn == "s":
        motor1.stopAll()
        motor2.stopAll()
        motor3.stopAll()
        motor4.stopAll()
        break;

    print("Setting motors to", default)
    if default >= min_value and default <= max_value:
        motor1.set_pwn(default)
        motor2.set_pwn(default)
        motor3.set_pwn(default)
        motor4.set_pwn(default)

