#include <Wire.h>
#include <ArduinoJson.h>

const float VCC   = 5.0;// supply voltage 5V or 3.3V. If using PCB, set to 5V only.
const int model = 2;   // enter the model (see below)
float cutOffLimit = 1.0;// reading cutt off current. 1.00 is 1 Amper

/*
   "ACS758LCB-050B",// for model use 0
   "ACS758LCB-050U",// for model use 1
   "ACS758LCB-100B",// for model use 2
   "ACS758LCB-100U",// for model use 3
   "ACS758KCB-150B",// for model use 4
   "ACS758KCB-150U",// for model use 5
   "ACS758ECB-200B",// for model use 6
   "ACS758ECB-200U"// for model use  7
   sensitivity array is holding the sensitivy of the  ACS758
   current sensors. Do not change.
*/
float sensitivity[] = {
  40.0,// for ACS758LCB-050B
  60.0,// for ACS758LCB-050U
  20.0,// for ACS758LCB-100B
  40.0,// for ACS758LCB-100U
  13.3,// for ACS758KCB-150B
  16.7,// for ACS758KCB-150U
  10.0,// for ACS758ECB-200B
  20.0,// for ACS758ECB-200U
};

/*
   quiescent Output voltage is factor for VCC that appears at output
   when the current is zero.
   for Bidirectional sensor it is 0.5 x VCC
   for Unidirectional sensor it is 0.12 x VCC
   for model ACS758LCB-050B, the B at the end represents Bidirectional (polarity doesn't matter)
   for model ACS758LCB-100U, the U at the end represents Unidirectional (polarity must match)
   Do not change.
*/
float quiescent_Output_voltage [] = {
  0.5,// for ACS758LCB-050B
  0.12,// for ACS758LCB-050U
  0.5,// for ACS758LCB-100B
  0.12,// for ACS758LCB-100U
  0.5,// for ACS758KCB-150B
  0.12,// for ACS758KCB-150U
  0.5,// for ACS758ECB-200B
  0.12,// for ACS758ECB-200U
};
const float FACTOR = sensitivity[model] / 1000; // set sensitivity for selected model
const float QOV =   quiescent_Output_voltage [model] * VCC;// set quiescent Output voltage for selected model
const float cutOff = FACTOR / cutOffLimit; // convert current cut off to mV

//SoftwareSerial BTSerial(10, 11); // RX | TX

const size_t capacity = 4*JSON_OBJECT_SIZE(3);

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  DynamicJsonDocument doc(capacity);
  float ai0 = analogRead(A0), ai1 = analogRead(A1), ai2 = analogRead(A2);
  
  // READ data from A0
  float voltage_raw =   (5.0 / 1023.0) * ai0; // Read the voltage from sensor
  float voltage =  voltage_raw - QOV + 0.007 ;// 0.007 is a value to make voltage zero when there is no current
  float current = voltage / FACTOR;

  JsonObject a0 = doc.createNestedObject("a0");

  if (abs(voltage) > cutOff ) {
    a0["voltage"] = voltage;
    a0["ampere"] = current;
    a0["watt"] = voltage * current;
  } else {
    a0["voltage"] = NULL;
    a0["ampere"] = NULL;
    a0["watt"] = NULL;
  }

  // READ data from A1
  voltage_raw =   (5.0 / 1023.0) * ai1; // Read the voltage from sensor
  voltage =  voltage_raw - QOV + 0.007 ;// 0.007 is a value to make voltage zero when there is no current
  current = voltage / FACTOR;

  JsonObject a1 = doc.createNestedObject("a1");

  if (abs(voltage) > cutOff ) {
    a1["voltage"] = voltage;
    a1["ampere"] = current;
    a1["watt"] = voltage * current;
  } else {
    a1["voltage"] = NULL;
    a1["ampere"] = NULL;
    a1["watt"] = NULL;
  }

  // READ data from A2
  voltage_raw =   (5.0 / 1023.0) * ai2; // Read the voltage from sensor
  voltage =  voltage_raw - QOV + 0.007 ;// 0.007 is a value to make voltage zero when there is no current
  current = voltage / FACTOR;

  JsonObject a2 = doc.createNestedObject("a2");

  if (abs(voltage) > cutOff ) {
    a2["voltage"] = voltage;
    a2["ampere"] = current;
    a2["watt"] = voltage * current;
  } else {
    a2["voltage"] = NULL;
    a2["ampere"] = NULL;
    a2["watt"] = NULL;
  }

  //serializeJson(doc, BTSerial);
  serializeJson(doc, Serial);
  Serial.write('\n');
  Serial.flush();
  //BTSerial.print("test");

  delay(5000);
}
