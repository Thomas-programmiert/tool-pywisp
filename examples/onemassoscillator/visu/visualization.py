# -*- coding: utf-8 -*-

import matplotlib as mpl
import matplotlib.patches
import matplotlib.lines
import matplotlib.transforms
import numpy as np
from exampleData import settings as st

from pywisp.visualization import MplVisualizer


class MplOneMassOscillatorVisualizer(MplVisualizer):
    def __init__(self, q_widget, q_layout):
        MplVisualizer.__init__(self, q_widget, q_layout)
        self.axes.set_xlim(-1.5, 1)
        self.axes.set_ylim(-1, 2)
        self.axes.set_aspect("equal")

        x = 0.5

        self.ground = mpl.lines.Line2D([-1.5,1],[0,0], linewidth=2.5, color="black")
        self.wall = mpl.lines.Line2D([-1,-1],[0,1], linewidth=2.5, color="black")

        self.box = mpl.patches.Rectangle(xy=[x-0.25,0], width=0.5, height=0.5, 
                                         facecolor="lightgrey", edgecolor="black",
                                         linewidth=1.5)


        self.springBumps = 12
        self.springPos = 0.125
        self.springHeight = 0.05

        divisor = (self.springBumps + 1) * 4
        self.spring = [
            mpl.lines.Line2D([ 0/divisor*(x+0.75)-1, 2/divisor*(x+0.75)-1],[self.springPos,self.springPos], linewidth=1.5, color="black"),
            mpl.lines.Line2D([ 2/divisor*(x+0.75)-1, 3/divisor*(x+0.75)-1],[self.springPos,self.springPos+self.springHeight], linewidth=1.5, color="black")
        ]
        
        for i in range((self.springBumps-1)):
            self.spring.append(mpl.lines.Line2D([(4*i+3)/divisor*(x+0.75)-1, (4*i+5)/divisor*(x+0.75)-1],[self.springPos+self.springHeight,self.springPos-self.springHeight], linewidth=1.5, color="black"))
            self.spring.append(mpl.lines.Line2D([(4*i+5)/divisor*(x+0.75)-1, (4*i+7)/divisor*(x+0.75)-1],[self.springPos-self.springHeight,self.springPos+self.springHeight], linewidth=1.5, color="black"))

        self.spring.append(mpl.lines.Line2D([(divisor-5)/divisor*(x+0.75)-1,(divisor-3)/divisor*(x+0.75)-1],[self.springPos+self.springHeight,self.springPos-self.springHeight], linewidth=1.5, color="black"))
        self.spring.append(mpl.lines.Line2D([(divisor-3)/divisor*(x+0.75)-1,(divisor-2)/divisor*(x+0.75)-1],[self.springPos-self.springHeight,self.springPos], linewidth=1.5, color="black"))
        self.spring.append(mpl.lines.Line2D([(divisor-2)/divisor*(x+0.75)-1,(divisor-0)/divisor*(x+0.75)-1],[self.springPos,self.springPos], linewidth=1.5, color="black"))

        self.axes.add_patch(self.box)
        self.axes.add_line(self.ground)
        self.axes.add_line(self.wall)

        for springSegment in self.spring:
            self.axes.add_line(springSegment)

        self.canvas.draw_idle()

    def update(self, dataPoints):
        x = 0
        for name, buffer in dataPoints.items():
            if buffer.values:
                if name == 'pos':
                    x = buffer.values[-1]

        self.box.set_x(x-0.25)

        divisor = (self.springBumps + 1) * 4
        self.spring[ 0].set_data([ 0/divisor*(x+0.75)-1, 2/divisor*(x+0.75)-1],[self.springPos,self.springPos])
        self.spring[ 1].set_data([ 2/divisor*(x+0.75)-1, 3/divisor*(x+0.75)-1],[self.springPos,self.springPos+self.springHeight])

        for i in range((self.springBumps-1)):
            self.spring[2*i+2].set_data([(4*i+3)/divisor*(x+0.75)-1, (4*i+5)/divisor*(x+0.75)-1],[self.springPos+self.springHeight,self.springPos-self.springHeight])
            self.spring[2*i+3].set_data([(4*i+5)/divisor*(x+0.75)-1, (4*i+7)/divisor*(x+0.75)-1],[self.springPos-self.springHeight,self.springPos+self.springHeight])

        self.spring[-3].set_data([(divisor-5)/divisor*(x+0.75)-1,(divisor-3)/divisor*(x+0.75)-1],[self.springPos+self.springHeight,self.springPos-self.springHeight])
        self.spring[-2].set_data([(divisor-3)/divisor*(x+0.75)-1,(divisor-2)/divisor*(x+0.75)-1],[self.springPos-self.springHeight,self.springPos])
        self.spring[-1].set_data([(divisor-2)/divisor*(x+0.75)-1,(divisor-0)/divisor*(x+0.75)-1],[self.springPos,self.springPos])

        self.canvas.draw_idle()
        self.saveIfChecked()
