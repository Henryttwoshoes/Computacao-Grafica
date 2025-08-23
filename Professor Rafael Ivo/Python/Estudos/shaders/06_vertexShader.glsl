#version 330 core

// Shader são programas que rodam em PARALELO. Não é necessário inicilizar as variáveis(dá erro).

// Declarações de entrada e saída
layout(location = 0) in vec2 a_pos;


void main(){
    gl_Position = vec4(a_pos, 0.0,1.0);


}