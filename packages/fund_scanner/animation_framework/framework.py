import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
import mpl_toolkits.mplot3d.axes3d as p3
import mpl_toolkits.mplot3d.art3d as art3d
from IPython.display import display,HTML
from ipywidgets import IntProgress

# ------------------------------------------------------------
class FWObject():
    def __init__(self, pos_x=0, pos_y=0, pos_z=0):
        """ Init the object """
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.artists = []
        self.parent = None

    def set_movie(self, movie):
        """Enable Object to find movie object"""
        self.movie = movie

    def set_parent(self, parent):
        """Enable Object to find Group Parent"""
        self.parent = parent

    def init_artists(self):
        """TO implement: Need to write proper drawing function
        self.artists = [self.ax.scatter(*self.position())]
        """
        pass

    def position(self):
        """ Return the position array """
        pos = [0., 0., 0.]
        pos = [x+y for x,y in zip(pos, self.get_parent_positon())]
        pos = [x+y for x,y in zip(pos, [self.pos_x, self.pos_y, self.pos_z])]
        return pos

    def get_parent_positon(self):
        if self.parent is not None:
            return self.parent.position()
        else:
            return [0., 0., 0.]

    def step(self):
        """ Calculate the next step of the object """
        for artist in self.artists:
            if artist.__class__ == art3d.Path3DCollection:
                artist._offsets3d = [[x] for x in self.position()]
            if artist.__class__ == art3d.Text3D:
                artist.set_position(xy=self.position()[:2])
                artist.set_3d_properties(z=self.position()[2], zdir='x')
        pass

    def relative_helper(self, min=0, max=1., current=0, total=100):
        """This helper return a relative value based on the current absolute value.
        For example, if 40(current) in 100(total), is 0.4 in the min and max context.
        It's mainly used to calculate the interval value of two position."""
        return current * (max-min) / total + min

    def get_artists(self):
        return self.artists

# ------------------------------------------------------------
class FWDot(FWObject):
    def __init__(self, color=None, alpha=1, size=1, **kwargs):
        self.color = color
        self.size = size
        self.alpha = alpha
        super().__init__(**kwargs)

    def init_artists(self):
        self.artists = [self.movie.ax.scatter(*self.position(), c=self.color, s=self.size, alpha=self.alpha)]
        return super().init_artists()

    def step(self):
        """ Calculate the next step of the object """
        for artist in self.artists:
            artist.set_sizes([self.size])
        return super().step()

# ------------------------------------------------------------


class FWText(FWObject):
    def __init__(self, color=None, text='default', fontsize=12, **kwargs):
        self.text = text
        self.fontsize = fontsize
        self.color = color
        super().__init__(**kwargs)

    def init_artists(self):
        self.artists = [self.movie.ax.text(*self.position(), self.text, fontsize=self.fontsize,
                                           horizontalalignment='center', verticalalignment='center',
                                           bbox=dict(facecolor=self.color, edgecolor=(0.8,0.8,0.8,1), alpha=0.4))]
        return super().init_artists()

    def step(self):
        for artist in self.artists:
            artist.set_text(self.text)
        return super().step()

# ------------------------------------------------------------


class FWGroup(FWObject):
    def __init__(self):
        self.children = []
        super().__init__()

    def add(self, children):
        self.children += children
        for child in children:
            child.set_parent(self)

    def set_movie(self, movie):
        for child in self.children:
            child.set_movie(movie)
        return super().set_movie(movie)

    def init_artists(self):
        for child in self.children:
            child.init_artists()

    def step(self):
        for child in self.children:
            child.step()
        return super().step()

    def get_artists(self):
        return super().get_artists() + [child.get_artists() for child in self.children]

