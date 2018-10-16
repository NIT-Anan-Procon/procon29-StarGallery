#include<Wire.h>
#include<SPI.h>
#include<math.h>
//#include <ArduinoJson.h>


#define slaveMPU 0x69
#define slaveMagnet 0x0C
#define pi 3.141592653589793
#define Time 500

int16_t AccX=0, AccY=0, AccZ=0;
float ComX=0, ComY=0, ComZ=0;
byte AcXH, AcXL, AcYH, AcYL, AcZH, AcZL, CoXH, CoXL, CoYH, CoYL, CoZH, CoZL, ST2;

void writeSPI(byte regAddr, byte value) {
  digitalWrite(8, LOW);
  SPI.transfer(regAddr);
  SPI.transfer(value);
  digitalWrite(8, HIGH);
}

byte readSPI(byte regAddr) {
  byte data = 0;
  digitalWrite(8, LOW);
  SPI.transfer(regAddr | 0x80);
  data = SPI.transfer(0xff);
  digitalWrite(8, HIGH);
  return data;
}

int16_t setSPI(byte High, byte Low) {
  int16_t Data = 0;
  Data=(High*256)+Low;
  return Data;
}

float gAcc(int16_t Ax, int16_t Ay){   //鏡筒の傾きを返す
  float x = Ax*0.000061;
  float y = Ay*0.000061;
  float Gra = atan2(x, y);
  Gra = Gra*180.0/pi;

  return Gra;
}

void writeI2C(byte slave, byte address, byte value){  //スレイブを定義、指定されたAdressにvalue(データ)を書き込む
  Wire.beginTransmission(slave);
  Wire.write(address);  //アドレスの指定
  Wire.write(value);    //書き込むデータ
  Wire.endTransmission();
  delay(50);
}

void readI2C(byte slave, byte address, int count) {  //スレイブを定義、addressからcount分のデータを読み込む
  Wire.requestFrom(slave, count);
  Wire.beginTransmission(slave);
  Wire.write(address);        //アドレスの指定
  Wire.endTransmission();
  delay(50);
}

void setI2C() {  //スリープモードから起動させる
  Wire.begin(0x69);
  writeI2C(slaveMPU, 0x6B, 0x00);
  writeI2C(slaveMPU, 0x37, 0x02);
  writeI2C(slaveMagnet, 0x0A, 0x12);
}

int setData(byte High, byte Low){   //8bitデータを16bitに直す
  int Data = 0;
  Data = ((High << 8) | Low);
  return -(Data & 0b1000000000000000) | (Data & 0b0111111111111111);
}

/*
void printCom(float daX, float daY, float daZ){   //コンパス表示
  Serial.print("ComX,");
  Serial.print(daX);
  Serial.print(",");
  Serial.print("ComY,");
  Serial.print(daY);
  Serial.print(",");
  Serial.print("ComZ,");
  Serial.print(daZ);
  Serial.print(",");
}*/

float Compass(float x, float y){
  float deg = ((atan2(y, x))*180.0/pi);
  return deg;
}

String Compass(float deg){
  String drc;
  if(deg >= -11.25 && deg < 11.25){
    drc = "E";
  }
  else if(deg >= 11.25 && deg < 33.75){
    drc = "ENE";
  }
  else if(deg >= 33.75 && deg < 56.25){
    drc = "NE";
  }
  else if(deg >= 56.25 && deg < 78.75){
    drc = "NNE";
  }
  else if(deg >= 78.75 && deg < 101.25){
    drc = "N";
  }
  else if(deg >= 101.25 && deg < 123.75){
    drc = "NNW";
  }
  else if(deg >= 123.75 && deg < 146.25){
    drc = "NW";
  }
  else if(deg >= 146.25 && deg < 168.75){
    drc = "WNW";
  }
  else if(deg >= 168.75 && deg <= 180 || deg <= -168.75 && deg >= -180){
    drc = "W";
  }
  else if(deg >= -168.75 && deg < -146.25){
    drc = "WSW";
  }
  else if(deg >= -146.25 && deg < -123.75){
    drc = "SW";
  }
  else if(deg >= -123.75 && deg < -101.25){
    drc = "SSW";
  }
  else if(deg >= -101.25 && deg < -78.75){
    drc = "S";
  }
  else if(deg >= -78.75 && deg < -56.25){
    drc = "SSE";
  }
  else if(deg >= -56.25 && deg < -33.75){
    drc = "SE";
  }
  else if(deg >= -33.75 && deg < -11.25){
    drc = "ESE";
  }
  return drc;
}

void setup() {
  setI2C();
  
  SPI.begin();
  SPI.setClockDivider(SPI_CLOCK_DIV16);
  SPI.setBitOrder(MSBFIRST);
  SPI.setDataMode(SPI_MODE0);
  pinMode(8, OUTPUT);
  writeSPI(0x6B, 0x00);
  writeSPI(0x37, 0x02);

  //StaticJsonBuffer<200> jsonBuffer;
  
  Serial.begin(115200);
}

void loop() {
  AcXH = readSPI(0x3B);
  AcXL = readSPI(0x3C);
  AcYH = readSPI(0x3D);
  AcYL = readSPI(0x3E);
  AcZH = readSPI(0x3F);
  AcZL = readSPI(0x40);

  AccX = setSPI(AcXH, AcXL);
  AccY = setSPI(AcYH, AcYL);
  AccZ = setSPI(AcZH, AcZL);

  float Gravty = gAcc(AccX, AccY);

  //setI2C();
  //delay(100);
  //Wire.begin(0x69);

  readI2C(slaveMagnet, 0x03, 7);
  while(Wire.available()){
    CoXL = Wire.read();
    CoXH = Wire.read();
    CoYL = Wire.read();
    CoYH = Wire.read();
    CoZL = Wire.read();
    CoZH = Wire.read();
    ST2 = Wire.read();
  }
  
  ComX = (float)(setData(CoXH, CoXL) + 22) / 200;
  ComY = (float)(setData(CoYH, CoYL) - 200) / 200;
  ComZ = (float)(setData(CoZH, CoZL) + 200) / 200;
  
  float Com = Compass(ComX, ComY);
  String ComData = Compass(Com);

  Serial.print("{\"commpassRaw\":");
  Serial.print(Com);
  //Serial.print(", \"commpass\":");
  //Serial.print(ComData);
  Serial.print(", \"Grav\":");
  Serial.print(Gravty);
  Serial.print("}");

  Serial.print("\n");
  
  delay(200);
}
