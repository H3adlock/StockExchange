from django.contrib import admin
from stocks.models import Symbol, NSEHistoricalData, NSETechnical

# Register your models here.
admin.site.register(Symbol)
admin.site.register(NSEHistoricalData)
admin.site.register(NSETechnical)
