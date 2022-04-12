#!/usr/bin/env python3
'''Assignment 4 Part 1 template'''
# print(__doc__)

from typing import IO

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


def writeHTMLcomment(f: IO[str], t: int, com: str):
    '''writeHTMLcomment method'''
    ts: str = "   " * t
    f.write(f'{ts}<!--{com}-->\n')

def drawRectLine(f: IO[str], t: int, r: Rectangle):
    ts: str = "   " * t
    line: str = f'<rect x="{r.x}" y="{r.y}" width="{r.width}" height="{r.height}" fill="rgb({r.red}, {r.green}, {r.blue})" fill-opacity="{r.op}"></rect>'
    f.write(f"{ts}{line}\n")

def drawCircleLine(f: IO[str], t: int, c: Circle):
    '''drawCircle method'''
    ts: str = "   " * t
    line: str = f'<circle cx="{c.cx}" cy="{c.cy}" r="{c.rad}" fill="rgb({c.red}, {c.green}, {c.blue})" fill-opacity="{c.op}"></circle>'
    f.write(f"{ts}{line}\n")

def genArt(f: IO[str], t: int):
   '''genART method'''
   drawCircleLine(f, t, Circle((50,50,50), (255,0,0,1.0)))
   drawCircleLine(f, t, Circle((150,50,50), (255,0,0,1.0)))
   drawCircleLine(f, t, Circle((250,50,50), (255,0,0,1.0)))
   drawCircleLine(f, t, Circle((350,50,50), (255,0,0,1.0)))
   drawCircleLine(f, t, Circle((450,50,50), (255,0,0,1.0)))
   drawCircleLine(f, t, Circle((50,250,50), (0,0,255,1.0)))
   drawCircleLine(f, t, Circle((150,250,50), (0,0,255,1.0)))
   drawCircleLine(f, t, Circle((250,250,50), (0,0,255,1.0)))
   drawCircleLine(f, t, Circle((350,250,50), (0,0,255,1.0)))
   drawCircleLine(f, t, Circle((450,250,50), (0,0,255,1.0)))
   drawRectLine(f, t, Rectangle((0,100,100,100), (0,255,0,0.8)))
   drawRectLine(f, t, Rectangle((60,100,100,100), (0,0,255,0.8)))
   drawRectLine(f, t, Rectangle((120,100,100,100), (255,0,0,0.8)))
   drawRectLine(f, t, Rectangle((180,100,100,100), (0,255,0,0.8)))
   drawRectLine(f, t, Rectangle((240,100,100,100), (0,0,255,0.8)))
   drawRectLine(f, t, Rectangle((300,100,100,100), (255,0,0,0.8)))

def openSVGcanvas(f: IO[str], t: int, canvas: tuple):
     '''openSVGcanvas method'''
     ts: str = "   " * t
     writeHTMLcomment(f, t, "Define SVG drawing box")
     f.write(f'{ts}<svg width="{canvas[0]}" height="{canvas[1]}">\n')

def closeSVGcanvas(f: IO[str], t: int):
    '''closeSVGcanvas method'''
    ts: str = "   " * t
    f.write(f'{ts}</svg>\n')
    f.write(f'</body>\n')
    f.write(f'</html>\n')

def writeHTMLline(f: IO[str], t: int, line: str):
     '''writeLineHTML method'''
     ts = "   " * t
     f.write(f"{ts}{line}\n")

def writeHTMLHeader(f: IO[str], winTitle: str):
    '''writeHeadHTML method'''
    writeHTMLline(f, 0, "<html>")
    writeHTMLline(f, 0, "<head>")
    writeHTMLline(f, 1, f"<title>{winTitle}</title>")
    writeHTMLline(f, 0, "</head>")
    writeHTMLline(f, 0, "<body>")

def writeHTMLfile():
    '''writeHTMLfile method'''
    fnam: str = "myPart1Art.html"
    winTitle = "My Art"
    f: IO[str] = open(fnam, "w")
    writeHTMLHeader(f, winTitle)
    openSVGcanvas(f, 1, (500,300))
    genArt(f, 2)
    closeSVGcanvas(f, 1)
    f.close()

def main():
    '''main method'''
    writeHTMLfile()

main()


