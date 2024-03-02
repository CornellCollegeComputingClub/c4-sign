import random
from datetime import timedelta
from time import sleep

from c4_sign.base_task import ScreenTask
from c4_sign.lib import graphics
from c4_sign.lib.canvas import Canvas

# all sorts must be in place
# yield so we can see the changes
# not quite working, but it's a start
# I CALL DIBS ~Luna


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            yield arr
        arr[j + 1] = key
        yield arr


def merge_sort_in_place(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m
    L = [0] * n1
    R = [0] * n2
    for i in range(0, n1):
        L[i] = arr[l + i]
    for i in range(0, n2):
        R[i] = arr[m + 1 + i]
    i = j = 0
    k = l
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
        yield arr
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
        yield arr
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1
        yield arr


def merge_sort(arr):
    current_size = 1
    while current_size < len(arr) - 1:
        left = 0
        while left < len(arr) - 1:
            mid = min((left + current_size - 1), (len(arr) - 1))
            right = (2 * current_size + left - 1, len(arr) - 1)[2 * current_size + left - 1 > len(arr) - 1]
            yield from merge_sort_in_place(arr, left, mid, right)
            left += current_size * 2
        current_size = 2 * current_size
        yield arr
    yield arr


def qs_partition(arr, low, high):
    i = low - 1
    pivot = arr[high]
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            yield arr
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    yield arr
    return i + 1


def quick_sort(arr, low, high):
    if low < high:
        pi = yield from qs_partition(arr, low, high)
        yield from quick_sort(arr, low, pi - 1)
        yield from quick_sort(arr, pi + 1, high)
    yield arr


def quick_sort_wrapper(arr):
    yield from quick_sort(arr, 0, len(arr) - 1)


def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[i] < arr[l]:
        largest = l
    if r < n and arr[largest] < arr[r]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        yield arr
        yield from heapify(arr, n, largest)


def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        yield arr
        yield from heapify(arr, i, 0)
    yield arr


class SortingAlgorithms(ScreenTask):
    name = "Sorting Algorithms"
    artist = "Luna"

    def __init__(self):
        super().__init__(timedelta(seconds=5))
        self.sorting_algorithms = {
            "Insertion Sort": insertion_sort,
            "Merge Sort": merge_sort,
            "Quick Sort": quick_sort_wrapper,
            "Heap Sort": heap_sort,
        }
        self.sorting_algorithm = None
        self.arr = None

    def prepare(self):
        self.sorting_algorithm_name = random.choice(list(self.sorting_algorithms.keys()))
        # array is [1..32] shuffled
        self.arr = list(range(1, 33))
        random.shuffle(self.arr)
        self.sorting_algorithm = self.sorting_algorithms[self.sorting_algorithm_name](self.arr)
        return True

    def draw_frame(self, canvas: Canvas, delta_time: timedelta) -> bool:
        # draw array
        for i, x in enumerate(self.arr):
            graphics.stroke_line(canvas, i, 32, i, 32 - x, 0xFFFFFF)
        try:
            next(self.sorting_algorithm)
            sleep(0.05)
            return False
        except StopIteration:
            return True

    def get_lcd_text(self) -> str:
        title = self.sorting_algorithm_name.center(16)
        artist = "By: " + self.artist
        artist = artist.center(16)
        return title + artist
