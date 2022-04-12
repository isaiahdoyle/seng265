#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 06 12:29:25 2022
Last edited on Sun Apr 10 16:33:12 2022
@author: isaiahdoyle

This is a program that, based on given arguments (if present), generates
a table of randomized shapes of random size, colour, etc. and writes the
shapes to an HTML file in SVG format. By default, the shapes will be
written to output.html, so be sure nothing important is being overwritten!

Note: As requested, importing is not used for supplementary classes from
a41.py and a42.py. Thus, this file can be daunting at first. Most of the
code is simply copy/pasted from parts 1 and 2, so the majority of this
mess can be avoided. Here's a guide to everything in this document:
    - Lines 27 - 73: classes from a41.py
    - Lines 75 - 156: classes from a42.py
    - Lines 158 - 200: functions from a41.py
    - Lines 202 - end: new code for part 3
"""
import random
import sys
from typing import IO


### BEGIN A41 CLASSES ###
class Circle:
    """Circle class"""
    def __init__(self, cir: tuple, col: tuple):
        self.cx: int = cir[0]
        self.cy: int = cir[1]
        self.rad: int = cir[2]
        self.red: int = col[0]
        self.green: int = col[1]
        self.blue: int = col[2]
        self.op: float = col[3]

class Rectangle:
    """Rectangle class"""
    def __init__(self, rect: tuple, fill: tuple):
        self.x: int = rect[0]
        self.y: int = rect[1]
        self.width: int = rect[2]
        self.height: int = rect[3]
        self.red: int = fill[0]
        self.green: int = fill[1]
        self.blue: int = fill[2]
        self.op: float = fill[3]

class ProEpilogue:
    """ HTML/SVG Prologue/Epilogue class

        A class designed to configure the HTML/SVG prologues and epilogues
        for a given canvas workspace.

        Object variables:
            - file: I/O stream given by an opened HTML file
            - winTitle: the title of the HTML window
            - canvas: the dimensions of the SVG canvas
    """
    def __init__(self, file: IO[str], winTitle: str, canvas: tuple):
        self.file = file
        self.winTitle = winTitle
        self.canvas = canvas

    def write_prologue(self):
        """ write_prologue method

            Combines pre-made writeHTMLHeader and openSVGcanvas methods
            to write HTML/SVG prologue to file
        """
        writeHTMLHeader(self.file, self.winTitle)
        openSVGcanvas(self.file, 1, self.canvas)

    def write_epilogue(self):
        """ write_epilogue method

            Ends file by writing HTML/SVG epilogue
        """
        closeSVGcanvas(self.file, 1)
### END A41 CLASSES ###

### BEGIN A42 CLASSES ###
class GenRandom:
    """ GenRandom class

        A class reserved for generating a random value within a given
        range.
    """
    def random(min, max):
        """ Generates a random value in a range

            The range min and max values can both be either ints or
            floats - if floats, the random value will be rounded to one
            decimal place.
        """
        if type(max) == float:
            # gets random float and rounds to one decimal place
            return round(random.uniform(min, max), 1)

        return random.randrange(min, max)

class ArtConfig:
    """ ArtConfig class

        A class for configuring a table of data, following the format
        specified in the assignment 4 documentation. That is, 12 random
        values will be chosen for each row.

        Object variables:
            - cnt: the number of shapes to generate
                -> default 10
            - vp_range: the range for x and y coordinates (max 999x999)
                -> default (960, 600)
    """
    def __init__(self, cnt: int = 10, vp_range: tuple = (960, 600)):
        self.cnt = cnt
        self.vp_range = vp_range

    def gen_table(self) -> list[list]:
        """ Generates a table of cnt shapes

            Output:
                - table of rows, each row representing a shape except for
                  the first row which is a row of headers for each column
        """
        table = [['CNT', 'SHA', 'X', 'Y', 'RAD', 'RX', 'RY', 'W', 'H', 'R', 'G', 'B', 'OP']]
        for i in range(self.cnt):
            sha = GenRandom.random(0, 3)
            x = GenRandom.random(0, min(self.vp_range[0], 999))
            y = GenRandom.random(0, min(self.vp_range[1], 999))
            rad = GenRandom.random(0, 100)
            rx = GenRandom.random(10, 30)
            ry = GenRandom.random(10, 30)
            w = GenRandom.random(10, 100)
            h = GenRandom.random(1, 100)
            r = GenRandom.random(0, 255)
            g = GenRandom.random(0, 255)
            b = GenRandom.random(0, 255)
            op = GenRandom.random(0.0, 1.0)

            table.append([i, sha, x, y, rad, rx, ry, w, h, r, g, b, op])

        return table

    def print_table(self, table: list[list]):
        """ Prints a table of shapes to stdout, formatted by columns

            Input:
                - table: a table with rows representing shapes generated
                         by gen_table()
        """
        for row in table:
            col_no = -1
            for col in row:
                col_no += 1

                if col_no == 12:
                    end = '\n'
                else:
                    end = ' '

                print('{:>3}'.format(col), end=end)
### END A42 CLASSES ###

### BEGIN A41 FUNCTIONS ###
def writeHTMLcomment(file: IO[str], tab: int, comment: str):
    """writeHTMLcomment method"""
    ts: str = "   " * tab
    file.write(f'{ts}<!--{comment}-->\n')

def drawRectLine(file: IO[str], tab: int, rect: Rectangle):
    """drawRectangle method"""
    ts: str = "   " * tab
    line: str = f'<rect x="{rect.x}" y="{rect.y}" width="{rect.width}" height="{rect.height}" fill="rgb({rect.red}, {rect.green}, {rect.blue})" fill-opacity="{rect.op}"></rect>'
    file.write(f"{ts}{line}\n")

def drawCircleLine(file: IO[str], tab: int, circle: Circle):
    """drawCircle method"""
    ts: str = "   " * tab
    line: str = f'<circle cx="{circle.cx}" cy="{circle.cy}" r="{circle.rad}" fill="rgb({circle.red}, {circle.green}, {circle.blue})" fill-opacity="{circle.op}"></circle>'
    file.write(f"{ts}{line}\n")

def openSVGcanvas(file: IO[str], tab: int, canvas: tuple):
     """openSVGcanvas method"""
     ts: str = "   " * tab
     writeHTMLcomment(file, tab, "Define SVG drawing box")
     file.write(f'{ts}<svg width="{canvas[0]}" height="{canvas[1]}">\n')

def closeSVGcanvas(file: IO[str], tab: int):
    """closeSVGcanvas method"""
    ts: str = "   " * tab
    file.write(f'{ts}</svg>\n')
    file.write(f'</body>\n')
    file.write(f'</html>\n')

def writeHTMLline(file: IO[str], t: int, line: str):
     """writeLineHTML method"""
     ts = "   " * t
     file.write(f"{ts}{line}\n")

def writeHTMLHeader(file: IO[str], winTitle: str):
    """writeHeadHTML method"""
    writeHTMLline(file, 0, "<html>")
    writeHTMLline(file, 0, "<head>")
    writeHTMLline(file, 1, f"<title>{winTitle}</title>")
    writeHTMLline(file, 0, "</head>")
    writeHTMLline(file, 0, "<body>")
### END A41 FUNCTIONS ###

### BEGIN NEW CODE FOR A43 ###
def create_art(file: IO[str], table: list[list]):
    """ Writes shapes from table to file

        Input:
            - file: HTML file stream to be written to
            - table: table of shapes generated by ArtConfig
    """
    if type(table[0][0]) == str:
        table.pop(0)

    for row in table:
        # ignore header row
        if row[0] not in range(len(table)):
            continue

        if row[1] == 1:
            data = (row[2], row[3], row[7], row[8])
            color = (row[9], row[10], row[11], row[12])
            rect = Rectangle(data, color)
            drawRectLine(file, 1, rect)
        else:
            data = (row[2], row[3], row[4])
            color = (row[9], row[10], row[11], row[12])
            circle = Circle(data, color)
            drawCircleLine(file, 1, circle)

def parse_args(argv: list):
    """ Parses CLI arguments

        Input:
            - argv: list of CLI arguments given by sys.argv
    """
    return argv[1], int(argv[2]), tuple(int(val) for val in argv[3].split('x'))

def main():
    """ Entry point to program

        Input: ./a43.py <output filename> <shape count> <canvas size>
    """
    if len(sys.argv) < 4:
        print('Usage: ./a43.py <output filename> <shape count> <canvas size>')
        exit(404)

    argv = parse_args(sys.argv)
    filename: str = argv[0]
    cnt: int = argv[1]
    canvas: tuple = argv[2]

    with open(filename, 'w') as file:
        html = ProEpilogue(file, 'Assignment 4 Art', canvas)
        html.write_prologue()

        art = ArtConfig(cnt, canvas)
        table = art.gen_table()

        create_art(file, table)

        html.write_epilogue()


if __name__ == '__main__':
    main()
