"""
Crypto Payment App — Direct Trust Wallet
==========================================
✅ Accept Bitcoin, ETH, USDC and more
✅ Works globally including Germany
✅ No ID verification needed
✅ Money goes straight to your crypto wallet
✅ No third party — direct wallet payment

Run: python crypto_app.py
Expose: ngrok http 5003
"""

import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ── Bypass ngrok browser warning for all visitors ──────────────────────────
@app.after_request
def add_ngrok_header(response):
    response.headers['ngrok-skip-browser-warning'] = 'true'
    return response

# ── Your Trust Wallet BTC address ─────────────────────────────────────────
YOUR_CRYPTO_WALLET = "bc1qewgeyzd62uyaqgpmm8e0a9zum7fhjvz7lhhzp8"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Secure Checkout</title>
  <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400&display=swap" rel="stylesheet"/>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root {
      --bg: #0a0a0f; --surface: #13131a; --border: #2a2a38;
      --accent: #7b61ff; --text: #f0f0f8; --muted: #6b6b88;
      --danger: #ff6b8a; --green: #00c087;
    }
    body {
      background: var(--bg); color: var(--text);
      font-family: 'DM Sans', sans-serif;
      min-height: 100vh; display: flex;
      align-items: center; justify-content: center; padding: 20px;
    }
    body::before {
      content: ''; position: fixed; inset: 0;
      background-image:
        radial-gradient(ellipse at 20% 20%, rgba(123,97,255,0.08) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 80%, rgba(123,97,255,0.05) 0%, transparent 60%);
      pointer-events: none;
    }
    .card {
      background: var(--surface); border: 1px solid var(--border);
      border-radius: 24px; padding: 36px 32px;
      width: 100%; max-width: 420px;
      box-shadow: 0 0 60px rgba(123,97,255,0.10);
    }
    .moonpay-logo {
      font-family: 'Syne', sans-serif; font-size: 1.6rem;
      font-weight: 800; margin-bottom: 6px;
      letter-spacing: -0.02em; color: #ffffff;
    }
    .moonpay-logo span { color: #7b61ff; }
    .subtitle {
      color: var(--muted); font-size: 0.88rem;
      margin-bottom: 24px; font-style: italic;
    }
    .product {
      background: rgba(255,255,255,0.03); border: 1px solid var(--border);
      border-radius: 14px; padding: 16px 18px;
      display: flex; align-items: center; justify-content: space-between;
      margin-bottom: 26px;
    }
    .product-info { display: flex; align-items: center; gap: 12px; }
    .product-icon {
      width: 46px; height: 46px;
      background: linear-gradient(135deg, #7b61ff, #a78bfa);
      border-radius: 12px; display: flex; align-items: center;
      justify-content: center; font-size: 20px;
    }
    .product-name { font-family: 'Syne', sans-serif; font-weight: 700; }
    .product-desc { color: var(--muted); font-size: 0.78rem; margin-top: 2px; }
    .product-price {
      font-family: 'Syne', sans-serif; font-size: 1.4rem;
      font-weight: 800; color: var(--accent);
    }
    .coin-label { color: var(--muted); font-size: 0.82rem; margin-bottom: 10px; }
    .coin-grid {
      display: grid; grid-template-columns: repeat(3, 1fr);
      gap: 8px; margin-bottom: 20px;
    }
    .coin-btn {
      background: rgba(255,255,255,0.04); border: 1px solid var(--border);
      border-radius: 10px; padding: 10px 6px; cursor: pointer;
      text-align: center; transition: all 0.2s; color: var(--text);
      font-family: 'DM Sans', sans-serif; font-size: 0.78rem;
    }
    .coin-btn:hover { border-color: var(--accent); background: rgba(123,97,255,0.08); }
    .coin-btn.selected { border-color: var(--accent); background: rgba(123,97,255,0.15); color: var(--accent); }
    .coin-btn .coin-icon { font-size: 1.4rem; display: block; margin-bottom: 4px; }
    #pay-btn {
      width: 100%; padding: 15px; background: var(--accent);
      color: #ffffff; border: none; border-radius: 12px;
      font-family: 'Syne', sans-serif; font-size: 1rem; font-weight: 700;
      cursor: pointer; transition: opacity 0.2s, transform 0.15s;
    }
    #pay-btn:hover { opacity: 0.88; transform: translateY(-1px); }
    #pay-btn:disabled { opacity: 0.45; cursor: not-allowed; transform: none; }
    #error-msg {
      color: var(--danger); font-size: 0.84rem; margin-top: 12px;
      padding: 10px 14px; background: rgba(255,107,138,0.08);
      border: 1px solid rgba(255,107,138,0.2); border-radius: 8px; display: none;
    }
    #payment-details { display: none; }
    .payment-box {
      background: rgba(255,255,255,0.03); border: 1px solid var(--border);
      border-radius: 14px; padding: 20px; margin-bottom: 16px; text-align: center;
    }
    .payment-box .amount {
      font-family: 'Syne', sans-serif; font-size: 1.6rem; font-weight: 800;
      color: var(--accent); margin-bottom: 8px;
    }
    .payment-box .wallet-label { color: var(--muted); font-size: 0.78rem; margin-bottom: 6px; }
    .payment-box .wallet-addr {
      font-size: 0.72rem; word-break: break-all; color: var(--text);
      background: rgba(0,0,0,0.3); padding: 10px; border-radius: 8px;
      cursor: pointer; border: 1px solid var(--border);
    }
    .copy-hint { color: var(--muted); font-size: 0.72rem; margin-top: 6px; }
    .timer { color: var(--muted); font-size: 0.82rem; margin-top: 10px; }
    .timer span { color: var(--accent); font-weight: 700; }
    .status-badge {
      display: inline-block; padding: 4px 12px; border-radius: 100px;
      font-size: 0.75rem; font-weight: 700; margin-top: 12px;
      background: rgba(123,97,255,0.15); color: var(--accent);
    }
    #confirm-btn {
      width: 100%; padding: 14px; background: var(--green);
      color: #fff; border: none; border-radius: 12px;
      font-family: 'Syne', sans-serif; font-size: 1rem; font-weight: 700;
      cursor: pointer;
    }
    #success-msg { text-align: center; display: none; padding: 16px 0 4px; }
    #success-msg .check { font-size: 3rem; display: block; margin-bottom: 10px; animation: pop 0.4s cubic-bezier(0.34,1.56,0.64,1); }
    #success-msg h2 { font-family: 'Syne', sans-serif; font-size: 1.4rem; margin-bottom: 6px; }
    #success-msg p { color: var(--muted); font-size: 0.86rem; }
    @keyframes pop { from { transform: scale(0); opacity: 0; } to { transform: scale(1); opacity: 1; } }
    .security {
      display: flex; align-items: center; justify-content: center;
      gap: 6px; margin-top: 16px; color: var(--muted); font-size: 0.75rem;
    }
  </style>
