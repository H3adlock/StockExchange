from django.db import models
from stocks.models.nse_historical_data import NSEHistoricalData


class NSETechnical(models.Model):
    nse_historical_data = models.OneToOneField(NSEHistoricalData, null=False, blank=False, on_delete=models.CASCADE)
    trend_macd = models.FloatField(null=True, blank=True)
    trend_macd_signal = models.FloatField(null=True, blank=True)
    trend_macd_diff = models.FloatField(null=True, blank=True)
    trend_sma_fast = models.FloatField(null=True, blank=True)
    trend_sma_slow = models.FloatField(null=True, blank=True)
    trend_ema_fast = models.FloatField(null=True, blank=True)
    trend_ema_slow = models.FloatField(null=True, blank=True)
    trend_ichimoku_conv = models.FloatField(null=True, blank=True)
    trend_ichimoku_base = models.FloatField(null=True, blank=True)
    trend_ichimoku_a = models.FloatField(null=True, blank=True)
    trend_ichimoku_b = models.FloatField(null=True, blank=True)
    trend_visual_ichimoku_a = models.FloatField(null=True, blank=True)
    trend_visual_ichimoku_b = models.FloatField(null=True, blank=True)
    volatility_bbm = models.FloatField(null=True, blank=True)
    volatility_bbh = models.FloatField(null=True, blank=True)
    volatility_bbl = models.FloatField(null=True, blank=True)
    volatility_bbw = models.FloatField(null=True, blank=True)
    volatility_bbp = models.FloatField(null=True, blank=True)
    volatility_bbhi = models.FloatField(null=True, blank=True)
    volatility_bbli = models.FloatField(null=True, blank=True)
    volume_adi = models.FloatField(null=True, blank=True)
    volume_mfi = models.FloatField(null=True, blank=True)
    momentum_rsi = models.FloatField(null=True, blank=True)
    momentum_stoch_rsi = models.FloatField(null=True, blank=True)
    momentum_stoch_rsi_k = models.FloatField(null=True, blank=True)
    momentum_stoch_rsi_d = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.nse_historical_data.symbol.symbol_name + ' ' + self.nse_historical_data.timestamp.strftime('%Y%m%d')
