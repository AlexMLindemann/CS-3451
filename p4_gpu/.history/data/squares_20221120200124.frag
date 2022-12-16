// Fragment shader

#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

#define PROCESSING_LIGHT_SHADER

// These values come from the vertex shader
varying vec4 vertColor;
varying vec3 vertNormal;
varying vec3 vertLightDir;
varying vec4 vertTexCoord;
// varying vec4 square_center;

void main() { 
  //gl_FragColor.a = 1;
  gl_FragColor = vec4(0.2, 0.4, 1.0, 0.7);
  vec2 square_center = vec2(0.5, 0.93);
  float distance = 0.05;
  int total = 9;

  for(int i = 0; i < total; ++i) 
  {
    if (vertTexCoord.x > (square_center.x - distance) && vertTexCoord.x < (square_center.x + distance)) {
      if (vertTexCoord.y > (square_center.y - distance) && vertTexCoord.y < (square_center.y + distance)) {
        gl_FragColor.a = 0;
      }
    }
    //Nested For
    //Check which row you're on
    int nums_squares;
    if (i == 2) {
      nums_squares = 2;
    } else if (i == 1 || i == 3) {
      nums_squares = 1;
    } else {
      nums_squares = 0;
    }
     
    //Have to place the x coordinate correctly to match the pattern
    if ((vertTexCoord.y - square_center.y) < distance) {
      for(int j = 0; j < nums_squares; ++j) {
        //right side
        square_center = vec2(0.8, 0.8);
        gl_FragColor.a = 0;
        if (vertTexCoord.x > (square_center.x - distance) && vertTexCoord.x < (square_center.x + distance)) {
          if (vertTexCoord.y > (0.2 - distance) && vertTexCoord.y < (0.2 + distance)) {
            square_center.x += 0.2;
            gl_FragColor.a = 0;
            // square_center = vec2(0.8, 0.8);
            // gl_FragColor.a = 0;
          }
        } 
        //left side
        if (vertTexCoord.x > (square_center.x - distance) && vertTexCoord.x < (square_center.x + distance)) {
          if (vertTexCoord.y > (square_center.y - distance) && vertTexCoord.y < (square_center.y + distance)) {
            square_center.x -= 0.2;
            gl_FragColor.a = 0;
          }
        }
        nums_squares -= 1;  
      }
    }
    square_center.y -= 0.2;    //decrement y
    --total;
  }//end for 
}

