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
	float cx, cy, z_real, z_img, z_new;
	vec2 z = vec2(0.0, 0.0);
	vec2 comp_Sine = vec2(0.0, 0.0);
	cx = vertTexCoord.x;
	cy = vertTexCoord.y;
	z = vec2(vertTexCoord.x * 6.28 - 3.14, vertTexCoord.y * 6.28 - 3.14);
	z_img = z_real = z_new;
	bool flag = false;
	for(int i = 0; i < 20; i++)	{
		z_real = z.x * cx;
		//z_img = z.y * cy;
		z_img = z_new;
		z_new = sin(z_real) * cy;
		comp_Sine = vec2(sin(z_real) * cosh(z_img), cos(z_real) * sinh(z_img));
		z = vec2(cx*comp_Sine.x - cy *comp_Sine.y, cx*comp_Sine.y - cy *comp_Sine.x);
		
		if(((z_real*z_real)+(z_img*z_img)) > 2500)	{
			flag = true;
			break;
		}
	}
	if(flag == true) {
		gl_FragColor = vec4(diffuse * diffuse_color.rgb, 1.0);
	}
	else	{
		gl_FragColor = vec4(diffuse * diffuse_color2.rgb, 1.0);
	}


	// z = zi = z_real = newZi = 0;

	// int i;
	// bool flag = false;
	// for(i = 0; i < 20; i++)	{
	// 	z = z_real;
	// 	zi = newZi;
	// 	comp_Sine = vec2(sin(z*cx) * cosh(zi), cos(z_real) * sinh(zi));
	// 	z_real = (z * z) - (zi * zi) + cx;
    // z_real = (cx * comp_Sine.x) - (cy * comp_Sine.y);
	// 	newZi = 2 * z * zi + cy;
		
	// 	if(((z_real*z_real)+(newZi*newZi)) > 4)	{
	// 		flag = true;
	// 		break;
	// 	}
	// }
	
	// if(flag == true)	{
	// 	gl_FragColor = vec4(diffuse * diffuse_color.rgb, 1.0);
	// }
	// else	{
	// 	gl_FragColor = vec4(diffuse * diffuse_color2.rgb, 1.0);
	// }
}
