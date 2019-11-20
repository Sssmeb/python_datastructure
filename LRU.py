# -*- coding: utf-8 -*-
# @Time    : 2019/11/20 20:40
# @Author  : CRJ
# @File    : LRU.py
# @Software: PyCharm
# @Python3.6


class Node:
    """
    双向链表 结点
    """
    def __init__(self, data, pre=None, next=None):
        self.data = data
        self._pre = pre
        self._next = next

    def __str__(self):
        return str(self.data)


class DoublyLink:
    """
    双向链表

    仅关注于双向链表的操作，无关LRU。 （插入结点时 插入头）
    """
    def __init__(self):
        self.tail = None
        self.head = None
        self.size = 0

    def insert(self, data):
        if isinstance(data, Node):
            tmp_node = data
        else:
            tmp_node = Node(data)

        if self.size == 0:
            self.tail = tmp_node
            self.head = tmp_node
        else:
            # 插入从头插
            self.head._pre = tmp_node
            tmp_node._next = self.head
            self.head = tmp_node

        self.size += 1
        return tmp_node

    def remove(self, node):

        # 头节点和尾节点特殊处理
        if node == self.head:
            if self.size == 1:
                self.head = None
                self.tail = None
            else:
                self.head._next._pre = None
                self.head = self.head._next
        elif node == self.tail:
            self.tail._pre._next = None
            self.tail = self.tail._pre

        # 普通情况
        else:
            node._pre._next = node._next
            node._next._pre = node._pre

        self.size -= 1
        return True

    def __str__(self):
        str_text = ""
        cur_node = self.head

        while cur_node != None:
            str_text += str(cur_node) + " "
            cur_node = cur_node._next

        return str_text


class LRUCache:
    """
    LRU 经典实现

    字典 + 双向链表
    """
    def __init__(self, size):
        self.size = size
        self.hash_map = dict()
        self.link = DoublyLink()

    def set(self, key, value):
        """
        插入数据函数
        当数量已到达上限，先移除链表尾的结点，再插入新结点

        :param key:
        :param value:
        :return:
        """
        if key in self.hash_map:
            self.link.remove(self.hash_map.get(key))

        # 如果到达数量上限，先移除链表尾
        if self.size == self.link.size:
            self.link.remove(self.link.tail)

        tmp_node = self.link.insert(value)
        self.hash_map.__setitem__(key, tmp_node)

        return True

    def get(self, key):
        """
        获取对应的值，并将结点移至链表头

        具体操作是先删除结点，再插入头结点
        :param key:
        :return:
        """
        tmp_node = self.hash_map.get(key)
        if tmp_node is not None:
            self.link.remove(tmp_node)
            self.link.insert(tmp_node)
            return tmp_node.data
        else:
            return None


if __name__ == '__main__':
    lru = LRUCache(5)

    import random
    for _ in range(7):
        data = random.randint(0, 9)
        lru.set(data, data)
        print("set: ", data, "      res: ", lru.link)

    print("*"*20)

    for _ in range(10):
        data = random.randint(0, 9)
        lru.get(data)
        print("get: ", data, "      res: ", lru.link)