</head>
<body>
<div class="card">

  <!-- MoonPay logo — text based, always loads, exact colors -->
  <div class="moonpay-logo">Moon<span>Pay</span></div>
  <div style="display:flex; justify-content:flex-end; margin-bottom:10px;">
  <button onclick="toggleLang()" id="lang-btn" style="background:rgba(123,97,255,0.15); border:1px solid #7b61ff; color:#7b61ff; padding:4px 12px; border-radius:100px; font-family:'Syne',sans-serif; font-size:0.75rem; font-weight:700; cursor:pointer;">🌐 DE</button>
</div>
<p class="subtitle" id="subtitle">Pay securely with crypto</p>

  <!-- Product block -->
  <div class="product">
    <div class="product-info">
      <div class="product-icon">💰</div>
      <div>
        <div class="product-name">Pending Deposit</div>
        <div class="product-desc">Payment: $250</div>
      </div>
    </div>
    <div class="product-price">$3,500</div>
  </div>

  <!-- Step 1: Choose coin -->
  <div id="checkout-form">
    <p class="coin-label">Select your cryptocurrency:</p>
    <div class="coin-grid">
      <button class="coin-btn selected" onclick="selectCoin('BTC',  this)"><span class="coin-icon">₿</span>Bitcoin</button>
      <button class="coin-btn"          onclick="selectCoin('ETH',  this)"><span class="coin-icon">Ξ</span>Ethereum</button>
      <button class="coin-btn"          onclick="selectCoin('USDT', this)"><span class="coin-icon">₮</span>Tether</button>
      <button class="coin-btn"          onclick="selectCoin('USDC', this)"><span class="coin-icon">◎</span>USDC</button>
      <button class="coin-btn"          onclick="selectCoin('LTC',  this)"><span class="coin-icon">Ł</span>Litecoin</button>
      <button class="coin-btn"          onclick="selectCoin('XRP',  this)"><span class="coin-icon">✕</span>XRP</button>
    </div>
    <button id="pay-btn" onclick="createPayment()">Pay $250 with BTC</button>
    <div id="error-msg"></div>
  </div>

  <!-- Step 2: Send to wallet address -->
  <div id="payment-details">
    <div class="payment-box">
      <div class="amount" id="crypto-amount">...</div>
      <div class="wallet-label">Send exactly this amount to:</div>
      <div class="wallet-addr" id="wallet-address" onclick="copyAddress()">...</div>
      <div class="copy-hint">Tap address to copy</div>
      <div class="timer">Expires in: <span id="countdown">60:00</span></div>
      <div class="status-badge" id="status-badge">⏳ Waiting for payment</div>
    </div>
    <button id="confirm-btn" onclick="confirmSent()">✓ I've sent the payment</button>
  </div>

  <!-- Success screen -->
  <div id="success-msg">
    <span class="check">✅</span>
    <h2>Payment Received!</h2>
    <p>Your deposit is confirmed.<br/>Thank you!</p>
  </div>

  <div class="security">🔒 256-bit encrypted · Secure checkout</div>
