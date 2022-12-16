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
  gl_FragColor = vec4(0.2, 0.4, 1.0, 0.7);
  gl_FragColor.a = 1.0;
  float x = vertTexCoord.x;
  float y = vertTexCoord.y;
  vec2 square_center = vec2(0.5, 0.1);
  float centerX = 0.5;
  float centerY = 0.1;
  float distance = 0.05;
  float count = 0.0;
  float x1 = centerX;
  float xr = centerX;

  for (int i = 0; i < 5; i++) {
    float dx = abs(vertTexCoord.x - centerX);
    float dy = abs(vertTexCoord.y - centerY);

    //vertical square_center
    if (dx < distance && dy < distance) {
      gl_FragColor.a = 0.0;
    }

    int num_squares = 0;
    if (i == 1 || i == 3) {
      num_squares = 1;
    } else if (i == 2) {
      num_squares = 2;
    }

    if (dy < distance) {
      for (int p = 0; p < num_squares; p++) {
        x1 = x1 - 0.2;
        xr = xr + 0.2;
        float dx1 = abs(x - x1);
        float dxr = abs(x - xr); 
        if (dx1 < distance || dxr < distance) {
          gl_FragColor.a = 0.0;
        }
      }
    }
    
    
    centerY += 0.2;
  }
  //gl_FragColor = vec4(0.2, 0.4, 1.0, alpha);
}

