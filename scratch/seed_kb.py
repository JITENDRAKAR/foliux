import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investment_advisory.settings')
django.setup()

from core.models import ChatbotKnowledge

kb = {
    "what is": "NPITS (Net Profit Investment Tracking System) is a rules-based financial platform designed for disciplined wealth creation. It helps you manage multiple asset classes with precision using FIFO accounting.",
    "npits": "NPITS is your central hub for investment management. It uses data-driven signals to remove emotions from investing, focusing on automated 'Buy' and 'Sell' advice.",
    "foliux": "FOLIUX is the premium branding for NPITS, representing our professional-grade suite of investment tracking tools and advanced strategy simulations.",
    "security": "NPITS prioritizes your data security. Your sensitive investment data is encrypted (using Fernet encryption), and we use secure OTP-based authentication for logins and family linking.",
    "how to add": "You can add items by clicking 'Add Instrument' on any dashboard. For stocks, you can also use 'Buy Stock' to add a single lot or 'Upload Portfolio' for bulk entry.",
    "upload": "To upload in bulk, go to the Stock Dashboard and click 'Upload Portfolio'. We support .csv and .xlsx files from major brokers like Zerodha, Groww, etc.",
    "excel": "You can download your portfolio as an Excel file using the 'Export' button on the Stock Dashboard for offline analysis.",
    "google sheets": "NPITS can sync with Google Sheets for real-time data ingestion. Check the 'Sync' options on the dashboard for more details.",
    "fifo": "NPITS uses First-In-First-Out (FIFO) logic to track individual stock lots. This ensures accurate P&L calculation and tax planning by matching your oldest buys with your sales.",
    "lots": "Lot-based tracking means every purchase of a stock is treated separately. This helps you see the profit of each specific entry instead of just a consolidated average.",
    "signals": "Signals are rule-based indicators: 'BUY' (price is low/attractive), 'SELL' (target reached), 'HOLD' (maintain position), and 'REDUCE' (over-allocation detected).",
    "rules": "Our rules are based on predefined strategies like the 5% Index Strategy. These signals help you stay disciplined and avoid emotional trading.",
    "strategy": "The Strategy page explains our frameworks: 'FlexiMultiInvest' (Broad Market), 'NiftyQuant' (Top 50), and 'Pyramiding' (Thematic/Sectoral).",
    "quant": "NiftyQuant is a strategy focusing on high-liquidity Nifty 50 stocks with specific rebalancing rules.",
    "flexi": "FlexiMultiInvest uses broad-market ETFs to provide diversified exposure with rule-based entry points.",
    "pyramid": "Pyramiding focuses on building positions in strong sectoral trends and ETFs like ITBEES, BANKBEES, etc.",
    "backtest": "The Strategic Simulation Lab (Backtester) on the Strategy page allows you to test how these rules would have performed in the past.",
    "stocks": "The Stock Dashboard tracks your equity investments, providing real-time P&L, signal badges, and allocation charts.",
    "mutual funds": "MF Cue helps you track Mutual Funds, SIPs, and goal-based investments with automated sell-trigger alerts.",
    "mf": "Mutual Fund Cue provides advice on when to sell (at 22% profit target) and tracks your monthly SIP executions automatically.",
    "nps": "NPS Cue tracks your National Pension System funds and NAVs across various fund managers (Scheme E, C, G).",
    "coin": "The Coin Dashboard tracks digital assets and cryptocurrencies with live price updates and transaction history.",
    "fd": "The FD module tracks Fixed Deposits, showing maturity dates, interest rates, and total monthly interest income.",
    "loan": "The Loan module manages your EMIs, tracking how much of each payment goes toward principal versus interest.",
    "ipo": "The IPO Tracker shows upcoming and active Initial Public Offerings with listing dates and subscription statuses.",
    "family": "Family Linking allows you to view your family members' portfolios in read-only mode after they verify your request with an OTP.",
    "profile": "In 'Edit Profile', you can set your investment limits, update your photo, and toggle between Crore/Lakh and Million/Billion numbering systems.",
    "otp": "We use OTPs for secure actions like registration, password resets, and linking family accounts for maximum security.",
    "contact": "For support or bug reports, please reach out to the platform administrator via the support email in the footer.",
    "help": "You can ask me about: how to add stocks, how signals work, what is FIFO, how to link family, or details about MF and NPS modules.",
    "hello": "Hello! I am your NPITS Assistant. How can I help you manage your wealth today?",
    "hi": "Hi there! Welcome to NPITS. I'm here to help you navigate your portfolio and strategies.",
    "thanks": "You're welcome! Happy investing with NPITS.",
}

for q, a in kb.items():
    ChatbotKnowledge.objects.get_or_create(question=q, defaults={'answer': a})

print(f"Successfully seeded {len(kb)} KB entries.")
