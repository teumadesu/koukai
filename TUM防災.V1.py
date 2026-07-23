import tkinter as tk
import requests

root = tk.Tk()
root.geometry("1920x1080")
root.title("TUM防災速報")

labels = []

# 列幅設定（これが表を揃える最重要部分）
root.grid_columnconfigure(0, weight=1)  # 時刻
root.grid_columnconfigure(1, weight=3)  # 震源地
root.grid_columnconfigure(2, weight=1)  # マグニチュード
root.grid_columnconfigure(3, weight=1)  # 震度
root.grid_columnconfigure(4, weight=3)  # 津波

# ===== ヘッダー（表のタイトル行）=====
headers = ["時刻", "震源地", "M", "震度", "津波"]

for col, text in enumerate(headers):
    lbl = tk.Label(
        root,
        text=text,
        font=("NK-R", 35, "bold"),
        bg="#222222",
        fg="white",
        anchor="w",
        padx=10,
        pady=5
    )
    lbl.grid(row=0, column=col, sticky="we")


def get_bg_color(shindo):
    colors = {
        "1": "#325A8C",
        "2": "#3278D2",
        "3": "#32D2E6",
        "4": "#FAFA8C",
        "5弱": "#FABE32",
        "5強": "#F1821E",
        "6弱": "#E61414",
        "6強": "#A01432",
        "7": "#5A1946"
    }
    return colors.get(shindo, "#46505A")


def henkan(shindo):
    table = {
        1.0: "1",
        2.0: "2",
        3.0: "3",
        4.0: "4",
        4.5: "5弱",
        5.0: "5強",
        5.5: "6弱",
        6.0: "6強",
        7.0: "7"
    }
    return table.get(shindo, "不明")


def update_data():

    # 古いラベル削除
    for lbl in labels:
        lbl.destroy()

    labels.clear()

    try:
        url = "https://api.p2pquake.net/v2/jma/quake"
        data = requests.get(url).json()

        for i, item in enumerate(data[:10]):  # 最大20件表示

            eq = item["earthquake"]

            # 津波情報
            tsunami = eq["domesticTsunami"]

            tsunami_map = {
                "None": "なし",
                "Checking": "調査中",
                "Watch": "注意報",
                "Warning": "避難！"
            }

            tsunamisinpai = tsunami_map.get(tsunami, "不明")

            # 震度
            shindo = eq['maxScale'] / 10
            shindo = henkan(shindo)

            bg = get_bg_color(shindo)

            row = i + 1

            # ===== 各列 =====

            values = [
                eq['time'][5:-3],
                eq['hypocenter']['name'],
                eq['hypocenter']['magnitude'],
                shindo,
                tsunamisinpai
            ]

            for col, value in enumerate(values):

                lbl = tk.Label(
                    root,
                    text=value,
                    font=("NK-R", 35),
                    bg=bg,
                    anchor="w",
                    padx=10,
                    pady=5
                )

                lbl.grid(
                    row=row,
                    column=col,
                    sticky="we"
                )

                labels.append(lbl)

    except Exception as e:
        print("更新エラー:", e)

    # 0.5秒後更新
    root.after(500, update_data)


update_data()

root.mainloop()
