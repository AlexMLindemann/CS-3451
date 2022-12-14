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


void main() { 
  gl_FragColor.a = 1;

  if (vertTexCoord.s > 0.4 && vertTexCoord.s < 0.6)
    gl_FragColor.a = 0;
  // gl_FragColor = vec4(0.2, 0.4, 1.0, vertTexCoord.s);
}

