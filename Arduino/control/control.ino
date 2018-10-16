/* 10/6 latest */
#include <Stepper.h>

int pin1 = 2;
int pin2 = 3;
int pin3 = 4;
int pin4 = 5;
int pin5 = 6;
int pin6 = 7;

int Time = 0, NoT = 0;

#define MOTOR_1 8   // blue
#define MOTOR_2 9   // pink
#define MOTOR_3 10   // yellow
#define MOTOR_4 11  // orange

#define del 300

#define MOTOR_STEPS 2048 //1回転

//モータ軸が60度回転すると主軸が1度回転する(ウォームギア)
//主軸が1度、5度、10度 回転するモードを作る

//主軸(度)>モータ軸(度)>step数
//1度＞60＞341.33...
//5度＞300＞1706.6...
//10度＞600＞3413.3...

// ライブラリが想定している配線が異なるので2番、3番を入れ替える
Stepper myStepper(MOTOR_STEPS, MOTOR_1, MOTOR_3, MOTOR_2, MOTOR_4);

// モーターへの電流を止める
void stopMotor() {
  digitalWrite(MOTOR_1, LOW);
  digitalWrite(MOTOR_2, LOW);
  digitalWrite(MOTOR_3, LOW);
  digitalWrite(MOTOR_4, LOW);
}

//モーターへ電流を流す
void startMotor() {
  digitalWrite(MOTOR_1, HIGH);
  digitalWrite(MOTOR_2, HIGH);
  digitalWrite(MOTOR_3, HIGH);
  digitalWrite(MOTOR_4, HIGH);
}

void setup() {
  pinMode(pin1, OUTPUT);
  digitalWrite(pin1, HIGH);
  pinMode(pin2, OUTPUT);
  digitalWrite(pin2, HIGH);
  pinMode(pin3, OUTPUT);
  digitalWrite(pin3, HIGH);
  pinMode(pin4, OUTPUT);
  digitalWrite(pin4, HIGH);
  pinMode(pin5, OUTPUT);
  digitalWrite(pin5, HIGH);
  pinMode(pin6, OUTPUT);
  digitalWrite(pin6, HIGH);

  pinMode(MOTOR_1, OUTPUT);
  pinMode(MOTOR_2, OUTPUT);
  pinMode(MOTOR_3, OUTPUT);
  pinMode(MOTOR_4, OUTPUT);
  stopMotor();

  myStepper.setSpeed(10);
  
  Serial.begin(115200);
}

void loop() {
  startMotor();
  
  char var = Serial.read();

  switch(var){    //スイッチングの分岐:角度    >>  ちょっとおおきめ
    case '1':          //(速さ:1, 回す時間:1000ms)*1 > 0.02度回す
      digitalWrite(pin1, LOW);
      digitalWrite(pin2, LOW);
      delay(del);
      digitalWrite(pin1, HIGH);
      digitalWrite(pin2, HIGH);
      Time = 800;
      NoT = 250;
      break;
      //2500ms*100=8deg
      //3000ms*50=5deg > 3000*5=0.5 > 3000*1=0.1 > 300*1=0.01deg ?
      //1000ms*180=5deg > 1000*36=1deg
      //800ms*250=5deg > 800*50=1deg > 800*5=0.1deg > 800*1=0.02deg

    case '2':          //(速さ:2, 回す時間:2500ms)*1 > 0.1度回す
      digitalWrite(pin1, LOW);
      digitalWrite(pin4, LOW);
      delay(del);
      digitalWrite(pin1, HIGH);
      digitalWrite(pin4, HIGH);
      Time = 2500;
      NoT = 1;
      break;

    case '3':          //(速さ:3, 回す時間:3500ms)*1 > 0.5度回す
      digitalWrite(pin1, LOW);
      digitalWrite(pin6, LOW);
      delay(del);
      digitalWrite(pin1, HIGH);
      digitalWrite(pin6, HIGH);
      Time = 3500;
      NoT = 1;
      break;

    case '4':          //(速さ:4, 回す時間:1500ms)*1 > 1度回す
      digitalWrite(pin5, LOW);
      digitalWrite(pin6, LOW);
      delay(del);
      digitalWrite(pin5, HIGH);
      digitalWrite(pin6, HIGH);
      Time = 1500;
      NoT = 1;
      break;

    case '5':          //(速さ:5, 回す時間:590ms)*1 > 5度回す
      digitalWrite(pin5, LOW);
      digitalWrite(pin2, LOW);
      delay(del);
      digitalWrite(pin5, HIGH);
      digitalWrite(pin2, HIGH);
      Time = 590;
      NoT = 1;
      break;

    case '6':          //(速さ:5, 回す時間:590ms)*3 > 15度回す
      digitalWrite(pin5, LOW);
      digitalWrite(pin2, LOW);
      delay(del);
      digitalWrite(pin5, HIGH);
      digitalWrite(pin2, HIGH);
      Time = 590;
      NoT = 3;
      break;
  }

  switch(var){    //スイッチングの分岐:上下左右とモータ
    case 'U':
      for(int i=0; i<NoT; i++){
        digitalWrite(pin3, LOW);
        digitalWrite(pin4, LOW);
        delay(Time);
        digitalWrite(pin3, HIGH);
        digitalWrite(pin4, HIGH);
        delay(del);
      }
      break;

    case 'D':
      for(int i=0; i<NoT; i++){
        digitalWrite(pin5, LOW);
        digitalWrite(pin4, LOW);
        delay(Time);
        digitalWrite(pin5, HIGH);
        digitalWrite(pin4, HIGH);
        delay(del);
      }
      break;

    case 'L':
      for(int i=0; i<NoT; i++){
        digitalWrite(pin2, LOW);
        digitalWrite(pin3, LOW);
        delay(Time);
        digitalWrite(pin2, HIGH);
        digitalWrite(pin3, HIGH);
        delay(del);
      }
      break;

    case 'R':
      for(int i=0; i<NoT; i++){
        digitalWrite(pin3, LOW);
        digitalWrite(pin6, LOW);
        delay(Time);
        digitalWrite(pin3, HIGH);
        digitalWrite(pin6, HIGH);
        delay(del);
      }
      break;

    case 'a':   // p1を送信すると主軸が1度正回転
      myStepper.step(341);
      break;

    case 'b':   // p5を送信すると主軸が5度正回転
      myStepper.step(1707);
      break;

    case 'c':   // p10を送信すると主軸が10度正回転
      myStepper.step(3413);
      break;

    case 'd':   // m1を送信すると主軸が1度反回転
      myStepper.step(-341);
      break;

    case 'e':   // m5を送信すると主軸が5度反回転
      myStepper.step(-1707);
      break;

    case 'f':   // m10を送信すると主軸が10度反回転
      myStepper.step(-3413);
      break;
  }

  delay(100);
  
  stopMotor();
}
