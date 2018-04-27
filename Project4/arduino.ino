#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

#define TOTAL_SAMPLES 50

volatile int roll;
volatile int pitch;
volatile int throttle;
volatile int yaw;
String rc_out;
String imu_out;
Adafruit_BNO055 bno = Adafruit_BNO055(55);

// This methods samples the PWM pin
int sample_pin(int pin)
{
  int i, value = 0;
  for (i = 0; i < TOTAL_SAMPLES; i++)
  {
    int temp = pulseIn(pin, HIGH);
    if (temp == 0)
      break;
     value += temp;
  }
    return value/i;
}

// This method reads the channels of the receiver
// and sends a message
void process_receiver()
{
  yaw = sample_pin(4);
  throttle = sample_pin(5);
  pitch = sample_pin(6);
  roll = sample_pin(7);
  rc_out = "CTL,";
  rc_out += String(yaw) + ",";
  rc_out += String(throttle) + ",";
  rc_out += String(pitch) + ",";
  rc_out += String(roll);
  Serial.println(rc_out);
}

// This method obtains the values from the IMU
// and sends a message
void process_imu()
{
  /* Get a new sensor event */
  sensors_event_t event;
  bno.getEvent(&event);
  imu_out = "NAV,";
  imu_out += String(event.orientation.x) + ","; // Yaw
  imu_out += String(event.orientation.z) + ","; // Pitch
  imu_out += String(event.orientation.y); // Roll
  Serial.println(imu_out);
}

// Setup
void setup()
{
  pinMode(4, INPUT); // Channel for Yaw
  pinMode(5, INPUT); // Channel for Throttle
  pinMode(6, INPUT); // Channel for Pitch
  pinMode(7, INPUT); // Channel for Roll

  Serial.begin(9600);

  if(!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }

   delay(1000);
   bno.setExtCrystalUse(true);
}

// Main loop
void loop()
{
  process_receiver();
  process_imu();
}
