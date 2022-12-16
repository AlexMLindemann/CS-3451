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
vec4 diffuse_color = vec4 (0.0, 1.0, 1.0, 1.0);

void main() { 
	float diffuse = clamp(dot (vertNormal, vertLightDir),0.0,1.0);
	gl_FragColor = vec4(diffuse * diffuse_color.rgb, 1.0);
	
	//your code here
	float radius = 5.0;
  ivec2 textureSize2d = textureSize(my_texture, 0);
  float texelSize;
  // grab the color values from the texture and the mask
  vec4 diffuse_color = texture2D(my_texture, vertTexCoord.xy); 
  vec4 mask_color = texture2D(my_mask, vertTexCoord.xy);
 
  vec4 texture_col1;
  vec4 texture_col2;
  float x = vertTexCoord.x;
  float y = vertTexCoord.y;
  textureSize = float(textureSize2d.x);
  texelSize = 1.0 / textureSize;
  float texelX = 1.0/textureSize(my_texture, 0).x;
  float texelY = 1.0/textureSize(my_texture, 0).y;
  //loop thru neighboring texels
  for (float i = (-radius-blur_radius); i < blur_radius; i++) {
    for (float j = (-radius-blur_radius); j < blur_radius; j++) {
      vec4 ij_coord = texture2D(my_texture, vertTexCoord.xy + vec2(x*texelX, y*texelY));
      blur_col += ij_coord;

      // vec2 i_coord = vec2(x, i * texelSize);
      // vec2 j_coord = vec2(y, i * texelSize);
      // texture_col1 = texture2D(my_mask, i_coord);
      // texture_col2 = texture2D(my_mask, j_coord);
      // blur_col += texture_col1;
      // blur_col += texture_col2;
      // vec4 blur_col = vec4; 
    }
    blur_col /= blur_radius*blur_radius;
    diffuse_color = blur_col;
  } 

  //calc mask intensity
  if (mask_color.rgb[0] < 0.1) {
    blur_radius = 6;
  } else if (0.1 <= mask_color.rgb[0] && mask_color.rgb[0] <= 0.5) {
    blur_radius = 3; 
  } else {
    blur_radius = 0;
  }

     // half sheep, half mask
  // if (vertTexCoord.x > 0.5)
  //   diffuse_color = mask_color;
  
//change diffuse_color to blur color
  // simple diffuse shading model
  //float diffuse = clamp(dot (vertNormal, vertLightDir),0.0,1.0);
  // gl_FragColor = vec4(diffuse * diffuse_color.rgb, 1.0);
}
