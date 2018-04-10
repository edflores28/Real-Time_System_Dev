import motor

max_value = 2000
min_value = 800
value = 950

# MAIN
print("Initializing motors\n")
motor1 = motor.Motor(4, min_value, max_value)
motor2 = motor.Motor(14, min_value, max_value)
motor3 = motor.Motor(23, min_value, max_value)
motor4 = motor.Motor(25, min_value, max_value)

print("Enter a value - a, d, q, e, or s")
print("a - decrement speed by 10")
print("q - decrement speed by 100")
print("d - increment speed by 10")
print("e - increment speed by 100\n")

while True:
    print("Setting all motors to", value, "\n")
    motor1.set_pwm(value)
    motor2.set_pwm(value)
    motor3.set_pwm(value)
    motor4.set_pwm(value)
    
    userIn = input()
    print(userIn)
    if userIn == "d":
        value += 10
    elif userIn == "e":
        value += 100
    elif userIn == "q":
        value -= 100
    elif userIn == "a":
        value -= 10
    else:
        print("Stopping all motors");
        motor1.stopAll()
        motor2.stopAll()
        motor3.stopAll()
        motor4.stopAll()
        break;

    if value >= min_value and value <= max_value:
        print("Setting motors to", value,"\n")
        motor1.set_pwm(value)
        motor2.set_pwm(value)
        motor3.set_pwm(value)
        motor4.set_pwm(value)
    else:
        print("No changes made to motor values","\n")

