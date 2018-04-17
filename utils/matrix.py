import random
from copy import copy


def dot(arr1, arr2):
    if len(arr1) != len(arr2):
        raise Exception('vectors length not match')
    return sum([x*y for x, y in zip(arr1, arr2)])


class Matrix:
    def __init__(self, rows, cols, arr=None):
        self.__rows = rows
        self.__cols = cols
        self._array = [
                        [random.random() for _ in range(cols)]
                        for _ in range(rows)
                      ] if not arr else copy(arr)

    @property
    def rows(self):
        return self.__rows

    @property
    def cols(self):
        return self.__cols

    def get_row(self, index):
        return self._array[index]

    def get_column(self, index):
        return [x[index] for x in self._array]

    def transpose(self):
        newarr = [self.get_column(x) for x in range(self.cols)]
        return self.new(newarr)

    @classmethod
    def identity(cls, size):
        arr = []
        for x in range(size):
            row = []
            for y in range(size):
                if x == y:
                    row.append(1.)
                else:
                    row.append(0)
            arr.append(row)
        return cls.new(arr)

    @property
    def array(self):
        return self._array

    @classmethod
    def new_zero_matrix(cls, rows, cols):
        arr = [[0 for _ in range(cols)] for _ in range(rows)]
        return cls(rows, cols, arr)

    @classmethod
    def new(cls, arr):
        rows = len(arr)
        cols = len(arr[0])
        if not arr or not isinstance(arr, list) or not cols:
            raise Exception('invalid array')
        if not all(map(lambda x: len(x) == cols, arr)):
            raise Exception('invalid size')
        return cls(rows, cols, arr)

    def __mul__(self, mat):
        if self.cols != mat.rows:
            raise Exception('sizes do not match')
        result = []
        for i in range(self.rows):
            row = []
            for j in range(mat.cols):
                row.append(dot(self.get_row(i), mat.get_column(j)))
            result.append(row)
        return self.new(result)

    def __str__(self):
        string = ''
        for row in self._array:
            for e in row:
                string += str(e) + "  "
            string += '\n'
        return string
