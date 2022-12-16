
#define PROCESSING_LIGHT_SHADER

// Set automatically by Processing
uniform mat4 transform;
uniform mat3 normalMatrix;
uniform vec3 lightNormal;
uniform mat4 texMatrix;


// Come from the geometry/material of the object
attribute vec4 vertex;
attribute vec4 color;
attribute vec3 normal;
attribute vec2 texCoord;

// These values will be sent to the fragment shader
varying vec4 vertColor;
varying vec3 vertNormal;
varying vec3 vertLightDir;
varying vec4 vertTexCoord;
varying vec4 square_center;

void main() {
  vertColor = color;
  
  vertNormal = normalize(normalMatrix * normal);
  
  vec4 vert = vertex;

  gl_Position = transform * vert; 
  vertLightDir = normalize(-lightNormal);
  vertTexCoord = texMatrix * vec4(texCoord, 1.0, 1.0);
  square_center = vec4(0.4, 0.4, 0.6, 0.6);

}
