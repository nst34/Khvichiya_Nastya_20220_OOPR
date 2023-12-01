import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from datetime import datetime
import csv


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        weight = 600
        #height = 450
        self.error_dt = 0
        self.sum_money = 0

        self.lst = list()

        self.title("Учет расходов")
        self.geometry('600x450')
        self.resizable(False, False)

        main_menu = tk.Menu(self)
        self.config(menu=main_menu)
        file_menu = tk.Menu(main_menu)
        main_menu.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Сохранить", command=self.save_file)
        file_menu.add_command(label="Загрузить", command=self.open_file)

        self.dmy = tk.Label(self, text="Дата (ДД.ММ.ГГГГ):")
        self.dmy.grid(row=1, column=0)
        self.dmy_entry = tk.Entry(width=22)
        self.dmy_entry.grid(row=1, column=1)

        self.category = tk.Label(text="Категория:")
        self.category.grid(row=2, column=0)

        self.category_entry = ttk.Combobox()
        self.category_entry.grid(row=2, column=1)
        self.category_entry.bind('<KeyRelease>', self.check_input)
        self.category_entry.bind("<<ComboboxSelected>>", self.selected)

        self.money = tk.Label(text="Деньги:")
        vcmd = self.register(self.validate)
        self.money_entry = tk.Entry(validate="key", validatecommand=(vcmd, '%P'), width=22)
        self.money.grid(row=3, column=0)
        self.money_entry.grid(row=3, column=1)

        self.add_button = ttk.Button(self, text="Добавить", command=self.add_params)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=20)

        self.total_amount = tk.Label(text=f"Общая сумма расходов:{'  ' * 25}{self.sum_money}")
        self.total_amount.grid(row=7, columnspan=2)

        self.scrollbar = ttk.Scrollbar(self, orient="vertical")
        self.scrollbar.grid(row=5, column=4, sticky="ns")

        self.tree = ttk.Treeview(self, columns=("Date", "Category", "Sum"), yscrollcommand=self.scrollbar.set,
                                 show="headings", selectmode="extended")
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Category", text="Категория",
                          command=lambda: self.treeview_sort_column(self.tree, "Category", True))
        self.tree.heading("Sum", text="Сумма",
                          command=lambda: self.treeview_sort_column(self.tree, "Sum", True, key=int))

        self.tree.column("Date", width=weight // 3)
        self.tree.column("Category", width=weight // 3)
        self.tree.column("Sum", width=weight // 3)
        self.tree.grid(row=5, columnspan=3, sticky="nsew")

        self.scrollbar.config(command=self.tree.yview)

        self.delete_button = ttk.Button(self, text="Удалить выбранную строку", command=self.delete_selected)
        self.delete_button.grid(row=6, column=0, columnspan=2, pady=20)

        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def delete_selected(self):
        selected_items = self.tree.selection()
        for item in selected_items:
            for i in [self.tree.item(item, option="values")]:
                if i[1] in self.lst:
                    self.lst.remove(i[1])
                self.sum_money -= int(i[2])
            self.total_amount.destroy()
            self.total_amount = tk.Label(text=f"Общая сумма расходов:{'  ' * 25}{self.sum_money}")
            self.total_amount.grid(row=7, columnspan=2)
            self.tree.delete(item)
        for item in self.tree.get_children():
            for i in [self.tree.item(item, option="values")]:
                if i[1] not in self.lst:
                    self.lst.append(i[1])
        self.category_entry['values'] = self.lst

    def validate(self, new_text: str):
        if not new_text:
            return True
        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False

    def check_date(self):
        date = list(map(int, self.dmy_entry.get().split('.')))
        try:
            datetime.fromisoformat(f"{date[2]}-{date[1]:02}-{date[0]:02}")
        except Exception as ex:
            print(ex)
            return True
        else:
            return False

    def check_input(self, event):
        value = event.widget.get()
        if value == '':
            self.category_entry['values'] = self.lst
        else:
            data = []
            for item in self.lst:
                if item.lower().startswith(value.lower()):
                    data.append(item)

            self.category_entry['values'] = data

    def selected(self, event):
        selection = event.widget.get()
        self.category_entry.set(selection)
        self.check_input(event)

    def treeview_sort_column(self, tv, col, reverse, key=str):
        l = [(tv.set(k, col), k) for k in tv.get_children()]
        l.sort(reverse=reverse, key=lambda t: key(t[0]))

        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse, key=key))

    def open_file(self):
        filepath = askopenfilename(
            filetypes=[("CSV Files", "*.csv")]
        )
        if not filepath:
            return
        self.total_amount.destroy()
        self.sum_money = 0
        self.category_entry.set('')
        self.lst = []
        for item in self.tree.get_children():
            self.tree.delete(item)
        with open(filepath, mode="r", encoding="utf-8") as input_file:
            reader = csv.DictReader(input_file, delimiter=',')

            for row in reader:
                Date = row['Date']
                Category = row['Category']
                Sum = row['Sum']
                self.tree.insert("", 0, values=(Date, Category, Sum))
        self.total_amount.destroy()
        for item in self.tree.get_children():
            for i in [self.tree.item(item, option="values")]:
                self.sum_money += int(i[2])
                if i[1] not in self.lst:
                    self.lst.append(i[1])

        self.total_amount = tk.Label(text=f"Общая сумма расходов:{'  ' * 25}{self.sum_money}")
        self.total_amount.grid(row=7, columnspan=2)
        self.category_entry['values'] = self.lst
        print("Таблица была успешно загружена", self.lst)

    def save_file(self):
        filepath = asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
        )
        if not filepath:
            return
        with open(filepath, mode="w", encoding="utf-8") as output_file:
            fieldnames = ["Date", "Category", "Sum"]
            writer = csv.DictWriter(output_file, fieldnames=fieldnames, delimiter=',')
            writer.writeheader()
            for row_id, row_item in enumerate(self.tree.get_children(), 1):
                row = self.tree.item(row_item)['values']
                writer.writerow({"Date": row[0], "Category": row[1], "Sum": row[2]})
                print(f'Cтрока №{row_id} была сохранена:', row)

    def add_params(self):
        if self.dmy_entry.get() and self.category_entry.get() and self.money_entry.get():
            if self.check_date():
                self.error_input = tk.Label(self, text="Введите дату согласно примеру")
                self.total_amount.destroy()
                self.error_input.grid(row=7, columnspan=2)
                self.error_dt = 1

            elif not (self.check_date()):
                self.tree.insert("", tk.END,
                                 values=(self.dmy_entry.get(), self.category_entry.get(), self.money_entry.get()))
                self.total_amount.destroy()
                if self.category_entry.get() not in self.lst:
                    self.lst.append(self.category_entry.get())
                self.sum_money += int(self.money_entry.get())
                self.total_amount = tk.Label(text=f"Общая сумма расходов:{'  ' * 25}{self.sum_money}")
                self.total_amount.grid(row=7, columnspan=2)
                self.dmy_entry.delete(0, tk.END)
                self.category_entry.delete(0, tk.END)
                self.money_entry.delete(0, tk.END)
                if self.error_dt:
                    self.error_input.destroy()
                    self.error_dt = 0
                self.category_entry['values'] = self.lst


if __name__ == "__main__":
    app = App()
    app.mainloop()
