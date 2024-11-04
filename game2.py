import tkinter as tk
import random

class SlotMachine:
    def __init__(self, master):
        self.master = master
        self.master.title("老虎机游戏")

        self.reels = ["🍒", "🍋", "🍊", "🍉", "⭐", "🍀"]

        self.label = tk.Label(master, text="欢迎来到老虎机游戏！", font=("Arial", 24))
        self.label.pack(pady=10)

        self.result_label = tk.Label(master, text="", font=("Arial", 48))
        self.result_label.pack(pady=20)

        self.bet_entry = tk.Entry(master, font=("Arial", 16))
        self.bet_entry.pack(pady=10)

        self.spin_button = tk.Button(master, text="旋转", font=("Arial", 16), command=self.spin)
        self.spin_button.pack(pady=10)

        self.output_label = tk.Label(master, text="", font=("Arial", 18))
        self.output_label.pack(pady=10)

    def spin(self):
        try:
            bet_amount = int(self.bet_entry.get())
            if bet_amount <= 0:
                self.output_label.config(text="请下注一个正数！")
                return
        except ValueError:
            self.output_label.config(text="无效的输入，请输入一个数字！")
            return

        self.output_label.config(text="")
        result = self.get_random_result()
        self.result_label.config(text=" | ".join(result))

        if self.check_win(result):
            winnings = bet_amount * 10
            self.output_label.config(text=f"恭喜你！你赢了 {winnings}！")
        else:
            self.output_label.config(text="很遗憾，你没有赢。")

    def get_random_result(self):
        return [random.choice(self.reels) for _ in range(3)]

    def check_win(self, result):
        return result[0] == result[1] == result[2]

if __name__ == "__main__":
    root = tk.Tk()
    slot_machine = SlotMachine(root)
    root.mainloop()