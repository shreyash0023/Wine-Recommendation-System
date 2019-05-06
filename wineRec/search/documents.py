from django_elasticsearch_dsl import DocType, Index
from .models import Wine

wine = Index('wines')


@wine.doc_type
class WineDocument(DocType):
    class Meta:
        model = Wine # The model associated with this DocType

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
       'country',
			'description',
			'designation',
			'title',
			'variety',
			'winery'
        ]





