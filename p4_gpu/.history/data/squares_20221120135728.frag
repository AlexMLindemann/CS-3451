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
  square_center = vec4(0.4, 0.4, 0.6, 0.6);
  if (vertTexCoord.x > 0.4 && vertTexCoord.x < 0.6) 
    if (vertTexCoord.y > 0.4 && vertTexCoord.y < 0.6)
      gl_FragColor.a = 0;
  //gl_FragColor = vec4(0.2, 0.4, 1.0, vertTexCoord.s);
}

