import glob
from django.core.management.base import BaseCommand
from stocks.models import Symbol, NSEHistoricalData
import logging
from datetime import datetime
import pandas as pd
import numpy as np

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Syncs NSE Symbols'

    def handle(self, *args, **kwargs):
        try:
            with open('NSE_CM_Symbol_List/BE SERIES.txt', 'r') as f:
                print(f"processing BE SERIES.txt ...")
                data = f.read().strip('\n')
                symbols = data.split('.BE.NSE')
                symbols.remove('')
                symbol_list = []
                count = 0
                for symbol in symbols:
                    symbol_list.append(Symbol(symbol_name=symbol.strip()))
                    count += 1
                Symbol.objects.bulk_create(symbol_list, ignore_conflicts=True)
                print(f"{count} nse symbol added from BE SERIES.txt...")
            with open('NSE_CM_Symbol_List/BZ SERIES.txt', 'r') as f:
                print(f"processing BZ SERIES.txt ...")
                data = f.read().strip('\n')
                symbols = data.split(',')
                symbol_list = []
                count = 0
                for symbol in symbols:
                    symbol_list.append(Symbol(symbol_name=symbol.split('.')[0]))
                    count += 1
                Symbol.objects.bulk_create(symbol_list, ignore_conflicts=True)
                print(f"{count} nse symbol added from BZ SERIES.txt...")
            with open('NSE_CM_Symbol_List/EQ SERIES.txt', 'r') as f:
                print(f"processing EQ SERIES.txt ...")
                data = f.read().strip('\n')

                symbols = data.split(',')
                symbol_list = []
                count = 0
                for symbol in symbols:
                    symbol_list.append(Symbol(symbol_name=symbol.split('.')[0]))
                    count += 1
                Symbol.objects.bulk_create(symbol_list, ignore_conflicts=True)
                print(f"{count} nse symbol added from EQ SERIES.txt...")
            with open('NSE_CM_Symbol_List/ETF SYMBOLS.txt', 'r') as f:
                print(f"processing ETF SYMBOLS.txt ...")
                data = f.read().strip('\n')
                symbols = data.split(',')
                symbol_list = []
                count = 0
                for symbol in symbols:
                    symbol_list.append(Symbol(symbol_name=symbol.split('.')[0]))
                    count += 1
                Symbol.objects.bulk_create(symbol_list)
                print(f"{count} nse symbol added from ETF SYMBOLS.txt...")
            with open('NSE_CM_Symbol_List/NSE_INDEX Symbols.txt', 'r') as f:
                print(f"processing NSE_INDEX Symbols.txt ...")
                data = f.read().strip('\n')

                symbols = data.split(',')
                symbol_list = []
                count = 0
                for symbol in symbols:
                    # import pdb
                    # pdb.set_trace()
                    symbol_list.append(Symbol(symbol_name=symbol.split('.')[0]))
                    count += 1
                Symbol.objects.bulk_create(symbol_list)
                print(f"{count} nse symbol added from NSE_INDEX Symbols.txt...")
        except Exception as e:
            log.exception(e)
