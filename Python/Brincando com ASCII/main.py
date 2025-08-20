import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont
import ctypes
import random

# -------------------------------
# Função auxiliar: carrega um shader de arquivo .vert ou .frag
# -------------------------------
def load_shader_source(path):
    with open(path, "r") as f:
        return f.read()

# -------------------------------
# Cria o programa de shader (vertex + fragment)
# -------------------------------
def create_shader_program():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SHADER_DIR = os.path.join(BASE_DIR, "shaders")

    vertex_src = load_shader_source(os.path.join(SHADER_DIR, "cell.vert"))
    fragment_src = load_shader_source(os.path.join(SHADER_DIR, "cell.frag"))

    return compileProgram(
        compileShader(vertex_src, GL_VERTEX_SHADER),
        compileShader(fragment_src, GL_FRAGMENT_SHADER)
    )

# -------------------------------
# Cria o quad (um retângulo feito de 2 triângulos)
# Esse quad é a "célula" base onde vamos colar o caractere.
# -------------------------------
def create_quad_vao():
    # vértices: posição (x,y) + coordenadas de textura (u,v)
    vertices = np.array([
        -0.5, -0.5, 0.0, 0.0,  # canto inferior esquerdo
         0.5, -0.5, 1.0, 0.0,  # canto inferior direito
         0.5,  0.5, 1.0, 1.0,  # canto superior direito
        -0.5,  0.5, 0.0, 1.0   # canto superior esquerdo
    ], dtype=np.float32)

    indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    # VBO (Vertex Buffer Object) → guarda vértices
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # EBO (Element Buffer Object) → guarda índices
    ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    # Layout: posição = location 0, textura = location 1
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(8))
    glEnableVertexAttribArray(1)

    return vao

# -------------------------------
# Cache de texturas → dicionário para não recriar texturas repetidas
# -------------------------------
texture_cache = {}

# -------------------------------
# Cria textura para um caractere ASCII
# -------------------------------
def get_char_texture(char, font_size=16):
    """Retorna a textura OpenGL do caractere. Usa cache para eficiência."""
    if char in texture_cache:
        return texture_cache[char]

    # cria imagem preta e desenha o caractere em branco
    img = Image.new("L", (font_size, font_size), color=0)
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((4, 4), char, font=font, fill=255)

    img_data = np.array(img, dtype=np.uint8)

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RED, img.size[0], img.size[1],
                 0, GL_RED, GL_UNSIGNED_BYTE, img_data)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    # guarda no cache
    texture_cache[char] = tex_id
    return tex_id

# -------------------------------
# Função principal
# -------------------------------
def main():
    pygame.init()
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)

    prog = create_shader_program()
    vao = create_quad_vao()

    # Configura grade
    cols, rows = 40, 25
    tile_width = 2.0 / cols
    tile_height = 2.0 / rows

    loc_offset = glGetUniformLocation(prog, "offset")
    loc_scale = glGetUniformLocation(prog, "scale")

    # -------------------------------
    # Cria a grade de símbolos
    # Exemplo: números aleatórios entre 33 e 126 (caracteres visíveis ASCII)
    # -------------------------------
    symbols = [[chr(random.randint(33, 126)) for x in range(cols)] for y in range(rows)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(prog)
        glBindVertexArray(vao)

        # desenha a grade
        for y in range(rows):
            for x in range(cols):
                char = symbols[y][x]   # pega o caractere da célula
                tex = get_char_texture(char)  # busca/cria a textura

                glBindTexture(GL_TEXTURE_2D, tex)

                # calcula posição na tela
                offset_x = -1.0 + (x + 0.5) * tile_width
                offset_y = -1.0 + (y + 0.5) * tile_height

                # envia uniforms
                glUniform2f(loc_offset, offset_x, offset_y)
                glUniform2f(loc_scale, tile_width, tile_height)

                # desenha o quad com a textura desse caractere
                glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
