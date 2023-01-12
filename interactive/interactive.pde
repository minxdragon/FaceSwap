import processing.video.*;
import java.awt.Rectangle;
import java.util.LinkedHashMap;
import java.io.File;

//import controlP5.*;
import g4p_controls.*;
import gab.opencv.*;
import processing.net.*; 
import codeanticode.syphon.*;
import videoExport.*;

Client myClient;
String inString;

PGraphics[] scenes = new PGraphics[10];
GToggleGroup sceneGUI;
GButton b0,b1,b2,b3,b4a,b4b,b5,b6,b7,b8a,b8b,b9;
GButton tog1;
GButton tog2;

PGraphics userImage;
PImage userPhoto;
OpenCV opencv;

PGraphics sCanvas;
SyphonClient client;

String responseKeywordsString = "";

//setBroadcast(false) to prevent a controller from triggering an event
int currentScene = 0;

VideoExport ve;
PGraphics veCanvas;
String userID;
Movie userVideo;

PGraphics videoLayer;
PGraphics progressBarCanvas;


void setup(){
  size(608,1080,P3D);
  createCanvases();
  frameRate(30);
  
  client = new SyphonClient(this);
  
  sceneGUI = new GToggleGroup();
  defineGUI();
  
  sceneFourSetup();
  
  userImage = createGraphics(608, 1080);
  userPhoto = createImage(608, 1080,RGB);
  
  myClient = new Client(this, "127.0.0.1", 5008); 
  
  
  veCanvas = createGraphics(width, height,P3D);
  //ve = new VideoExport(this, "/data/gallery/movie.mp4", veCanvas);
  ve = new VideoExport(this);
  ve.setGraphics(veCanvas);
  
  videoLayer = createGraphics(width, height,P3D);
  progressBarCanvas = createGraphics(width, height,P3D);
  
  background(0,0,0);
}

void draw(){
  //background(0);
  listenServerClient();
  renderScene(currentScene);
  image(scenes[currentScene], 0, 0); 
}

void listenServerClient(){
  if (myClient.available() > 0) {    
    inString = myClient.readString(); 
    println(inString);
    
    String[] responseList = split(inString, ',');
    switch(responseList[0]) {
      case "cameraNoMaskReady": 
        println("Recognised response.");
        break;
      case "analysisComplete": 
        currentScene = 3;
        responseKeywordsString = responseList[1];
        //responseKeywordsString musical&level-headed&visionary&risk-taker&creative
        returnedKeywords = split(responseKeywordsString, '&');
        b3.setVisible(true);
        break;
      case "cameraMaskReady": 
        currentScene = 6;
        b6.setVisible(true);
        break;
      default:             
        println(responseList[0] + " is not a recognised response");
        break;
    }
  }
}

void renderScene(int currentSceneNumber){
  switch(currentSceneNumber) {
    case 0: 
      sceneZero(scenes[0]);
      break;
    case 1: 
      sceneOne(scenes[1]);
      break;
    case 2: 
      sceneTwo(scenes[2]);
      break;
    case 3: 
      sceneThree(scenes[3]);
      break;
    case 4: 
      sceneFour(scenes[4]);
      break;
    case 5: 
      sceneFive(scenes[5]);
      break;
    case 6: 
      sceneSix(scenes[6]);
      break;
    case 7: 
      sceneSeven(scenes[7]);
      break;
    case 8: 
      sceneEight(scenes[8]);
      break;
    case 9: 
      sceneNine(scenes[9]);
      break;
    }
}

void createCanvases(){
  for(int i = 0; i < 10; i++){
    scenes[i] = createGraphics(width, height, P3D);
  }
}

void defineGUI(){
  defineGUIZero(); 
  defineGUIOne();
  defineGUITwo();
  defineGUIThree();
  defineGUIFour();
  defineGUIFive();
  defineGUISix();
  defineGUISeven();
  defineGUIEight();
  defineGUINine();
}