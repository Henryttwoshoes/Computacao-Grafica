import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders as gls
import numpy as np # usado para converter a lista de vértices em um array de itens com 4 bytes(32 bits)
import ctypes # adiciona a tipagem da linguagem C á linguage Python


'''vertices = [
    [-0.8, -0.8, 1,0,0],
    [0.0, -0.8, 1,1,0],
    [-0.4, 0.0, 1,0,1],
    [0.0, -0.8, 1,1,0],
    [0.8, -0.8, 0,1,0],
    [0.4, 0.0, 0,1,1],
    [-0.4, 0.0, 1,0,1],
    [0.4, 0.0, 0,1,1],
    [0.0, 0.8, 0,0,1],
    
]'''

vertices = [
    [-0.8, -0.8, 1,0,0], # v0
    [0.0, -0.8, 1,0,0], # v1 - vermelho
    [0.0, -0.8, 0,1,0], # v1 - verde
    [0.0, -0.8, 1,1,0], # v1 - amarelo
    [0.8, -0.8, 0,1,0], # v2
    [-0.4, 0.0, 1,0,0], # v3 - vermelho
    [-0.4, 0.0, 1,0,1], # v3 - magenta
    [0.4, 0.0, 0,1,0], # v4 - verde
    [0.4, 0.0, 0,1,1], # v4 - ciano
    [0.0, 0.8, 0,0,1], # v5
    
    
]
faces = [
    [0,1,5], # face inferior esquerda
    [2,4,7], # face inferior direita
    [6,8,9], # face superior
    [3,8,6] # face do meio
]

qtdVertices = len(vertices)
qtdFaces = len(faces)
vaoID = 0
shaderID = 0


# Função para configurações iniciais da minha aplicação.
def init():
    global vertices, vaoID, faces, shaderID
    glClearColor(1,1,1,1)
    # Converte os valores da lista dos vértices para tipo float de 32 bits
    vertices = np.array(vertices, dtype=np.float32) # 32 bits = 4 bytes

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
                          5*4, # quantidade de bytes entre um atributo e o próximo
                          ctypes.c_void_p(0)) # ponteiro pra void
    
    glVertexAttribPointer(1, # código do atributo(cor)
                          3, # qtd de valores do atributo
                          GL_FLOAT, # tipo dos valores do atributo
                          GL_FALSE, # deseja normalizar os valores
                          5*4, # quantidade de bytes entre um atributo e o próximo
                          ctypes.c_void_p(2*4)) # ponteiro pra void
    
    glEnableVertexAttribArray(0) # habilita o atributo posição (location = 0)
    glEnableVertexAttribArray(1) # habilita o atributo cor (location = 1)

    # criando EBO - Element Array Buffer
    faces = np.array(faces, dtype=np.uint32)
    eboID = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, eboID)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, faces.nbytes, faces, GL_STATIC_DRAW)


    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    # Criar shader

    # código fonte dos shaders
    # ler o arquivo vertex shader
    with open('C:/Users/Usuário/Desktop/College Things/Repositórios/Computacao-Grafica/Professor Rafael Ivo/Python/Estudos/shaders/06_vertexShader.glsl', 'r') as file:
        vsSource = file.read()

    # ler o arquivo fragment shader
    with open('C:/Users/Usuário/Desktop/College Things/Repositórios/Computacao-Grafica/Professor Rafael Ivo/Python/Estudos/shaders/06_fragmentShader.glsl', 'r') as file:
        fsSource = file.read()

# Comandos abaixo são uma forma mais prática que a linguagem Python disponibiliza nesse módulo de OpenGL usado no programa. Esses códigos fazem os comandos em comentário logo abaixo dispensáveis para a implementação dos shaders.
    vsID = gls.compileShader(vsSource, GL_VERTEX_SHADER)
    fsID = gls.compileShader(fsSource, GL_FRAGMENT_SHADER)
    shaderID = gls.compileProgram(vsID, fsID)

# ----------------------------
# Comandos em comentário abaixo são OpenGL clássico e puro para implementar os shaders.
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
# --------------------------------------------------------
# Cria o programa dos shaders
    shaderID = glCreateProgram() # criar um shader program
    glAttachShader(shaderID, vsID) # linka o vertex shader
    glAttachShader(shaderID, fsID) # linka o fragment shader
    glLinkProgram(shaderID) # conecta eles em um só

# Função para atualizar a renderização da cena.
def render():
    glClear(GL_COLOR_BUFFER_BIT)


    glUseProgram(shaderID)
    glBindVertexArray(vaoID)
    #glDrawArrays(GL_TRIANGLES,
    #             0,
    #             qtdVertices)

    glDrawElements(GL_TRIANGLES, # primitiva
                   3 * qtdFaces, # qtd de faces
                   GL_UNSIGNED_INT, # tipo de dados dos índices (outros tipos = GL_UNSIGNED_BYTE / GL_UNSIGNED_SHORT)
                   None) # Offset = quantidade de bytes a partir do início. None é pra nenhum pulo a partir do início
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