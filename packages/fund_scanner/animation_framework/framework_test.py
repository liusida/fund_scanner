""" Testing """
import matplotlib
matplotlib.rcParams['backend'] = 'TkAgg'

import unittest
import fund_scanner.animation_framework.framework as fw
import matplotlib.pyplot as plt

class TestFramework(unittest.TestCase):

    def test_show(self):
        ani = fw.FWMovie(frame_num=5)
        dot = fw.FWDot()
        dot1 = fw.FWDot()
        t = fw.FWText()

        dot2 = MyDot(10)
        g = MyFancyDot(1)

        g.add([dot, dot1, t])
        ani.add_objects([g, dot2])

        plt.show()


class MyDot(fw.FWDot):
    def __init__(self, offset=0):
        self.offset = offset
        super().__init__()

    def step(self):
        self.pos_x += 1
        if self.pos_x > self.movie.boundary('x_max'):
            self.pos_x = self.movie.boundary('x_max')
        self.pos_y += 1 + self.offset
        if self.pos_y > self.movie.boundary('y_max'):
            self.pos_y = self.movie.boundary('y_max')
        self.pos_z += (self.movie.boundary('z_max') - self.pos_z) / 5
        return super().step()

class MyFancyDot(fw.FWGroup):
    def __init__(self, offset=0):
        self.offset = offset
        super().__init__()

    def step(self):
        self.pos_x += 1
        if self.pos_x > self.movie.boundary('x_max'):
            self.pos_x = self.movie.boundary('x_max')
        self.pos_y += 1 + self.offset
        if self.pos_y > self.movie.boundary('y_max'):
            self.pos_y = self.movie.boundary('y_max')
        self.pos_z += (self.movie.boundary('z_max') - self.pos_z) / 5
        return super().step()

if __name__ == '__main__':
    fig = plt.figure()
    plt.show()
    unittest.main()