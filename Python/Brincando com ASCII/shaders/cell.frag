#version 330 core
in vec2 TexCoord;
out vec4 FragColor;

uniform sampler2D tex;

void main() {
    float value = texture(tex, TexCoord).r; // pega intensidade
    FragColor = vec4(value, value, value, 1.0); // escala de cinza
}
