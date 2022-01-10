
// composed by Titus Kemboi Cheserem
// Date: 10 Dec 2021 23:56

int myrelay = 8; 
char userInput;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  delay(200);
  // declare pin 8 to be an output:
  pinMode(myrelay, OUTPUT);
  //Initialize the relay to be in the discharge state
//  digitalWrite(myrelay, LOW);

}

void loop() {
  // put your main code here, to run repeatedly:
  //++++++++++++++++++++++++++++++++ new update +++++++++++++++++++++
if(Serial.available() > 0) //if serial input is not empty process the user input
  {
    userInput = Serial.read();
    // capture the charge_now == (charge_full-200) && battery_is_present && status==Charging)
    // to make our ino file a bit simple we are are going to map them to decimal values using a key_value_pair
    
    if(userInput == 'c') //turn on relay for charging
    {
         
//       myservo.write(90);
      
        digitalWrite(myrelay, HIGH);
        Serial.println("Turning Relay ON: Battery is Charging ): ");
        delay(500);
        
        
        
    }
    else if (userInput=='d') //turn off relay for charging
    {
     
        Serial.println("Turning Relay Off: Battery is Discharging (:");
        delay(500);
        digitalWrite(myrelay, LOW);
     
     
      
      
    }
    else{ // Incorrect user input command 
//      Serial.println("Doing Nothing yet");
      
    }
  }
  else{ // no user input therefore do nothing
    
//    Serial.println("Nothing to be input");
    
  }
  //++++++++++++++++++++++++++++++== end update +++++++++++++++++++++++++
  
 

}
