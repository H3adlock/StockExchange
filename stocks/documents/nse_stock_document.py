from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from stocks.models import Symbol, NSEHistoricalData


@registry.register_document
class NSEStockDocument(Document):
    symbol = fields.ObjectField(properties={
        'symbol_name': fields.TextField(),
    })

    def get_queryset(self):
        """Not mandatory but to improve performance we can select related in one sql request"""
        return super(NSEStockDocument, self).get_queryset().select_related(
            'symbol'
        )

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the NSEHistoricalData instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """
        if isinstance(related_instance, Symbol):
            return related_instance.nsehistoricaldata_set.all()

    class Index:
        name = 'nse-stocks'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = NSEHistoricalData
        fields = [
            'ISIN',
            'series',
            'open',
            'high',
            'low',
            'close',
            'last',
            'prev_close',
            'total_traded_quantity',
            'total_traded_value',
            'timestamp',
            'total_trades'
        ]
        related_models = [Symbol]
