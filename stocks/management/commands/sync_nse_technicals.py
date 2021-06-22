from django.core.management.base import BaseCommand
from stocks.models import Symbol, NSEHistoricalData, NSETechnical
import logging
import pandas as pd
import numpy as np
from ta.volume import AccDistIndexIndicator, MFIIndicator
from ta.volatility import BollingerBands
from ta.trend import MACD, SMAIndicator, EMAIndicator, IchimokuIndicator
from ta.momentum import StochRSIIndicator, RSIIndicator

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Syncs NSE Technicals'

    def add_arguments(self, parser):
        parser.add_argument('--override', dest='update', action='store_false', help='', default=True)

    def handle(self, *args, **options):
        # import pdb
        # pdb.set_trace()
        if not options['update']:
            NSETechnical.objects.all().delete()
        symbols = Symbol.objects.all()
        for symbol in symbols:
            nse_history_data = NSEHistoricalData.objects.filter(symbol__symbol_name=symbol).order_by(
                'timestamp')
            if not nse_history_data:
                continue
            nse_technical = pd.DataFrame(
                list(nse_history_data.values('timestamp', 'open', 'high', 'low', 'close', 'total_traded_quantity')))
            '''
                Moving average convergence divergence
            '''
            indicator_macd = MACD(
                close=nse_technical['close'], window_slow=26, window_fast=12, window_sign=9, fillna=False
            )
            nse_technical["trend_macd"] = indicator_macd.macd()
            nse_technical["trend_macd_signal"] = indicator_macd.macd_signal()
            nse_technical["trend_macd_diff"] = indicator_macd.macd_diff()

            '''
                Simple Moving Average
            '''
            nse_technical["trend_sma_fast"] = SMAIndicator(
                close=nse_technical['close'], window=12, fillna=False
            ).sma_indicator()
            nse_technical["trend_sma_slow"] = SMAIndicator(
                close=nse_technical['close'], window=26, fillna=False
            ).sma_indicator()

            '''
                Exponential Moving Average
            '''
            nse_technical["trend_ema_fast"] = EMAIndicator(
                close=nse_technical['close'], window=12, fillna=False
            ).ema_indicator()
            nse_technical["trend_ema_slow"] = EMAIndicator(
                close=nse_technical['close'], window=26, fillna=False
            ).ema_indicator()
            '''
                Ichimoku Indicator
            '''
            indicator_ichi = IchimokuIndicator(
                high=nse_technical['high'],
                low=nse_technical['low'],
                window1=9,
                window2=26,
                window3=52,
                visual=False,
                fillna=False,
            )
            nse_technical["trend_ichimoku_conv"] = indicator_ichi.ichimoku_conversion_line()
            nse_technical["trend_ichimoku_base"] = indicator_ichi.ichimoku_base_line()
            nse_technical["trend_ichimoku_a"] = indicator_ichi.ichimoku_a()
            nse_technical["trend_ichimoku_b"] = indicator_ichi.ichimoku_b()
            indicator_ichi_visual = IchimokuIndicator(
                high=nse_technical['high'],
                low=nse_technical['low'],
                window1=9,
                window2=26,
                window3=52,
                visual=True,
                fillna=False,
            )
            nse_technical["trend_visual_ichimoku_a"] = indicator_ichi_visual.ichimoku_a()
            nse_technical["trend_visual_ichimoku_b"] = indicator_ichi_visual.ichimoku_b()
            '''
                Bollinger Band
            '''
            indicator_bb = BollingerBands(
                close=nse_technical['close'], window=20, window_dev=2, fillna=False
            )
            nse_technical["volatility_bbm"] = indicator_bb.bollinger_mavg()
            nse_technical["volatility_bbh"] = indicator_bb.bollinger_hband()
            nse_technical["volatility_bbl"] = indicator_bb.bollinger_lband()
            nse_technical["volatility_bbw"] = indicator_bb.bollinger_wband()
            nse_technical["volatility_bbp"] = indicator_bb.bollinger_pband()
            nse_technical["volatility_bbhi"] = indicator_bb.bollinger_hband_indicator()
            nse_technical["volatility_bbli"] = indicator_bb.bollinger_lband_indicator()
            '''
                Accumulation Distribution Index
            '''
            nse_technical["volume_adi"] = AccDistIndexIndicator(
                high=nse_technical['high'], low=nse_technical['low'], close=nse_technical['close'],
                volume=nse_technical['total_traded_quantity'], fillna=False
            ).acc_dist_index()
            '''
                Money Flow Index
            '''
            nse_technical["volume_mfi"] = MFIIndicator(
                high=nse_technical['high'],
                low=nse_technical['low'],
                close=nse_technical['close'],
                volume=nse_technical['total_traded_quantity'],
                window=14,
                fillna=False,
            ).money_flow_index()
            '''
                Relative Strength Index (RSI)
            '''
            nse_technical["momentum_rsi"] = RSIIndicator(
                close=nse_technical['close'], window=14, fillna=False
            ).rsi()

            '''
                Stoch RSI (StochRSI)
            '''
            indicator_srsi = StochRSIIndicator(
                close=nse_technical['close'], window=14, smooth1=3, smooth2=3, fillna=False
            )
            nse_technical["momentum_stoch_rsi"] = indicator_srsi.stochrsi()
            nse_technical["momentum_stoch_rsi_k"] = indicator_srsi.stochrsi_k()
            nse_technical["momentum_stoch_rsi_d"] = indicator_srsi.stochrsi_d()

            nse_technical.replace({np.nan: None}, inplace=True)
            nse_technical.replace([np.inf, -np.inf], None, inplace=True)
            list_to_create = []
            list_to_update = []
            for index in range(len(nse_history_data) - 1, -1, -1):
                data = nse_history_data[index]
                if data.technicals:
                    break
                technical = NSETechnical(nse_historical_data=data,
                                         trend_macd=nse_technical['trend_macd'][index],
                                         trend_macd_signal=nse_technical['trend_macd_signal'][index],
                                         trend_macd_diff=nse_technical['trend_macd_diff'][index],
                                         trend_sma_fast=nse_technical['trend_sma_fast'][index],
                                         trend_sma_slow=nse_technical['trend_sma_slow'][index],
                                         trend_ema_fast=nse_technical['trend_ema_fast'][index],
                                         trend_ema_slow=nse_technical['trend_ema_slow'][index],
                                         trend_ichimoku_conv=nse_technical['trend_ichimoku_conv'][index],
                                         trend_ichimoku_base=nse_technical['trend_ichimoku_base'][index],
                                         trend_ichimoku_a=nse_technical['trend_ichimoku_a'][index],
                                         trend_ichimoku_b=nse_technical['trend_ichimoku_b'][index],
                                         trend_visual_ichimoku_a=nse_technical[
                                             'trend_visual_ichimoku_a'][index],
                                         trend_visual_ichimoku_b=nse_technical[
                                             'trend_visual_ichimoku_b'][index],
                                         volatility_bbm=nse_technical['volatility_bbm'][index],
                                         volatility_bbh=nse_technical['volatility_bbh'][index],
                                         volatility_bbl=nse_technical['volatility_bbl'][index],
                                         volatility_bbw=nse_technical['volatility_bbw'][index],
                                         volatility_bbp=nse_technical['volatility_bbp'][index],
                                         volatility_bbhi=nse_technical['volatility_bbhi'][index],
                                         volatility_bbli=nse_technical['volatility_bbli'][index],
                                         volume_adi=nse_technical['volume_adi'][index],
                                         volume_mfi=nse_technical['volume_mfi'][index],
                                         momentum_rsi=nse_technical['momentum_rsi'][index],
                                         momentum_stoch_rsi=nse_technical['momentum_stoch_rsi'][index],
                                         momentum_stoch_rsi_k=nse_technical[
                                             'momentum_stoch_rsi_k'][index],
                                         momentum_stoch_rsi_d=nse_technical[
                                             'momentum_stoch_rsi_d'][index])
                data.technicals = True
                list_to_update.append(data)
                list_to_create.append(technical)
            NSETechnical.objects.bulk_create(list_to_create)
            NSEHistoricalData.objects.bulk_update(list_to_update, ['technicals'])
            print(f"Technicals updated for {symbol}")
