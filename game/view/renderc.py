def draw_scene(model, screen):
    key_pressed = 0

    screen.clear()
    screen.refresh()

    while key_pressed != ord('q'):
        key_pressed = screen.getch()
