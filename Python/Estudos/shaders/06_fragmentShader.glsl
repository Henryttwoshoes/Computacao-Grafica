#version 330 core

out vec4 fragColor;
in vec3 f_color;

void main(){
    float value = gl_FragCoord.y / 500.0;
    fragColor = vec4(f_color, 1.0);
}