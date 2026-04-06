from .utils import get_recommendations

def signal_info(request):
    """
    Context processor to provide buy/sell signal counts to all templates.
    """
    if not request.user.is_authenticated:
        return {}

    try:
        from .models import MFPortfolio, CoinPortfolio
        from decimal import Decimal
        recommendations, _, _ = get_recommendations(request.user)
        
        # 1. Stocks & ETFs (Broad Logic - matching dashboard recommendations)
        buy_count = sum(1 for r in recommendations if r.get('action') == 'BUY')
        reduce_count = sum(1 for r in recommendations if r.get('action') == 'REDUCE')
        sell_count = sum(1 for r in recommendations if r.get('action') == 'SELL')
        
        # 2. Mutual Funds advice
        mf_buy = 0
        mf_sell = 0
        mf_holdings = MFPortfolio.objects.filter(user=request.user)
        for h in mf_holdings:
            if h.pnl_percentage >= 22:
                mf_sell += 1
            if h.realized_profit > 0:
                target = Decimal('100000') + h.realized_profit
                if h.invested_amount < target:
                    mf_buy += 1
                    
        # 3. Coin advice (Simple 22% rule for now)
        coin_buy = 0
        coin_sell = 0
        coin_holdings = CoinPortfolio.objects.filter(user=request.user)
        for h in coin_holdings:
            if h.pnl_percentage >= 22:
                coin_sell += 1
        
        total_actions = buy_count + reduce_count + sell_count + mf_buy + mf_sell + coin_buy + coin_sell
        
        return {
            'total_signal_count': total_actions,
            'action_count': total_actions,
            'sell_count': sell_count,
            'buy_count': buy_count,
            'reduce_count': reduce_count,
            # Pass individual counts for potential use in portfolio template
            'mf_buy_count': mf_buy,
            'mf_redemption_count': mf_sell,
            'coin_buy_count': coin_buy,
            'coin_sell_count': coin_sell,
        }
    except Exception as e:
        # Avoid crashing the entire site if recommendation logic fails
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in signal_info context processor: {e}")
        return {
            'buy_reduce_count': 0,
            'sell_count': 0,
            'has_sell_signal': False,
        }
