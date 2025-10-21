import tkinter as tk
from tkinter import ttk
import requests

# =================== CẤU HÌNH ===================
TOKEN_ADDRESS_ETH = "0xfd9a3f94bec6b08711d90ff69cbba42fac96b45a"      # CORL token ETH
LEADING_WALLETS = [
    "0x30a018455a8c6f9a50a6e89d01a6f0adfb167d2e"
]

ETHERSCAN_API_KEY = "AM2DBRIY6GUACJYY478MP1NQMBE7B6HYB1"

# =================== HÀM LẤY GIAO DỊCH ===================
def get_transactions():
    url = f"https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={TOKEN_ADDRESS_ETH}&sort=desc&apikey={ETHERSCAN_API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data['status'] == '1':
            txs = data['result']
            filtered = []
            for tx in txs[:50]:  # Lấy 50 giao dịch gần nhất
                frm = tx.get('from','').lower()
                to = tx.get('to','').lower()
                value = int(tx.get('value','0')) / 10**18
                if frm.lower() in [w.lower() for w in LEADING_WALLETS] or to.lower() in [w.lower() for w in LEADING_WALLETS]:
                    filtered.append({'from': frm, 'to': to, 'value': value})
            return filtered
        else:
            return []
    except Exception as e:
        print("Lỗi API:", e)
        return []

# =================== HÀM CẬP NHẬT GUI ===================
def update_table():
    transactions = get_transactions()
    for row in tree.get_children():
        tree.delete(row)
    action = "HOLD"
    for tx in transactions:
        tree.insert("", "end", values=(tx['from'], tx['to'], f"{tx['value']:.4f}"))
        if tx['from'].lower() in [w.lower() for w in LEADING_WALLETS]:
            action = "SELL"
        elif tx['to'].lower() in [w.lower() for w in LEADING_WALLETS]:
            action = "BUY"
    label_action.config(text=f"Hành động: {action}")
    root.after(5000, update_table)

# =================== GUI ===================
root = tk.Tk()
root.title("CORL Tracker")

frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

tree = ttk.Treeview(frame, columns=("From", "To", "Amount"), show="headings")
tree.heading("From", text="From")
tree.heading("To", text="To")
tree.heading("Amount", text="Amount")
tree.pack()

label_action = ttk.Label(root, text="Hành động: HOLD", font=("Arial", 16), foreground="blue")
label_action.pack(pady=10)

# Start GUI update loop
update_table()
root.mainloop()
