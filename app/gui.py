from raylib.pyray import PyRay
from raylib.colors import *


pyray = PyRay()

pyray.init_window(800, 450, "Hello Pyray")
pyray.set_target_fps(60)

camera = pyray.Camera3D([18.0, 16.0, 18.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], 45.0, 0)
pyray.set_camera_mode(camera, pyray.CAMERA_ORBITAL)

while not pyray.window_should_close():
    pyray.update_camera(pyray.pointer(camera))
    pyray.begin_drawing()
    pyray.clear_background(RAYWHITE)
    pyray.begin_mode_3d(camera)
    pyray.draw_grid(20, 1.0)
    pyray.end_mode_3d()
    pyray.draw_text("Hello world", 190, 200, 20, VIOLET)
    pyray.end_drawing()
pyray.close_window()
