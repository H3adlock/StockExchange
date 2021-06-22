from django.db import models
from stocks.models.symbol import Symbol


class NSEHistoricalData(models.Model):
    ISIN = models.CharField(max_length=20, blank=False, null=False)
    symbol = models.ForeignKey(Symbol, on_delete=models.PROTECT, blank=False, null=False)
    series = models.CharField(max_length=10, blank=True, null=True)
    open = models.FloatField(blank=False, null=False)
    high = models.FloatField(blank=False, null=False)
    low = models.FloatField(blank=False, null=False)
    close = models.FloatField(blank=False, null=False)
    last = models.FloatField(blank=False, null=False)
    prev_close = models.FloatField(blank=False, null=False)
    total_traded_quantity = models.BigIntegerField(blank=False, null=False)
    total_traded_value = models.FloatField(blank=False, null=False)
    timestamp = models.DateField(blank=False, null=False)
    total_trades = models.BigIntegerField(blank=False, null=False)
    technicals = models.BooleanField(blank=False, null=False, default=False)

    def __str__(self):
        return self.symbol.symbol_name + ' ' + self.timestamp.strftime('%Y%m%d')
