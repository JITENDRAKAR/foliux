import os

file_path = r".\core\views.py"

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_head = [
    "from django.shortcuts import render, redirect, get_object_or_404\n",
    "from django.db import models\n",
    "from django.contrib import messages\n",
    "from django.contrib.auth.decorators import login_required\n",
    "from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt\n",
    "from django.contrib.auth.forms import UserCreationForm\n",
    "from django.contrib.auth.models import User\n",
    "from django.contrib.auth import login\n",
    "from django.core.mail import send_mail\n",
    "from django.conf import settings\n",
    "from django.http import JsonResponse\n",
    "from django.utils import timezone\n",
    "from datetime import datetime, timedelta, date\n",
    "from dateutil.relativedelta import relativedelta\n",
    "from django.contrib.auth.views import PasswordChangeView\n",
    "from django.contrib.auth.forms import SetPasswordForm as DjangoSetPasswordForm\n",
    "try:\n",
    "    from allauth.account.forms import SetPasswordForm as AllauthSetPasswordForm\n",
    "except ImportError:\n",
    "    AllauthSetPasswordForm = DjangoSetPasswordForm\n",
    "\n",
    "from .models import (\n",
    "    Portfolio, PnLStatement, Instrument, Profile, OTP, Transaction, \n",
    "    SignupOTP, MarketTicker, Strategy, MutualFund, MFPortfolio, MFTransaction,\n",
    "    Coin, CoinPortfolio, CoinTransaction,\n",
    "    NPSFund, NPSPortfolio, NPSTransaction, FixedAsset, OtherAsset,\n",
    "    Loan, LoanPayment, IPO, ChatbotKnowledge\n",
    ")\n",
    "from .forms import (\n",
    "    UploadFileForm, PortfolioForm, ManualPortfolioForm, \n",
    "    CustomUserCreationForm, ProfileForm, ForgotPasswordForm, \n",
    "    VerifyOTPForm, SetPasswordForm, EditLotForm,\n",
    "    LoanForm, LoanPaymentForm\n",
    ")\n",
    "from .utils import fetch_live_ltp, perform_sync, get_recommendations, fetch_strategy_stocks, get_target_user\n",
    "\n",
    "import random\n"
]

# Find where the old head ended. We know it currently has 'import json' at line 18 (index 17)
# But let's be safer and find 'import json'
json_idx = -1
for i, line in enumerate(lines):
    if line.strip() == "import json":
        json_idx = i
        break

if json_idx != -1:
    new_lines = new_head + lines[json_idx:]
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("Successfully fixed views.py head")
else:
    print("Could not find import json")
