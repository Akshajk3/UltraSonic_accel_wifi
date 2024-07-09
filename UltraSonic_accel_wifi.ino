#include <WiFi.h>
#define port 80

#include <MPU6050_tockn.h>
#include <Wire.h>
#define SDA 13
#define SCL 14
MPU6050 mpu6050(Wire);//Attach the IIC
int16_t ax,ay,az;//define acceleration values of 3 axes
int16_t gx,gy,gz;//define variables to save the values in 3 axes of gyroscope
long timer = 0;

#define trigPin 32 //generating pulse
#define echoPin 33 
const char *ssid_Router = "Kanumuri-TP_2GEXT"; //input your wifi name
const char *password_Router = "9848016272"; //input your wifi passwords
WiFiServer server(port);


void setup()
{
  Serial.begin(115200);
 Wire.begin(SDA, SCL); //attach the IIC pin
 mpu6050.begin(); //initialize the MPU6050
 mpu6050.calcGyroOffsets(true); //get the offsets value

  pinMode (trigPin, OUTPUT);// set trigPin to output mode
  pinMode (echoPin, INPUT); 
  Serial.begin(115200);
  Serial.printf("\nConnecting to ");
  Serial.println(ssid_Router);
  WiFi.disconnect();
  WiFi.begin(ssid_Router, password_Router);
  delay(1000);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.printf("IP port: %d\n",port);
  server.begin(port);
  WiFi.setAutoReconnect(true);
}
void getMotion6(void){
 ax=mpu6050.getRawAccX();//gain the values of X axis acceleration raw data
 ay=mpu6050.getRawAccY();//gain the values of Y axis acceleration raw data
 az=mpu6050.getRawAccZ();//gain the values of Z axis acceleration raw data
 gx=mpu6050.getRawGyroX();//gain the values of X axis Gyroscope raw data
 gy=mpu6050.getRawGyroX();//gain the values of Y axis Gyroscope raw data
 gz=mpu6050.getRawGyroX();//gain the values of Z axis Gyroscope raw data
}


float getTripT() {
  unsigned long pingTime;
  float distance;
  digitalWrite (trigPin, HIGH); 
  delayMicroseconds(10); //sending out a 10us's high pulse
  digitalWrite(trigPin, LOW);
  pingTime = pulseIn(echoPin, HIGH);
  return pingTime;
}
void loop(){
  WiFiClient client = server.available(); // listen for incoming clients
  if (client) { // if you get a client
    Serial.println("Client connected.");
    while (client.connected()) { // loop while the client's connected
      float tripT = getTripT();
      Serial.print(tripT);+
      client.print(String(tripT) + String(", "));
      mpu6050.update(); //update the MPU6050
      getMotion6(); //gain the values of Acceleration and Gyroscope value
      Serial.print("a/g:\t");
      Serial.print(ax); Serial.print("\t");
      Serial.print(ay); Serial.print("\t");
      Serial.print(az); Serial.print("\t");
      Serial.print(gx); Serial.print("\t\t");
      Serial.print(gy); Serial.print("\t\t");
      Serial.println(gz);
      String accel = String("a/g: ") + String(ax) + String("\t") + String(ay) + String("\t") + String(az) + String("\t") + String(gx) + String("\t") + String(gy) + String("\t") + String(gz);
      client.println(accel);
      delay(500);
    }
    client.stop(); // stop the client connecting.
    Serial.println("Client Disconnected.");
  }
}