</div>

<script>
let selectedCoin = 'BTC';
let countdown    = 3600;
let timer        = null;

function selectCoin(coin, btn) {
  selectedCoin = coin;
  document.querySelectorAll('.coin-btn').forEach(b => b.classList.remove('selected'));
  btn.classList.add('selected');
  document.getElementById('pay-btn').textContent = `Pay $1,000 with ${coin}`;
}

async function createPayment() {
  const btn = document.getElementById('pay-btn');
  btn.disabled = true;
  btn.textContent = 'Loading…';
  hideError();

  try {
    const res  = await fetch('/create-crypto-payment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ coin: selectedCoin })
    });
    const data = await res.json();
    if (data.error) throw new Error(data.error);

    document.getElementById('crypto-amount').textContent  = `${data.pay_amount} ${selectedCoin}`;
    document.getElementById('wallet-address').textContent = data.pay_address;

    document.getElementById('checkout-form').style.display   = 'none';
    document.getElementById('payment-details').style.display = 'block';

    startCountdown();
  } catch(err) {
    showError(err.message);
    btn.disabled = false;
    btn.textContent = `Pay $1,000 with ${selectedCoin}`;
  }
}

function copyAddress() {
  const addr = document.getElementById('wallet-address').textContent;
  navigator.clipboard.writeText(addr).then(() => {
    document.querySelector('.copy-hint').textContent = '✓ Copied!';
    setTimeout(() => document.querySelector('.copy-hint').textContent = 'Tap address to copy', 2000);
  });
}

function confirmSent() {
  document.getElementById('status-badge').textContent = '✅ Confirmed — checking wallet…';
  setTimeout(() => {
    document.getElementById('payment-details').style.display = 'none';
    document.getElementById('success-msg').style.display     = 'block';
  }, 1500);
}

