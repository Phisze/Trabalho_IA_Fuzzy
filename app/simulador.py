import numpy
from raylib.pyray import PyRay
from raylib.colors import *


def simular() -> None:
    # sistema(400, 200, "centroid")
    # pyplot.show()
    
    altitude_real = 0
    altitude_relativa = 0
    predios = numpy.zeros(10)
    
    pyray = PyRay()

    pyray.init_window(800, 500, "Simulador")
    pyray.set_target_fps(60)
    
    while not pyray.window_should_close():
        pyray.begin_drawing()
        pyray.clear_background(RAYWHITE)

        #texture = pyray.
        pyray.draw_texture()

        pyray.end_drawing()
    
    pyray.close_window()
