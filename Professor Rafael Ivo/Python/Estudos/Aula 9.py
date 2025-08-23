import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders as gls
import numpy as np # usado para converter a lista de vértices em um array de itens com 4 bytes(32 bits)
import ctypes # adiciona a tipagem da linguagem C á linguage Python
from shader import *

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
    [-0.8, -0.8],
    [0.8, -0.8],
    [0.8, 0.8],
    [-0.8, 0.8]
    
    
]
faces = [
    [0,1,2],
    [0,2,3]
]

colors = [
    [1,0,0], 
    [0,1,0],
    [0,0,1],
    [1,1,0],
    [1,0,1],
    [0,1,1]
]

colorActive = 0


qtdVertices = len(vertices)
qtdFaces = len(faces)
vaoID = 0
shaderID = 0
myShader = None

# Função para configurações iniciais da minha aplicação.
def init():
    global vertices, vaoID, faces, myShader
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
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2*4, ctypes.c_void_p(0))
    
    '''glVertexAttribPointer(1, # código do atributo(cor)
                          3, # qtd de valores do atributo
                          GL_FLOAT, # tipo dos valores do atributo
                          GL_FALSE, # deseja normalizar os valores
                          5*4, # quantidade de bytes entre um atributo e o próximo
                          ctypes.c_void_p(2*4)) # ponteiro pra void'''
    
    glEnableVertexAttribArray(0) # habilita o atributo posição (location = 0)
    # glEnableVertexAttribArray(1) # habilita o atributo cor (location = 1)

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
    myShader = Shader(
    'C:/Users/Usuário/Desktop/College Things/Repositórios/Computacao-Grafica/Professor Rafael Ivo/Python/Estudos/shaders/06_vertexShader.glsl',
    'C:/Users/Usuário/Desktop/College Things/Repositórios/Computacao-Grafica/Professor Rafael Ivo/Python/Estudos/shaders/06_fragmentShader.glsl'
)



    # ler o arquivo fragment shader
    with open('C:/Users/Usuário/Desktop/College Things/Repositórios/Computacao-Grafica/Professor Rafael Ivo/Python/Estudos/shaders/06_fragmentShader.glsl', 'r') as file:
        fsSource = file.read()



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
    '''shaderID = glCreateProgram() # criar um shader program
    glAttachShader(shaderID, vsID) # linka o vertex shader
    glAttachShader(shaderID, fsID) # linka o fragment shader
    glLinkProgram(shaderID) # conecta eles em um só'''

# Função para atualizar a renderização da cena.
def render():
    glClear(GL_COLOR_BUFFER_BIT)


    # glUseProgram(shaderID)
    myShader.bind()
    glBindVertexArray(vaoID)
    myShader.setUniformv('color', colors[colorActive])
    #glDrawArrays(GL_TRIANGLES,
    #             0,
    #             qtdVertices)

    glDrawElements(GL_TRIANGLES, # primitiva
                   3 * qtdFaces, # qtd de faces
                   GL_UNSIGNED_INT, # tipo de dados dos índices (outros tipos = GL_UNSIGNED_BYTE / GL_UNSIGNED_SHORT)
                   None) # Offset = quantidade de bytes a partir do início. None é pra nenhum pulo a partir do início
    glBindVertexArray(0)
    myShader.unbind()


def keyboard(window, key, scancode, action, mods):
    global colorActive
    if action == glfw.PRESS:
        if key == glfw.KEY_ESCAPE: glfw.set_window_should_close(window, True)
        if key == glfw.KEY_SPACE: colorActive = (colorActive + 1) % len(colors)



# Função principal
def main():
    glfw.init() # Inicializando a API GLFW
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    window = glfw.create_window(500,500,'03 - Primitvas',None,None) # Criando a janela
    glfw.make_context_current(window) # Criando o contexto OpenGL na janela

    glfw.set_key_callback(window, keyboard)


    init() # Chama a função de configurações iniciais da aplicação.
    while not glfw.window_should_close(window): # Enquanto a janela não é fechada
        glfw.poll_events() # Tratamento de eventos
        render() # chama a função render para atualizar os buffers na aplicação
        glfw.swap_buffers(window) # Troca de frame buffers
    glfw.terminate() # Finalizando a API GLFW

if __name__ == '__main__':
    main()