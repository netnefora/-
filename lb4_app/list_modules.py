import ctypes
import os
import platform

class BaseList:
    def push_front(self, value): pass
    def push_back(self, value): pass
    def insert_at(self, index, value): pass
    def delete_at(self, index): pass
    def clear(self): pass
    def get_count(self): pass
    def get_all(self): pass

# --- 1. Базовый модуль Python ---
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class PythonLinkedList(BaseList):
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def push_front(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.count += 1

    def push_back(self, value):
        new_node = Node(value)
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.count += 1

    def insert_at(self, index, value):
        if index < 0 or index > self.count: raise IndexError("Неверный индекс")
        if index == 0:
            self.push_front(value)
            return
        if index == self.count:
            self.push_back(value)
            return
        new_node = Node(value)
        curr = self.head
        for _ in range(index - 1): curr = curr.next
        new_node.prev = curr
        new_node.next = curr.next
        curr.next.prev = new_node
        curr.next = new_node
        self.count += 1

    def delete_at(self, index):
        if self.count == 0: raise IndexError("Список пуст")
        if index < 0 or index >= self.count: raise IndexError("Неверный индекс")
        if index == 0:
            self.head = self.head.next
            if self.head: self.head.prev = None
            else: self.tail = None
        elif index == self.count - 1:
            self.tail = self.tail.prev
            if self.tail: self.tail.next = None
            else: self.head = None
        else:
            curr = self.head
            for _ in range(index): curr = curr.next
            curr.prev.next = curr.next
            curr.next.prev = curr.prev
        self.count -= 1

    def clear(self):
        self.head = None
        self.tail = None
        self.count = 0

    def get_count(self): return self.count

    def get_all(self):
        res, curr = [], self.head
        while curr:
            res.append(curr.data)
            curr = curr.next
        return res

# Базовый модуль C++ ---
class CppLinkedList(BaseList):
    def __init__(self, lib_name="cpp_dyn"):
        ext = ".dll" if platform.system() == "Windows" else ".so"
        current_dir = os.path.abspath(os.path.dirname(__file__))
        lib_path = os.path.join(current_dir, lib_name + ext)
        
        #Проверяем, существует ли файл ФИЗИЧЕСКИ на диске
        if not os.path.exists(lib_path):
            raise FileNotFoundError(f"Файла нет в папке!\nПуть, где я его искал:\n{lib_path}")
        try:
            if hasattr(os, 'add_dll_directory'):
                os.add_dll_directory(current_dir)
            
            self.lib = ctypes.cdll.LoadLibrary(lib_path)
            
        except OSError as e:
            raise FileNotFoundError(f"Файла нет в папке!\nПуть, где я его искал:\n{lib_path}")

        self.lib.create_list.restype = ctypes.c_void_p
        self.obj = self.lib.create_list()

    def __del__(self):
        if hasattr(self, 'lib') and hasattr(self, 'obj') and self.obj:
            self.lib.destroy_list(ctypes.c_void_p(self.obj))

    def push_front(self, value): self.lib.push_front(ctypes.c_void_p(self.obj), ctypes.c_int(value))
    def push_back(self, value): self.lib.push_back(ctypes.c_void_p(self.obj), ctypes.c_int(value))

    def insert_at(self, index, value):
        res = self.lib.insert_at(ctypes.c_void_p(self.obj), ctypes.c_int(index), ctypes.c_int(value))
        if res == -1: raise IndexError("Неверный индекс")

    def delete_at(self, index):
        res = self.lib.delete_at(ctypes.c_void_p(self.obj), ctypes.c_int(index))
        if res == -1: raise IndexError("Список пуст или неверный индекс")

    def clear(self): self.lib.clear_list(ctypes.c_void_p(self.obj))
    def get_count(self): return self.lib.get_count(ctypes.c_void_p(self.obj))
    
    def get_all(self):
        count = self.get_count()
        return [self.lib.get_element_at(ctypes.c_void_p(self.obj), i) for i in range(count)]