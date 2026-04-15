import tkinter as tk
from tkinter import filedialog

# костыль номер раз: словарик для маппинга системных имен виджетов (типа .!frame.!entry) в человеческие
widget_names = {}

def save_file(event=None):
    # забираем текст из текстового поля (задание 5.1)
    text = text_area.get("1.0", tk.END)
    # открываем диалог сохранения
    filepath = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("текстовые файлы", "*.txt"), ("все файлы", "*.*")]
    )
    if filepath:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)
        print("успех: файл сохранен в", filepath)

def close_app(event=None):
    # жестко рубим окно по эскейпу
    root.destroy()

def on_left_click(event):
    # достаем имя из словаря, если его там нет — кидаем дефолт (задание 5.2)
    name = widget_names.get(str(event.widget), "неизвестное поле")
    lbl_active_field.config(text=f"активное поле: {name}")

def on_right_click(event):
    # вывод в консоль по правому клику
    name = widget_names.get(str(event.widget), "неизвестное поле")
    print(f"правый клик прилетел в: {name}")

def on_mouse_move(event):
    # обновляем метку координатами x и y (задание 5.3)
    lbl_mouse.config(text=f"координаты мыши: x={event.x}, y={event.y}")

def on_key_press(event):
    # фильтруем мусорные нажатия типа shift или стрелочек (задание 5.4)
    if event.char and event.keysym not in ['Escape', 'BackSpace', 'Return', 'Tab']:
        current = lbl_keys.cget("text")
        # если строка разрослась, рубим начало, чтобы не растягивать окно
        if len(current) > 60:
            current = "нажатые клавиши: ..." + current[30:]
        lbl_keys.config(text=current + event.char)


# собираем интерфейс
root = tk.Tk()
root.title("практическая работа №15 — монохромная имитация")
root.geometry("800x600")
root.configure(bg="#e5e5e5") # серый фон как в прошлой лабе

# костыль номер два: мы биндим события через bind_all, 
# чтобы они отслеживались вообще везде, независимо от того, над каким элементом мышка
root.bind_all("<Control-s>", save_file)
root.bind_all("<Control-S>", save_file) # ловим капс или русскую раскладку
root.bind_all("<Escape>", close_app)
root.bind_all("<Motion>", on_mouse_move)
root.bind_all("<Key>", on_key_press)

# делаем карточку, чтобы визуально сымитировать html-версию из прошлого задания
card = tk.Frame(root, bg="#ffffff", padx=30, pady=30)
card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=500, height=520)

# 5.1 многострочное поле и кнопка
tk.Label(card, text="задание 5.1 (сохранение текста)", bg="#ffffff", fg="#666666", font=("Arial", 9, "bold")).pack(anchor="w")
text_area = tk.Text(card, height=6, bg="#fafafa", fg="#1a1a1a", relief="flat", highlightbackground="#cccccc", highlightthickness=1)
text_area.pack(fill=tk.X, pady=(5, 10))

btn_save = tk.Button(card, text="сохранить", bg="#1a1a1a", fg="#ffffff", relief="flat", command=save_file)
btn_save.pack(fill=tk.X, pady=(0, 20))

# 5.2 три поля ввода
tk.Label(card, text="задание 5.2 (клики по полям)", bg="#ffffff", fg="#666666", font=("Arial", 9, "bold")).pack(anchor="w")
entries_frame = tk.Frame(card, bg="#ffffff")
entries_frame.pack(fill=tk.X, pady=(5, 10))

# создаем поля ввода
entry1 = tk.Entry(entries_frame, bg="#fafafa", relief="flat", highlightbackground="#cccccc", highlightthickness=1)
entry1.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

entry2 = tk.Entry(entries_frame, bg="#fafafa", relief="flat", highlightbackground="#cccccc", highlightthickness=1)
entry2.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

entry3 = tk.Entry(entries_frame, bg="#fafafa", relief="flat", highlightbackground="#cccccc", highlightthickness=1)
entry3.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

# заполняем словарь маппинга (str(widget) возвращает внутреннее имя ткинтера)
widget_names[str(entry1)] = "левое поле"
widget_names[str(entry2)] = "центральное поле"
widget_names[str(entry3)] = "правое поле"

# подписка на события класса (как жестко просили в задании)
root.bind_class("Entry", "<Button-1>", on_left_click)
root.bind_class("Entry", "<Button-3>", on_right_click) # правый клик windows/linux
root.bind_class("Entry", "<Button-2>", on_right_click) # правый клик macos (на всякий случай)

lbl_active_field = tk.Label(card, text="активное поле: пока не кликали", bg="#f5f5f5", fg="#1a1a1a", pady=8)
lbl_active_field.pack(fill=tk.X, pady=(0, 20))

# 5.3 координаты мыши
tk.Label(card, text="задание 5.3 (движение мыши)", bg="#ffffff", fg="#666666", font=("Arial", 9, "bold")).pack(anchor="w")
lbl_mouse = tk.Label(card, text="координаты мыши: x=0, y=0", bg="#f5f5f5", fg="#1a1a1a", pady=8)
lbl_mouse.pack(fill=tk.X, pady=(5, 20))

# 5.4 нажатые клавиши
tk.Label(card, text="задание 5.4 (клавиатура)", bg="#ffffff", fg="#666666", font=("Arial", 9, "bold")).pack(anchor="w")
lbl_keys = tk.Label(card, text="нажатые клавиши: ", bg="#f5f5f5", fg="#1a1a1a", pady=8)
lbl_keys.pack(fill=tk.X, pady=(5, 0))

root.mainloop()
