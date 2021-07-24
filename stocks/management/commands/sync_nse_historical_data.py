import glob
from django.core.management.base import BaseCommand
from stocks.models import Symbol, NSEHistoricalData
import logging
from datetime import datetime
import pandas as pd
import numpy as np

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Syncs NSE Historical Data'

    def handle(self, *args, **kwargs):
        last_record = NSEHistoricalData.objects.order_by('timestamp').last()
        nse_csv_list = glob.glob("historic_data_dump/*_NSE.csv")
        import_csv_list = []
        if last_record:
            last_record_date = int(last_record.timestamp.strftime('%Y%m%d'))
            print(f"last record date: {last_record_date}")
            for csv_name in nse_csv_list:
                if int(csv_name.lstrip('historic_data_dump\\').rstrip('_NSE.csv')) > last_record_date:
                    import_csv_list.append(csv_name)
        else:
            log.info(f"No record in db")
            import_csv_list = nse_csv_list
        total_records = 0
        for csv_name in import_csv_list:
            print(f"processing {csv_name} ...")
            data = pd.read_csv(csv_name)
            data.dropna(how='all', inplace=True)
            data.replace({np.nan: None}, inplace=True)
            nse_data_list = []
            count = 0
            for row in data.index:
                nse_data = data.loc[row].copy()
                nse_data['TIMESTAMP'] = pd.to_datetime(nse_data['TIMESTAMP'], format="%d-%b-%Y")
                if nse_data['TIMESTAMP']:
                    nse_data_list.append(
                        NSEHistoricalData(ISIN=nse_data['ISIN'],
                                          symbol=Symbol.objects.get_or_create(symbol_name=nse_data['SYMBOL'])[0],
                                          series=nse_data['SERIES'],
                                          open=nse_data['OPEN'], high=nse_data['HIGH'], low=nse_data['LOW'],
                                          close=nse_data['CLOSE'], last=nse_data['LAST'], prev_close=nse_data['PREVCLOSE'],
                                          total_traded_quantity=nse_data['TOTTRDQTY'],
                                          total_traded_value=nse_data['TOTTRDVAL'],
                                          timestamp=nse_data['TIMESTAMP'], total_trades=nse_data['TOTALTRADES']))
                    count += 1
            NSEHistoricalData.objects.bulk_create(nse_data_list)
            print(f"{count} nse record added from {csv_name}...")
            total_records += count
        print(f"{total_records} nse record added from {len(import_csv_list)} files...")
