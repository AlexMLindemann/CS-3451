// Fragment shader
// The fragment shader is run once for every pixel
// It can change the color and transparency of the fragment.

#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

#define PROCESSING_TEXLIGHT_SHADER

// Set in Processing
uniform sampler2D my_texture;
uniform sampler2D my_mask;
uniform float blur_flag;

// These values come from the vertex shader
varying vec4 vertColor;
varying vec3 vertNormal;
varying vec3 vertLightDir;
varying vec4 vertTexCoord;
//maintain sum of blur color
//divide each component of color by # of texels sampled (blur radius * blur radius)
float textureSize;
vec4 blur_col = vec4(0.0, 0.0, 0.0, 0.0);
float blur_radius = 3.0;

void main() { 
  ivec2 textureSize2d = textureSize(my_texture, 0);
  float texelSize;
  for (int i = 0; i < blur_radius; i++) {
    for (int j = 0; j < blur_radius; j++) {
      ivec2 textureSize2d = textureSize(my_texture, 0);
      textureSize = float(textureSize2d.x);
      texelSize = 1.0 / textureSize;
      float x_size = float(textureSize2d.x + i * texelSize);
      float y_size = float(textureSize2d.y + j * texelSize);
      

    }
    blur_col /= blur_radius*blur_radius;
  } 
  // grab the color values from the texture and the mask
  vec4 diffuse_color = texture2D(my_texture, vertTexCoord.xy);
  vec4 mask_color = texture2D(my_mask, vertTexCoord.xy);

  //loop thru neighboring texels

     // half sheep, half mask
  if (vertTexCoord.x > 0.5)
    diffuse_color = mask_color;
  
//change diffuse_color to blur color
  // simple diffuse shading model
  float diffuse = clamp(dot (vertNormal, vertLightDir),0.0,1.0);

  gl_FragColor = vec4(diffuse * diffuse_color.rgb, 1.0);
}
