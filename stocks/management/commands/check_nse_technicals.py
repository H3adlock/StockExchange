from django.core.management.base import BaseCommand
from stocks.models import Symbol, NSEHistoricalData, NSETechnical
from django.db.models import Q
import logging
import pandas as pd
import numpy as np
from ta.volume import AccDistIndexIndicator, MFIIndicator
from ta.volatility import BollingerBands
from ta.trend import MACD, SMAIndicator, EMAIndicator, IchimokuIndicator
from ta.momentum import StochRSIIndicator, RSIIndicator

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Check NSE Technicals'

    def handle(self, *args, **options):
        # import pdb
        # pdb.set_trace()
        last_date = NSEHistoricalData.objects.all().order_by(
            'timestamp').last().timestamp
        rsi_buy = NSETechnical.objects.filter(
            Q(nse_historical_data__timestamp=last_date) & Q(nse_historical_data__series='EQ') & Q(
                momentum_rsi__gte=55) & Q(momentum_rsi__lte=60)).values(
            'nse_historical_data__symbol__symbol_name', 'momentum_rsi')
