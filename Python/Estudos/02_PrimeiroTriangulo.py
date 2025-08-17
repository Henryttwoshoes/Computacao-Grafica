import glfw
from OpenGL.GL import *

vertices = [
    [-0.5, -0.5],
    [0.5, -0.5],
    [0. , 0.5]
]

cores = [
    [1,0,0],
    [0,1,0],
    [0,0,1]
]

# Função para configurações iniciais da minha aplicação.
def init():
    glClearColor(1,1,1,1)

# Função para atualizar a renderização da cena.
def render():
    glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_TRIANGLES)
    for v, c in zip(vertices, cores):
        glColor3fv(c)
        glVertex2fv(v)
    glEnd()

# Função principal
def main():
    glfw.init() # Inicializando a API GLFW
    window = glfw.create_window(500,500,'02 - Primeiro Triângulo',None,None) # Criando a janela
    glfw.make_context_current(window) # Criando o contexto OpenGL na janela
    init() # Chama a função de configurações iniciais da aplicação.
    while not glfw.window_should_close(window): # Enquanto a janela não é fechada
        glfw.poll_events() # Tratamento de eventos
        render() # chama a função render para atualizar os buffers na aplicação
        glfw.swap_buffers(window) # Troca de frame buffers
    glfw.terminate() # Finalizando a API GLFW

if __name__ == '__main__':
    main()