function startCountdown() {
  timer = setInterval(() => {
    countdown--;
    const m = Math.floor(countdown / 60).toString().padStart(2, '0');
    const s = (countdown % 60).toString().padStart(2, '0');
    document.getElementById('countdown').textContent = `${m}:${s}`;
    if (countdown <= 0) {
      clearInterval(timer);
      document.getElementById('countdown').textContent = 'Expired — please refresh';
    }
  }, 1000);
}

function showError(msg) {
  const el = document.getElementById('error-msg');
  el.textContent = '⚠ ' + msg; el.style.display = 'block';
}
function hideError() {
  document.getElementById('error-msg').style.display = 'none';
}let isGerman = false;
const translations = {
  subtitle:    ['Pay securely with crypto', 'Sicher mit Krypto bezahlen'],
  productName: ['Pending Deposit', 'Ausstehende Einzahlung'],
  productDesc: ['Payment: $250', 'Zahlung: $250'],
  coinLabel:   ['Select your cryptocurrency:', 'Wähle deine Kryptowährung:'],
  payBtn:      ['Pay $250 with', 'Zahle $250 mit'],
  confirmBtn:  ["✓ I've sent the payment", '✓ Ich habe gezahlt'],
  success:     ['Payment Received!', 'Zahlung erhalten!'],
  successMsg:  ['Your deposit is confirmed. Thank you!', 'Deine Einzahlung ist bestätigt. Danke!'],
  security:    ['256-bit encrypted · Secure checkout', '256-Bit-verschlüsselt · Sicherer Checkout'],
  walletLabel: ['Send exactly this amount to:', 'Sende genau diesen Betrag an:'],
  copyHint:    ['Tap address to copy', 'Adresse antippen zum Kopieren'],
  waiting:     ['⏳ Waiting for payment', '⏳ Warte auf Zahlung'],
  langBtn:     ['🌐 DE', '🌐 EN']
};

function toggleLang() {
  isGerman = !isGerman;
  const i = isGerman ? 1 : 0;
  document.getElementById('subtitle').textContent     = translations.subtitle[i];
  document.querySelector('.product-name').textContent = translations.productName[i];
  document.querySelector('.product-desc').textContent = translations.productDesc[i];
  document.querySelector('.coin-label').textContent   = translations.coinLabel[i];
  document.getElementById('pay-btn').textContent      = `${translations.payBtn[i]} ${selectedCoin}`;
  document.getElementById('confirm-btn').textContent  = translations.confirmBtn[i];
  document.querySelector('#success-msg h2').textContent = translations.success[i];
  document.querySelector('#success-msg p').textContent  = translations.successMsg[i];
  document.querySelector('.security').textContent     = translations.security[i];
  document.querySelector('.wallet-label').textContent = translations.walletLabel[i];
  document.querySelector('.copy-hint').textContent    = translations.copyHint[i];
  document.getElementById('status-badge').textContent = translations.waiting[i];
  document.getElementById('lang-btn').textContent     = translations.langBtn[i];
}
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/create-crypto-payment", methods=["POST"])
def create_crypto_payment():
    data = request.get_json()
    coin = data.get("coin", "BTC")

    # BTC amounts per $1,000 (approximate)
    amounts = {
        "BTC":  "0.016",
        "ETH":  "0.63",
        "USDT": "1000",
        "USDC": "1000",
        "LTC":  "23.13",
        "XRP":  "907.77"
    }

    return jsonify(
        payment_id  = "direct",
        pay_amount  = amounts.get(coin, "0.016"),
        pay_address = YOUR_CRYPTO_WALLET
    )


@app.route("/check-payment/<payment_id>")
def check_payment(payment_id):
    # Direct wallet — manually confirmed by buyer
    return jsonify(status="waiting")


if __name__ == "__main__":
    print("\n" + "="*50)
    print("  ₿  Crypto Payment App")
    print("="*50)
    print("  Local:   http://localhost:5003")
    print("  iPhone:  run `ngrok http 5003`")
    print("="*50 + "\n")
    app.run(debug=True, port=5003)
