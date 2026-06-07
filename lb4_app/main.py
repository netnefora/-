import tkinter as tk
from tkinter import messagebox
import random
from list_modules import PythonLinkedList, CppLinkedList

class LinkedListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Двусвязный список")
        self.root.geometry("950x600")
        
        # Основные цвета минимализма
        self.bg_color = "#ffffff"  # Чистый белый фон
        self.fg_color = "#000000"  # Черный текст
        self.gray_color = "#888888" # Серый для второстепенных элементов
        
        self.root.configure(bg=self.bg_color)

        self.list_obj = None
        self.init_ui()
        self.change_implementation()

    def init_ui(self):
        main_font = ("Segoe UI", 10)
        title_font = ("Segoe UI", 10, "bold")

        # --- Верхняя панель (выбор модуля) ---
        top_frame = tk.Frame(self.root, bg=self.bg_color, pady=15)
        top_frame.pack(fill=tk.X, padx=20)
        
        tk.Label(top_frame, text="Модуль:", bg=self.bg_color, fg=self.fg_color, font=title_font).pack(side=tk.LEFT)
        
        self.module_var = tk.StringVar(value="python")
        
        rb_style = {
            "bg": self.bg_color, "fg": self.gray_color, 
            "selectcolor": self.bg_color, "activebackground": self.bg_color, 
            "activeforeground": self.fg_color, "font": main_font, "cursor": "hand2",
            "bd": 0, "highlightthickness": 0
        }
        tk.Radiobutton(top_frame, text="Python", variable=self.module_var, value="python", command=self.change_implementation, **rb_style).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(top_frame, text="C++ (Dynamic)", variable=self.module_var, value="cpp_dyn", command=self.change_implementation, **rb_style).pack(side=tk.LEFT, padx=10)

        # Тонкая линия-разделитель
        tk.Frame(self.root, height=1, bg="#e0e0e0").pack(fill=tk.X)

        # --- Левая панель (Управление) ---
        control_frame = tk.Frame(self.root, width=250, bg=self.bg_color, padx=20, pady=20)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        lbl_style = {"bg": self.bg_color, "fg": self.gray_color, "font": ("Segoe UI", 9)}
        entry_style = {
            "font": main_font, "relief": tk.SOLID, "bd": 1, 
            "bg": self.bg_color, "fg": self.fg_color, 
            "highlightthickness": 0, "insertbackground": self.fg_color
        }
        
        tk.Label(control_frame, text="Значение", **lbl_style).pack(anchor=tk.W)
        self.entry_val = tk.Entry(control_frame, **entry_style)
        self.entry_val.pack(fill=tk.X, pady=(2, 15), ipady=4)

        tk.Label(control_frame, text="Индекс", **lbl_style).pack(anchor=tk.W)
        self.entry_idx = tk.Entry(control_frame, **entry_style)
        self.entry_idx.pack(fill=tk.X, pady=(2, 25), ipady=4)

        # Минималистичные кнопки
        def create_btn(parent, text, command):
            return tk.Button(parent, text=text, command=command, bg=self.bg_color, fg=self.fg_color, 
                             font=main_font, relief=tk.SOLID, bd=1, cursor="hand2", 
                             activebackground="#f5f5f5", activeforeground=self.fg_color, pady=4)

        create_btn(control_frame, "Вставить в начало", self.cmd_push_front).pack(fill=tk.X, pady=4)
        create_btn(control_frame, "Вставить в конец", self.cmd_push_back).pack(fill=tk.X, pady=4)
        create_btn(control_frame, "Вставить по индексу", self.cmd_insert).pack(fill=tk.X, pady=4)
        create_btn(control_frame, "Удалить по индексу", self.cmd_delete).pack(fill=tk.X, pady=4)
        
        tk.Frame(control_frame, height=1, bg="#e0e0e0").pack(fill=tk.X, pady=15)
        
        create_btn(control_frame, "Очистить", self.cmd_clear).pack(fill=tk.X, pady=4)
        create_btn(control_frame, "Случайные", self.cmd_random).pack(fill=tk.X, pady=4)

        self.lbl_info = tk.Label(control_frame, text="count: 0", bg=self.bg_color, fg=self.gray_color, font=("Consolas", 10), pady=20)
        self.lbl_info.pack(side=tk.BOTTOM, anchor=tk.W)

        # Тонкая линия-разделитель (вертикальная)
        tk.Frame(self.root, width=1, bg="#e0e0e0").pack(side=tk.LEFT, fill=tk.Y)

        # --- Правая панель (Визуализация) ---
        self.canvas = tk.Canvas(self.root, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

    def change_implementation(self):
        mode = self.module_var.get()
        try:
            if mode == "python":
                self.list_obj = PythonLinkedList()
            elif mode == "cpp_dyn":
                self.list_obj = CppLinkedList("cpp_dyn")
            self.update_visualization()
        except Exception as e:
            messagebox.showerror("Ошибка окружения", str(e))
            self.module_var.set("python")
            self.list_obj = PythonLinkedList()

    def get_value(self):
        try: return int(self.entry_val.get())
        except ValueError: raise ValueError("Введите числовое значение")

    def get_index(self):
        try: return int(self.entry_idx.get())
        except ValueError: raise ValueError("Введите числовой индекс")

    def safe_execute(self, func):
        try:
            func()
            self.update_visualization()
        except ValueError as e: messagebox.showwarning("Внимание", str(e))
        except IndexError as e: messagebox.showerror("Ошибка", str(e))
        except Exception as e: messagebox.showerror("Ошибка", str(e))

    def cmd_push_front(self): self.safe_execute(lambda: self.list_obj.push_front(self.get_value()))
    def cmd_push_back(self): self.safe_execute(lambda: self.list_obj.push_back(self.get_value()))
    def cmd_insert(self): self.safe_execute(lambda: self.list_obj.insert_at(self.get_index(), self.get_value()))
    def cmd_delete(self): self.safe_execute(lambda: self.list_obj.delete_at(self.get_index()))
    def cmd_clear(self): self.safe_execute(lambda: self.list_obj.clear())
    
    def cmd_random(self):
        def fill():
            for _ in range(int(self.entry_val.get())): self.list_obj.push_back(random.randint(10, int(self.entry_idx.get())))
        self.safe_execute(fill)

    def update_visualization(self):
        self.canvas.delete("all")
        if not self.list_obj: return

        count = self.list_obj.get_count()
        self.lbl_info.config(text=f"count: {count}")

        if count == 0:
            self.canvas.create_text(300, 200, text="empty", font=("Consolas", 14), fill=self.gray_color)
            return

        elements = self.list_obj.get_all()
        x_start, y_start = 30, 50
        box_w, box_h = 50, 50
        x_gap = 40 
        x, y = x_start, y_start

        for i, val in enumerate(elements):
            if x + box_w + x_gap > self.canvas.winfo_width() and self.canvas.winfo_width() > 100:
                x = x_start
                y += box_h + 50

            # Минималистичный прямоугольник (без заливки, только тонкая черная рамка)
            self.canvas.create_rectangle(x, y, x + box_w, y + box_h, fill=self.bg_color, outline=self.fg_color, width=1)
            
            # Текст значения
            self.canvas.create_text(x + box_w/2, y + box_h/2, text=str(val), font=("Segoe UI", 12), fill=self.fg_color)
            
            # Индекс (мелкий, снизу)
            self.canvas.create_text(x + box_w/2, y + box_h + 12, text=str(i), font=("Consolas", 8), fill=self.gray_color)

            # Отрисовка стрелок (тонкая черная линия с двумя концами)
            if i < count - 1:
                if x + box_w * 2 + x_gap * 2 <= self.canvas.winfo_width():
                    arr_x_start = x + box_w
                    arr_x_end = arr_x_start + x_gap
                    arr_y = y + box_h/2
                    
                    self.canvas.create_line(arr_x_start, arr_y, arr_x_end, arr_y, arrow=tk.BOTH, fill=self.fg_color, width=1)

            x += box_w + x_gap

if __name__ == "__main__":
    root = tk.Tk()
    app = LinkedListApp(root)
    root.mainloop()
