// Fragment shader

#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

#define PROCESSING_LIGHT_SHADER
#define PI 3.1415926538
// These values come from the vertex shader
varying vec4 vertColor;
varying vec3 vertNormal;
varying vec3 vertLightDir;
varying vec4 vertTexCoord;
// varying vec4 square_center;

void main() { 
  gl_FragColor = vec4(0.2, 0.4, 1.0, 0.7);
  //gl_FragColor.a = 1.0;
  float x = vertTexCoord.x;
  float y = vertTexCoord.y;
  // vec2 square_center = vec2(0.5, 0.1);
  float square_X = 0.5;
  float square_Y = 0.1;
  vec2 square_center = vec2(0.5, 0.1);
  float distance = 0.06;
  float off_X = square_X;
  float off_Y = square_X;
  float temp_X = vertTexCoord.x;
  x = x * cos(PI / 4) - y * sin(PI / 4) + 0.5;
  y = temp_X * sin(PI / 4) + y * cos(PI/4) - 0.2;
??  float temp_coord = vertTexCoord.xy - square_center.xy;

  for (int i = 0; i < 5; i++) {
    //vertical square_center
    if (abs(vertTexCoord.x - square_X) < distance && abs(vertTexCoord.y - square_Y) < distance) {
      gl_FragColor.a = 0.0;
    }

    int num_squares = 0;
    if (i == 1 || i == 3) {
      num_squares = 1;
    } else if (i == 2) { //2 on each side
      num_squares = 2;
    }

    if (abs(vertTexCoord.y - square_Y) < distance) {
      for (int p = 0; p < num_squares; p++) {
        off_X = off_X - 0.2;
        off_Y = off_Y + 0.2;
        float delta_X = abs(x - off_X);
        float delta_Y = abs(x - off_Y); 
        if (delta_X < distance || delta_Y < distance) {
          gl_FragColor.a = 0.0;
        }
      }
    }
    
    
    square_Y += 0.2;
  }
  //gl_FragColor = vec4(0.2, 0.4, 1.0, alpha);
}

