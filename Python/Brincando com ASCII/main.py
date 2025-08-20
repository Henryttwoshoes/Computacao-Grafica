import pygame
from pygame.locals import *
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
from PIL import Image, ImageDraw, ImageFont
import ctypes

# -------------------------
# Utilitários de Shader
# -------------------------
def load_shader_source(path):
    with open(path, "r") as f:
        return f.read()

def create_shader_program():
    vertex_src = load_shader_source("C:/Users/Usuário/Desktop/College Things/Repositórios/Computacao-Grafica/Python/Brincando com ASCII/shaders/cell.vert")
    fragment_src = load_shader_source("C:/Users/Usuário/Desktop/College Things/Repositórios/Computacao-Grafica/Python/Brincando com ASCII/shaders/cell.frag")

    program = compileProgram(
        compileShader(vertex_src, GL_VERTEX_SHADER),
        compileShader(fragment_src, GL_FRAGMENT_SHADER)
    )
    return program

# -------------------------
# Textura ASCII
# -------------------------
def create_ascii_texture(char=",", font_size=16):
    # cria uma imagem em tons de cinza (L)
    img = Image.new("L", (font_size, font_size), color=0)
    draw = ImageDraw.Draw(img)

    # fonte padrão (pode trocar por TTF se quiser depois)
    font = ImageFont.load_default()
    draw.text((4, 4), char, font=font, fill=255)

    img_data = np.array(img, dtype=np.uint8)

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RED, img.size[0], img.size[1],
                 0, GL_RED, GL_UNSIGNED_BYTE, img_data)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    return tex_id

# -------------------------
# Quad para desenhar um tile
# -------------------------
def create_quad_vao():
    vertices = np.array([
        # pos      # texcoords
        -0.5, -0.5,  0.0, 0.0,
         0.5, -0.5,  1.0, 0.0,
         0.5,  0.5,  1.0, 1.0,
        -0.5,  0.5,  0.0, 1.0
    ], dtype=np.float32)

    indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    # posição (2 floats)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # texcoords (2 floats)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(8))
    glEnableVertexAttribArray(1)

    return vao

# -------------------------
# Main Loop
# -------------------------
def main():
    pygame.init()
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)

    prog = create_shader_program()
    vao = create_quad_vao()
    tex = create_ascii_texture(",")

    # configurações da grade
    cols, rows = 40, 25
    tile_width = 2.0 / cols   # escala para caber na tela normalizada (-1 a 1)
    tile_height = 2.0 / rows

    # localizações dos uniforms
    loc_offset = glGetUniformLocation(prog, "offset")
    loc_scale = glGetUniformLocation(prog, "scale")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(prog)
        glBindVertexArray(vao)
        glBindTexture(GL_TEXTURE_2D, tex)

        # percorre grade e desenha
        for y in range(rows):
            for x in range(cols):
                offset_x = -1.0 + (x + 0.5) * tile_width
                offset_y = -1.0 + (y + 0.5) * tile_height
                glUniform2f(loc_offset, offset_x, offset_y)
                glUniform2f(loc_scale, tile_width, tile_height)
                glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
