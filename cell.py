class Cell:
    def __init__(self, i, j):
        x = j * 10 + 6
        y = i * 10 + 6
        self.is_alive = False
        self.next_state = None
        self.position_in_canvas = (x, y)
        self.position_in_matrix = (i, j)

    def switch_state(self):
        self.is_alive = not self.is_alive
