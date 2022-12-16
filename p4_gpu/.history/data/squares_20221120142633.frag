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
varying vec4 square_center;

void main() { 
  //gl_FragColor.a = 1;
  gl_FragColor = vec4(0.2, 0.4, 1.0, 0.7);
  square_center = vec2(0.5, 0.5);
  in int distance = 0.25;

  if (vertTexCoord.x > square_center.x && vertTexCoord.x < (square_center.x + distance)) 
    gl_FragColor.a = 0;
  if (vertTexCoord.y > square_center.y && vertTexCoord.y < (square_center.y + distance)) 
    // if (vertTexCoord.y > 0.4 && vertTexCoord.y < 0.6)
      gl_FragColor.a = 0;
  }//gl_FragColor = vec4(0.2, 0.4, 1.0, vertTexCoord.s);
}

