from django.db import models


class Symbol(models.Model):
    symbol_name = models.CharField(max_length=50, blank=False, null=False, unique= True)

    def __str__(self):
        return self.symbol_name
