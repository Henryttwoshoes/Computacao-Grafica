import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders as gls
import numpy as np # usado para converter a lista de vértices em um array de itens com 4 bytes(32 bits)
import ctypes # adiciona a tipagem da linguagem C á linguage Python


vertices = [
    [-0.8, -0.8],
    [0.0, -0.8],
    [-0.4 , 0.0],
    [0.0 , -0.8],
    [0.4 , 0.0],
    [-0.4 , 0.0],
    [0.4 , 0.0],
    [0.0 , 0.8],
]

qtdVertices = len(vertices)
vaoID = 0
shaderID = 0


# Função para configurações iniciais da minha aplicação.
def init():
    global vertices, vaoID, shaderID
    glClearColor(1,1,1,1)
    # Converte os valores da lista dos vértices para tipo float de 32 bits
    vertices = np.array(vertices, np.dtype(np.float32)) # 32 bits = 4 bytes

    vaoID = glGenVertexArrays(1) # criando o VAO
    glBindVertexArray(vaoID) # tornando VAO ativo


    # Criar o VBO
    vboID = glGenBuffers(1)
    # Tornar o VBO ativo
    glBindBuffer(GL_ARRAY_BUFFER, vboID)
    # Enviar os dados para esse VBO
    glBufferData(GL_ARRAY_BUFFER, # tipo de buffer
                 vertices.nbytes, #tamanho do buffer
                 vertices, # conteúdo
                 GL_STATIC_DRAW) # uso do buffer
    glVertexAttribPointer(0, # código do atributo(posição)
                          2, # qtd de valores do atributo
                          GL_FLOAT, # tipo dos valores do atributo
                          GL_FALSE, # deseja normalizar os valores
                          2*4, # quantidade de bytes entre um atributo e o próximo
                          ctypes.c_void_p(0)) # ponteiro pra void
    glEnableVertexAttribArray(0)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    # Criar shader

    # código fonte dos shaders
    # ler o arquivo vertex shader
    with open('shaders/05_vertexShader.glsl', 'r') as file:
        vsSource = file.read()

    # ler o arquivo fragment shader
    with open('shaders/05_fragmentShader.glsl', 'r') as file:
        fsSource = file.read()

    vsID = gls.compileShader(vsSource, GL_VERTEX_SHADER)
    fsID = gls.compileShader(fsSource, GL_FRAGMENT_SHADER)
    shaderID = gls.compileProgram(vsID, fsID)

    '''vsID = glCreateShader(GL_VERTEX_SHADER) # criar o objeto vertex shader
    glShaderSource(vsID, vsSource) # enviar o código-fonte vertex shader para esse objeto
    glCompileShader(vsID) # compilar o vertex shader
    if not glGetShaderiv(vsID, GL_COMPILE_STATUS): # verificar por erros no vertex shader
        info = glGetShaderInfoLog(vsID)
        print("Erro de compilação no vertex shader.")
        print(info)'''


    '''fsID = glCreateShader(GL_FRAGMENT_SHADER) # criar o objeto fragment shader
    glShaderSource(fsID, fsSource) # enviar o código-fonte fragment shader para esse objeto
    glCompileShader(fsID) # compilar o fragment shader
    if not glGetShaderiv(fsID, GL_COMPILE_STATUS): # verificar por erros no fragment shader
        info = glGetShaderInfoLog(fsID)
        print("Erro de compilação no vertex shader.")
        print(info)'''
    
    shaderID = glCreateProgram() # criar um shader program
    glAttachShader(shaderID, vsID)
    glAttachShader(shaderID, fsID)
    glLinkProgram(shaderID)

# Função para atualizar a renderização da cena.
def render():
    glClear(GL_COLOR_BUFFER_BIT)


    glUseProgram(shaderID)
    glBindVertexArray(vaoID)
    glDrawArrays(GL_TRIANGLES,
                 0,
                 qtdVertices)
    glBindVertexArray(0)
    glUseProgram(0)

# Função principal
def main():
    glfw.init() # Inicializando a API GLFW
    window = glfw.create_window(500,500,'03 - Primitvas',None,None) # Criando a janela
    glfw.make_context_current(window) # Criando o contexto OpenGL na janela
    init() # Chama a função de configurações iniciais da aplicação.
    while not glfw.window_should_close(window): # Enquanto a janela não é fechada
        glfw.poll_events() # Tratamento de eventos
        render() # chama a função render para atualizar os buffers na aplicação
        glfw.swap_buffers(window) # Troca de frame buffers
    glfw.terminate() # Finalizando a API GLFW

if __name__ == '__main__':
    main()