#include <Arduino.h>
#include <SimpleDHT.h>
#include <TimerOne.h>
#include <SD.h>

#define DHTPIN 7

// Global variables
SimpleDHT11 dht11;
File SDfile;
bool hasTenSecondsPassed = false;
bool hasFiveSecondsPassed = false;
int counter = 0;
int tenSecondCounter = 0;
String file = "temp.csv";

// Method is called every 5 seconds that
// just toggles flags
void isr() {
	if (!hasFiveSecondsPassed)
		hasFiveSecondsPassed = true;
	else {
		hasTenSecondsPassed = true;
		hasFiveSecondsPassed = false;
	}
}

void setup() {
	// Startup the serial interface
	Serial.begin(9600);
	// Initialize the interrupt to occur every  5 seconds
	Timer1.initialize(5000000);
	// Attach the interrupt
	Timer1.attachInterrupt(isr);
	// Set pin 10 to output
	pinMode(10, OUTPUT);

	if (!SD.begin(10)) {
		Serial.println("initialization failed!");
	    return;
	}
	// Determine if the file already exists and
	// remove it
	if (SD.exists(file))
		SD.remove(file);

	// Open the file for writing
	SDfile = SD.open(file,FILE_WRITE);
	if (SDfile) {
		// Write the first data entries
		SDfile.println("0,0.0");
		Serial.println("initialization done.");
	}
}

void loop() {

	// Start processing once 10 seconds have passed
	if (hasTenSecondsPassed){

		// Read the DHT11 for the temperature
		byte temperature = 0;
		int err = SimpleDHTErrSuccess;
		if ((err = dht11.read(DHTPIN, &temperature, NULL, NULL)) != SimpleDHTErrSuccess) {
			return;
		}

		// Convert the temperature to fahrenheit
		float fahr = (float(temperature) * 1.8) + 32;

		// Increment the ten second counter
		tenSecondCounter += 10;

		// Write the seconds and temp to file as csv
		SDfile.print(String(tenSecondCounter) + ",");
		SDfile.println(float(fahr),1);

		// Toggle the flag
		hasTenSecondsPassed = false;

		// Once 10 minutes have passed close the file and exit
		if (tenSecondCounter == 600) {
			Timer1.detachInterrupt();
			SDfile.close();
			exit(0);
		}
	}
}

