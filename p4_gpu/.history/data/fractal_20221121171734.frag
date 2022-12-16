// Fragment shader

#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

#define PROCESSING_LIGHT_SHADER

uniform float cx;
uniform float cy;

// These values come from the vertex shader
varying vec4 vertColor;
varying vec3 vertNormal;
varying vec3 vertLightDir;
varying vec4 vertTexCoord;

void main() { 

  vec4 diffuse_color = vec4 (1.0, 0.0, 0.0, 1.0);
  vec4 diffuse_color2 = vec4 (1.0, 1.0, 1.0, 1.0);
  float diffuse = clamp(dot (vertNormal, vertLightDir),0.0,1.0);
  gl_FragColor = vec4(diffuse * diffuse_color.rgb, 1.0);
  float cx, cy, z, zi, newZ, newZi;
	
	cx = vertTexCoord.x * 3.0 - 2.1;
	cy = vertTexCoord.y * 3.0 - 1.5;
	
	z = zi = newZ = newZi = 0;
	
	int i;
	bool flag = false;
	for(i = 0; i < 20; i++)	{
		z = newZ;
		zi = newZi;
		
		newZ = (z * z) - (zi * zi) + cx;
		newZi = 2 * z * zi + cy;
		
		if(((newZ*newZ)+(newZi*newZi)) > 4)	{
			flag = true;
			break;
		}
	}
	
	if(flag == true)	{
		gl_FragColor = vec4(diffuse * diffuse_color.rgb, 1.0);
	}
	else	{
		gl_FragColor = vec4(diffuse * diffuse_color2.rgb, 1.0);
	}
}
