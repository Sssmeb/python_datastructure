# -*- coding: utf-8 -*-
# @Time    : 2019/10/19 14:02
# @Author  : CRJ
# @File    : heap.py
# @Software: PyCharm
# @Python3.6
from collections import Iterable


class BinaryHeap(object):
    """利用数组 实现小堆"""

    def __init__(self, max_size=float("inf")):
        self._heap = [float("-inf")]
        self.max_size = max_size
        self.size = 0

    def __len__(self):
        """求长度"""
        # return len(self._heap)  # size
        return self.size

    def heappush(self, *data):
        """向堆中插入元素"""
        if isinstance(data[0], Iterable):
            if len(data) > 1:
                raise ValueError
            data = data[0]
        if self.size + len(data) > self.max_size:
            # 容量不足
            raise ValueError("Capacity is insufficient")

        for x in data:
            self._heap.append(x)
            self._siftup()
            self.size += 1



    def heappop(self):
        """删除堆顶元素"""
        if not self.size:
            raise IndexError("")
        _min = self._heap[1]
        last = self._heap.pop()
        self.size -= 1
        if self.size:  # 为空了就不需要向下了
            self._heap[1] = last
            self._siftdown(1)
        return _min

    def heapify(self, data):
        if not data:
            return
        self._heap.extend(data)
        self.size += len(data)
        for idx in range(self.size >> 1, 0, -1):
            self._siftdown(idx)

    def get_min(self):
        return self._heap[1]

    def _siftup(self):
        """上浮最后一个元素（新插入的元素）"""
        pos = self.size + 1                 			# 插入的位置 由于占位0 所以需要+1
        x = self._heap[-1]                  			# 获取最后一个位置元素
        while x < self._heap[pos >> 1]:     			# 当比父节点小时，执行交换操作
            self._heap[pos] = self._heap[pos >> 1]
            pos >>= 1
        self._heap[pos] = x

    def _siftdown(self, idx):
        """序号为i的元素下沉"""
        temp = self._heap[idx]
        length = self.size
        while 1:
            child_idx = idx << 1
            if child_idx > length:
                break
            if child_idx != length and self._heap[child_idx] > self._heap[child_idx + 1]:
                child_idx += 1
            if temp > self._heap[child_idx]:
                self._heap[idx] = self._heap[child_idx]
            else:
                break
            idx = child_idx
        self._heap[idx] = temp

if __name__ == '__main__':
    heap = BinaryHeap()
    test = [1, 7, 6,5,6,8,0,2,10,9,11,4]
    heap.heapify(test)
    # test = [9,1,4,2,5,3,5,7,8]
    # heap.heapify(test)
    print(heap._heap)
    # print(heap.get_min())
    # heap.heappush([12,0,6])
    # print(heap._heap)
    # print(heap.get_min())
    # print(heap.heappop())