# ------------------------------------------------------------
class FWMovie():
    def __init__(self, frame_num, figsize=[8,5], movie_length=5000, stageArea=[[0,100],[0,100],[0,100]]):
        """ Init a movie """
        self.figsize = figsize
        self.frame_num = frame_num
        self.movie_length = movie_length
        self.interval = movie_length / frame_num
        self.stageArea = stageArea
        self.progress_bar = IntProgress(min=0, max=self.frame_num-1, value=0)
        self.rotate = False
        self.angles = []
        self.heights = []

        self.reset()
        ax = self.ax
        ax.set_xlim(*stageArea[0])
        ax.set_ylim(*stageArea[1])
        ax.set_zlim(*stageArea[2])
        # Get rid of the panes
        ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        # Get rid of the spines
        ax.w_zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        # Get rid of the ticks
        ax.set_xticks([]) 
        ax.set_yticks([]) 
        ax.set_zticks([])        
    
    def boundary(self, direction='x_min'):
        """return the boundary value of the movie"""
        return {
            'x_min': self.stageArea[0][0],
            'x_max': self.stageArea[0][1],
            'y_min': self.stageArea[1][0],
            'y_max': self.stageArea[1][1],
            'z_min': self.stageArea[2][0],
            'z_max': self.stageArea[2][1]
        }[direction]

    def reset(self):
        """ clean up so no need to do plt.show().
        otherwise they all in the memory. """
        plt.clf()
        plt.cla()
        plt.close()
        self.fig = plt.figure(figsize=self.figsize)
        self.ax = p3.Axes3D(self.fig)
        self.objects = []

    def flatten_helper(self, list_of_list):
        ret = []
        for l in list_of_list:
            if type(l)==list:
                ret += self.flatten_helper(l)
            else:
                ret += [l]
        return ret

    def get_artists(self):
        ret = self.flatten_helper([obj.get_artists() for obj in self.objects])
        return (ret)

    def set_rotate(self):
        self.rotate = True
        self.angles = np.linspace(0, 360, num=self.frame_num)
        self.heights = np.concatenate( (np.linspace(0,30,num=self.frame_num/2), np.linspace(30,0,num=self.frame_num/2+1)), axis=0 )

    def update(self, frame):
        """ Key Function for FuncAnimation.
        update every object, and then draw them."""
        for obj in self.objects:
            obj.step()
        if self.rotate:
            self.ax.view_init(self.heights[frame], self.angles[frame])
        self.progress_bar.value = frame
        return self.get_artists()

    def add_objects(self, obj_list):
        """Add new Dots to the movie"""
        for obj in obj_list:
            obj.set_movie(self)
            obj.init_artists()
        self.objects += obj_list

    def get_movie(self, rotate=False):
        """Start generating full movie."""
        if rotate:
            self.set_rotate()
        self.ani = animation.FuncAnimation(self.fig, self.update, frames=self.frame_num, interval=self.interval, blit=True)
        display(self.progress_bar)
        return HTML(self.ani.to_html5_video())

    def display_movie(self, rotate=False):
        """Directly display the movie into Notebook"""
        display(self.get_movie(rotate))
        self.reset()

# ------------------------------------------------------------
# main() is for fast validation
# ------------------------------------------------------------


def main():
    import framework as fw

    class MyDot(fw.FWDot):
        def __init__(self, offset=0):
            self.offset = offset
            super().__init__()
        
        def step(self):
            self.pos_x += 1
            if self.pos_x>self.movie.boundary('x_max'):
                self.pos_x=self.movie.boundary('x_max')
            self.pos_y += 1 + self.offset
            if self.pos_y>self.movie.boundary('y_max'):
                self.pos_y=self.movie.boundary('y_max')
            self.pos_z += (self.movie.boundary('z_max') - self.pos_z) / 5
            return super().step()

    class MyFancyDot(fw.FWGroup):
        def __init__(self, offset=0):
            self.offset = offset
            super().__init__()

        def step(self):
            self.pos_x += 1
            if self.pos_x>self.movie.boundary('x_max'):
                self.pos_x = self.movie.boundary('x_max')
            self.pos_y += 1 + self.offset
            if self.pos_y>self.movie.boundary('y_max'):
                self.pos_y = self.movie.boundary('y_max')
            self.pos_z += (self.movie.boundary('z_max') - self.pos_z) / 5
            return super().step()
            
    ani = fw.FWMovie(frame_num=5)
    dot = FWDot()
    dot1 = FWDot()
    t = FWText()

    dot2 = MyDot(10)
    g = MyFancyDot(1)

    g.add([dot, dot1, t])
    ani.add_objects([g, dot2])

    ani.display_movie()

if __name__ == '__main__':
    main()

    




