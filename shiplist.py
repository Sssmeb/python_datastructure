# -*- coding: utf-8 -*-
# @Time    : 2019/11/17 21:17
# @Author  : CRJ
# @File    : shiplist.py
# @Software: PyCharm
# @Python3.6
import random


# class ListNode:
#     def __init__(self, key=None, value=None):
#         self._key = key
#         self._value = value
#         self._forwards = []

class ListNode:
    def __init__(self, data = None):
        self._data = data
        self._forwards = []   # 存放类似指针/引用的数组，占用空间很小


class SkipList:
    _MAX_LEVEL = 4

    def __init__(self):
        self._level_count = 1
        self._head = ListNode()
        self._head._forwards = [None] * self._MAX_LEVEL

    def insert(self, value):
        """
        插入一个元素

        :param value:
        :return: 已存在返回False 正常插入True
        """
        level = self._random_level()
        if self._level_count < level:
            self._level_count = level

        new_node = ListNode(value)
        new_node._forwards = [None] * level

        # 保存插入节点的左边的节点 ??? 这是干嘛
        update = [self._head] * level
        # 找到每一层需要插入索引的位置
        p = self._head
        for i in range(level-1, -1, -1):
            # 在同一层，找到小于等于当前节点的最后一个节点
            while p._forwards[i] and p._forwards[i]._data< value:
                p = p._forwards[i]
            if p._forwards[i] and p._forwards[i]._data==value:
                # 说明已存在，不需要再插入
                return False
            # 保存这个节点
            update[i] = p

        # 调整每层索引       a → c  添加新索引  a → b → c
        for i in range(level):
            new_node._forwards[i] = update[i]._forwards[i]
            update[i]._forwards[i] = new_node

        return True

    def delete(self, value):
        """
        删除一个元素  (插入的逆操作)

        :param value:
        :return: 如果不存在这个节点False 成功删除True
        """

        # 记录下每层索引可能受影响的节点
        update = [None] * self._level_count
        p = self._head
        for i in range(self._level_count-1, -1, -1):
            while p._forwards[i] and p._forwards[i]._data < value:
                p = p._forwards[i]
            update[i] = p

        # 检查每层的节点，如果存在要删除节点， 则删除
        # 此时p为最底层，如果不等的话，说明不存在这个节点
        if p._forwards[0] and p._forwards[0]._data==value:
            for i in range(self._level_count-1, -1, -1):
                if update[i]._forwards[i] and update[i]._forwards[i]._data == value:
                    update[i]._forwards[i] = update[i]._forwards[i]._forwards[i]
            return True

        else:
            return False

    def find(self, value):
        """
        查找单个元素，返回一个ListNode对象

        :param value:
        :return:
        """
        p = self._head
        for i in range(self._level_count - 1, -1, -1):
            while p._forwards[i] and p._forwards[i]._data < value:
                p = p._forwards[i]
            if p._forwards[i] and p._forwards[i]._data == value:
                return p._forwards[i]

        return None

    def find_range(self, begin_value, end_value):
        """
        查找一个范围内的元素，返回一组有序ListNode对象

        :param begin_value:
        :param end_value:
        :return:
        """
        p = self._head
        begin = None
        for i in range(self._level_count - 1, -1, -1):  # Move down a level
            while p._forwards[i] and p._forwards[i]._data < begin_value:
                p = p._forwards[i]  # Move along level
            if p._forwards[i] and p._forwards[i]._data >= begin_value:
                begin = p._forwards[i]

        if begin is None:
            return None  # 没有找到
        else:
            result = []
            while begin and begin._data <= end_value:
                result.append(begin)
                begin = begin._forwards[0]
            return result

    def _random_level(self, p=0.5):
        """
        返回随机层数

        :param p:
        :return:
        """
        level = 1
        while random.random()<p and level<self._MAX_LEVEL:
            level +=1
        return level
