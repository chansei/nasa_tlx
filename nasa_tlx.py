# NASA-TLXのプロトタイプ
# 2023/10/30 @Chansei

VERSION = "1.1"

import csv
import logging
import random
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

import customtkinter as ctk

import cal_tlx_score as score  # スコア計算

scales = [
    "精神的欲求", "身体的要求", "時間切迫感", "作業達成度", "努力", "不満"
]

descriptions = [
    "【精神的欲求】\nどの程度，精神的かつ知覚的活動が要求されましたか？（例．思考，意志決定，計算，記憶，観察，検索，等）作業は容易でしたか，それとも困難でしたか．単純でしたか，それとも複雑でしたか．苛酷でしたか，それとも寛大でしたか．",
    "【身体的要求】\nどの程度，身体的活動が必要でしたか？（例．押す，引く，回す， 操作する等）　作業は容易でしたか，それとも困難でしたか．ゆっくりしていましたか，それともきびきびしていましたか．ゆるやかでしたか，それとも努力を要するものでしたか．落ち着いたものでしたか，それとも骨の折れるものでしたか．",
    "【時間切迫感】\n作業や要素作業の頻度や速さにどの程度，時間的圧迫感を感じましたか？　作業ペースはゆっくりしていて暇でしたか，それとも急速で大変でしたか．",
    "【作業達成度】\n実験者（あるいは，あなた自身）によって設定された作業の達成目標の遂行について，どの程度成功したと思いますか？　この目標達成における作業成績にどのくらい満足していますか？",
    "【努力】\nあなたの作業達成レベルに到達するのにどのくらい一生懸命（精神的および身体的に）作業を行わなければなりませんでしたか？",
    "【不満】\n作業中，どのくらい，不安，落胆，いらいら，ストレス，不快感，あるいは安心，喜び，満足，リラックス，自己満足を感じましたか？"
]

current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_filename = f'nasa_tlx_{current_time}.log'
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')
logger = logging.getLogger()

class NASATLXApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"NASA-TLX(v{VERSION})")
        # self.iconbitmap('icon.ico')
        self.geometry("1920x1080")
        # self.attributes("-fullscreen", 1)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # 上部フレームの設定
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="both", pady=15, padx=15)
        top_frame.grid_columnconfigure(1, weight=1)

        self.participant_label = ctk.CTkLabel(top_frame, text="被験者名:", font=("Meiryo", 12))
        self.participant_label.grid(row=0, column=0, padx=20, pady=10)
        self.participant_entry = ctk.CTkEntry(top_frame)
        self.participant_entry.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

        self.task_label = ctk.CTkLabel(top_frame, text="タスク数:", font=("Meiryo", 12))
        self.task_label.grid(row=0, column=2, padx=20, pady=10)
        self.task_entry = ctk.CTkEntry(top_frame)
        self.task_entry.grid(row=0, column=3, padx=20, pady=10, sticky="ew")

        self.tlx_slider_show_button = ctk.CTkButton(top_frame, text="設定", font=("Meiryo", 12), command=self.check_input)
        self.tlx_slider_show_button.grid(row=1, column=4, padx=20, pady=10)

        # 下部のフレームの設定
        self.bottom_frame = None

        # 1対比較の設定
        self.scale_pairs = []
        for i in range(len(scales)):
            for j in range(i+1, len(scales)):
                self.scale_pairs.append((scales[i], scales[j]))
        random.shuffle(self.scale_pairs)
        self.current_pair_idx = 0

        # 結果の保存
        self.slider_results = {}
        self.comparisons = []

        # タスク数の管理
        self.current_task = 1
    
    # 一対比較
    def check_input(self):
        try:
            if self.participant_entry.get() == "":
                logger.warning("被験者名が入力されていません")
                messagebox.showerror("エラー", "被験者名を入力してください")
                return
            if self.task_entry.get() == "":
                logger.warning("タスク数が入力されていません")
                messagebox.showerror("エラー", "タスク数を入力してください")
                return
            if not self.task_entry.get().isdecimal():
                logger.warning("タスク数が数字ではありません")
                messagebox.showerror("エラー", "タスク数は数字で入力してください")
                return
            
            # 設定欄の無効化
            self.participant_entry.configure(state='disabled')
            self.task_entry.configure(state='disabled')
            self.tlx_slider_show_button.configure(state='disabled')

            # CSVファイルの作成
            with open(f"{self.participant_entry.get()}_result.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["task_number"] + scales + ["overall_score"])
            with open(f"{self.participant_entry.get()}_compare.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["option1", "option2", "selected_index"])

            # 一対比較へ
            self.tlx_compare()

        except Exception as e:
            logger.error(f"check_input:{str(e)}")
            raise

    def tlx_compare(self):
        if self.bottom_frame:
            self.bottom_frame.destroy()
        self.bottom_frame = ctk.CTkFrame(self)
        # 上下左右いっぱいに広げる
        self.bottom_frame.pack(fill="both", expand=True, pady=15, padx=15)
        for idx in range(3):
            self.bottom_frame.grid_rowconfigure(idx, weight=1)
        self.bottom_frame.grid_columnconfigure(1, weight=1)
        self.display_pair(self.current_pair_idx)
    
    def display_pair(self, idx):
        scale1, scale2 = self.scale_pairs[idx]

        label = ctk.CTkLabel(self.bottom_frame, text="次の2つの項目のうち、作業負荷に関わりが深いと感じる方にチェックをつけてください", font=("Meiryo", 20))
        label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.var = tk.IntVar()
        self.var.set(0)
        radio1 = ctk.CTkRadioButton(self.bottom_frame, text=scale1, variable=self.var, value=1, font=("Meiryo", 20), height=250, command=lambda: self.next_pair([scale1, scale2]))
        radio1.grid(row=1, column=0, padx=10, pady=10, sticky="ns")
        desc1 = ctk.CTkLabel(self.bottom_frame, text=descriptions[scales.index(scale1)], wraplength=800, font=("Meiryo", 20))
        desc1.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        radio2 = ctk.CTkRadioButton(self.bottom_frame, text=scale2, variable=self.var, value=2, font=("Meiryo", 20), height=250, command=lambda: self.next_pair([scale1, scale2]))
        radio2.grid(row=2, column=0, padx=10, pady=10, sticky="ns")
        desc2 = ctk.CTkLabel(self.bottom_frame, text=descriptions[scales.index(scale2)], wraplength=800, font=("Meiryo", 20))
        desc2.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        progress = (self.current_pair_idx + 1) / len(self.scale_pairs)
        self.progress_bar = ctk.CTkProgressBar(self.bottom_frame)
        self.progress_bar.grid(row=3, column=0, columnspan=3, pady=20, sticky="ew")
        self.progress_bar.set(progress)
    
    def next_pair(self, scale_pair):
        logger.info([scale_pair[0], scale_pair[1], self.var.get()])
        self.comparisons.append([scale_pair[0], scale_pair[1], self.var.get()])

        self.current_pair_idx += 1
        if self.current_pair_idx < len(self.scale_pairs):
            self.tlx_compare()
        else:
            # 一対比較の結果を保存
            with open(f"{self.participant_entry.get()}_compare.csv", "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                for comparison in self.comparisons:
                    writer.writerow(comparison)
            self.tlx_slider()
    
    # 尺度評価
    def tlx_slider(self):
        # タスク番号/タスク数をタイトルに表示
        self.title(f"NASA-TLXアンケート【{self.current_task}/{self.task_entry.get()}タスク目】")

        if self.bottom_frame:
            self.bottom_frame.destroy()
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.pack(fill="both", expand=True, pady=15, padx=15)
        for idx in range(13):
            self.bottom_frame.grid_rowconfigure(idx, weight=1)
        self.bottom_frame.grid_columnconfigure(1, weight=1)

        sliders = []
        for idx, scale in enumerate(scales):
            scale_label = ctk.CTkLabel(self.bottom_frame, text=scale, font=("Meiryo", 20))
            scale_label.grid(row=idx*2, column=0, padx=10, pady=0)
            scale_description = ctk.CTkLabel(self.bottom_frame, text=descriptions[idx], wraplength=1600, font=("Meiryo", 12))
            scale_description.grid(row=idx*2, column=1, padx=10, pady=0, sticky="nsew")
            _label = ctk.CTkLabel(self.bottom_frame, text="低い", font=("Meiryo", 12))
            _label.grid(row=idx*2+1, column=0, padx=10, pady=0)
            sliders.append(ctk.CTkSlider(self.bottom_frame, height=20, from_=0))
            sliders[idx].grid(row=idx*2+1, column=1, padx=10, pady=0, sticky="ew")
            _label = ctk.CTkLabel(self.bottom_frame, text="高い", font=("Meiryo", 12))
            _label.grid(row=idx*2+1, column=3, padx=10, pady=0)
        
        self.tlx_compare_show_button = ctk.CTkButton(self.bottom_frame, text="完了", font=("Meiryo", 12), command=lambda: self.next_task(sliders))
        self.tlx_compare_show_button.grid(row=12, column=3, padx=20, pady=10)

    def next_task(self, sliders):
        # スコアを計算
        logger.info(self.comparisons)
        slider_results = [[scale, slider.get()] for scale, slider in zip(scales, sliders)]
        logger.info(slider_results)

        tlx_score = score.tlx_score(self.comparisons, slider_results)
        overall_score = tlx_score.compute_overall_workload()
        logger.info(overall_score)

        # 結果を保存
        with open(f"{self.participant_entry.get()}_result.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([self.current_task] + [slider.get() for slider in sliders] + [overall_score])

        if self.bottom_frame:
            self.bottom_frame.destroy()
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.pack(fill="both", expand=True, pady=15, padx=15)
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_rowconfigure(0, weight=1)

        # タスク数が終わったら終了
        self.current_task += 1
        self.current_pair_idx = 0

        if self.current_task > int(self.task_entry.get()):
            self.tlx_next_task_button = ctk.CTkButton(self.bottom_frame, text="終了", font=("Meiryo", 12), command=self.tlx_finish)
            self.tlx_next_task_button.grid(row=0, column=0, padx=20, pady=10)
        else:
            self.tlx_next_task_button = ctk.CTkButton(self.bottom_frame, text="次のタスクへ", font=("Meiryo", 12), command=self.tlx_slider)
            self.tlx_next_task_button.grid(row=0, column=0, padx=20, pady=10)
    
    def tlx_finish(self):
        self.destroy()

if __name__ == "__main__":
    print(f"NASA-TLX(v{VERSION})")
    print("2021/10/31 @Chansei")
    try:
        app = NASATLXApp()
        app.mainloop()
    except Exception as e:
        logger.error(f"main:{str(e)}")
        raise