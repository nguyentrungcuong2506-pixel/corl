import requests
import time

# =================== CẤU HÌNH ===================

TOKEN_ADDRESS_ETH = "0xfd9a3f94bec6b08711d90ff69cbba42fac96b45a"      # CORL token ETH
LEADING_WALLETS = [
"0x30a018455a8c6f9a50a6e89d01a6f0adfb167d2e"
]

ETHERSCAN_API_KEY = "AM2DBRIY6GUACJYY478MP1NQMBE7B6HYB1"

# Telegram bot

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"         # <-- thay token bot thật vào đây
CHAT_ID = "YOUR_CHAT_ID"                      # <-- thay chat_id (user/group) cần gửi tin nhắn

# =================== HÀM GỬI TELEGRAM ===================

def send_tele_message(text):
try:
url = f"[https://api.telegram.org/bot{BOT_TOKEN}/sendMessage](https://api.telegram.org/bot{BOT_TOKEN}/sendMessage)"
payload = {"chat_id": CHAT_ID, "text": text}
requests.post(url, data=payload, timeout=10)
except Exception as e:
print("Lỗi gửi Telegram:", e)

# =================== HÀM LẤY GIAO DỊCH ===================

def get_transactions():
url = f"[https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={TOKEN_ADDRESS_ETH}&sort=desc&apikey={ETHERSCAN_API_KEY}](https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={TOKEN_ADDRESS_ETH}&sort=desc&apikey={ETHERSCAN_API_KEY})"
try:
response = requests.get(url, timeout=10)
data = response.json()
if data['status'] == '1':
txs = data['result']
filtered = []
for tx in txs[:50]:
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

# =================== VÒNG LẶP CHÍNH ===================

def main():
print("CORL bot đang chạy 24/7...")
last_sent = set()
while True:
transactions = get_transactions()
for tx in transactions:
key = f"{tx['from']}-{tx['to']}-{tx['value']}"
if key not in last_sent:
if tx['from'].lower() in [w.lower() for w in LEADING_WALLETS]:
action = "🚨 SELL detected"
elif tx['to'].lower() in [w.lower() for w in LEADING_WALLETS]:
action = "🟢 BUY detected"
else:
action = "ℹ️ Other tx"
msg = f"{action}\nFrom: {tx['from']}\nTo: {tx['to']}\nValue: {tx['value']:.4f} CORL"
print(msg)
send_tele_message(msg)
last_sent.add(key)
time.sleep(30)  # kiểm tra lại mỗi 30 giây

if **name** == "**main**":
main()
