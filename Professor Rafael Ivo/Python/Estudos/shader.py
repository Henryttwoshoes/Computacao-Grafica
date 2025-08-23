from OpenGL.GL import *
import OpenGL.GL.shaders as gls

class Shader:
    def __init__(self, vertexShaderFileName, fragmentShaderFileName):
        with open(vertexShaderFileName, 'r') as file:
            vsSource = file.read()

        # ler o arquivo fragment shader
        with open(fragmentShaderFileName, 'r') as file:
            fsSource = file.read()

        # Comandos abaixo são uma forma mais prática que a linguagem Python disponibiliza nesse módulo de OpenGL usado no programa. Esses códigos fazem os comandos em comentário logo abaixo dispensáveis para a implementação dos shaders.
        vsID = gls.compileShader(vsSource, GL_VERTEX_SHADER)
        fsID = gls.compileShader(fsSource, GL_FRAGMENT_SHADER)
        self.shaderID = gls.compileProgram(vsID, fsID)

    def bind(self):
        glUseProgram(self.shaderID)

    def unbind(self):
        glUseProgram(0)

    def setUniform(self, name, x, y=None, z=None, w=None):
        name_loc = glGetUniformLocation(self.shaderID, name)
        if y == None: glUniform1f(name_loc, x)
        elif z == None: glUniform2f(name_loc, x, y)
        elif w == None: glUniform3f(name_loc, x , y, z)
        else: glUniform4f(name_loc, x, y, z, w)

    def setUniformv(self, name, values):
        name_loc = glGetUniformLocation(self.shaderID, name)
        if len(values) == 1: glUniform1fv(name_loc, 1, values)
        elif len(values) == 2: glUniform2fv(name_loc, 1, values)
        elif len(values) == 3: glUniform3fv(name_loc, 1, values)
        else: glUniform4fv(name_loc, values)