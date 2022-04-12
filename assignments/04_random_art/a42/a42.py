#!/usr/bin/env python3

import random
from datetime import datetime

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

def main():
    art = ArtConfig()
    table = art.gen_table()
    art.print_table(table)

if __name__ == '__main__':
    main()
