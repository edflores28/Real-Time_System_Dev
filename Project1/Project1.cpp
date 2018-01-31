#include <Arduino.h>
#include <Morse.h>

// Maximum size of the buffer
#define MAX_BUFFER 100

// Global variables.
int ledPin = 13; // The pin on the Arduino
String input;
char recv = 0;
char buffer[MAX_BUFFER];
Morse morse(ledPin, 1200); // Morse code set at 1200WPM

// Setup stuff.
void setup()
{
	// Start the serial interface for the keyboard.
	Serial.begin(9600);
}

// Main loop.
void loop()
{
    if (Serial.available() > 0) {

    	// Read the incoming byte from the serial interface
        recv = Serial.read();

        // Only keep the byte if it's a letter or number
        // than can be represented in morse code.
        // This uses the decimal representation of the
        // ASCII characters.
        if (((recv >= 48) && (recv <= 57)) ||
        	((recv >= 65) && (recv <= 90)) ||
			((recv >= 97) && (recv <= 122)) ||
			(recv == 32))
        {
        	input.concat(recv);
        }

        // Once the new line character has been received
        // convert the string to morse code.
        if (recv == 13)
        {
        	if (!morse.busy)
        	{
        	Serial.println("User input: " + input);
        	// Convert the string into a char array
        	input.toCharArray(buffer,MAX_BUFFER);

        	// Queue up the message for processing.
        	morse.send(buffer);

        	// Clear out the buffer and string
        	memset(buffer, 0, sizeof(buffer));
        	input = "";
        	}
        }
    }

    // Update the morse code.
    delay(300);
	morse.update();
}
