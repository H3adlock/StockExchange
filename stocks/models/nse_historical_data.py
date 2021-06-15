from djmoney.models.fields import MoneyField
from django.db import models
from stocks.models.symbol import Symbol


class NSEHistoricalData(models.Model):
    ISIN = models.CharField(max_length=20, blank=False, null=False)
    symbol = models.ForeignKey(Symbol, on_delete=models.PROTECT, blank=False, null=False)
    series = models.CharField(max_length=10, blank=True, null=True)
    open = models.DecimalField(max_digits=14, decimal_places=2, blank=False, null=False)
    high = models.DecimalField(max_digits=14, decimal_places=2, blank=False, null=False)
    low = models.DecimalField(max_digits=14, decimal_places=2, blank=False, null=False)
    close = models.DecimalField(max_digits=14, decimal_places=2, blank=False, null=False)
    last = models.DecimalField(max_digits=14, decimal_places=2, blank=False, null=False)
    prev_close = models.DecimalField(max_digits=14, decimal_places=2, blank=False, null=False)
    total_traded_quantity = models.BigIntegerField(blank=False, null=False)
    total_traded_value = models.DecimalField(max_digits=14, decimal_places=2, blank=False, null=False)
    timestamp = models.DateField(blank=False, null=False)
    total_trades = models.BigIntegerField(blank=False, null=False)
