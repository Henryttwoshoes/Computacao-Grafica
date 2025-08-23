#version 330 core
in vec2 TexCoord;
out vec4 FragColor;

uniform sampler2D tex;

void main() {
    float value = texture(tex, TexCoord).r; // pega intensidade
    FragColor = vec4(0.0, value, 0.0, 1.0); // verde com intensidade do caractere
}
