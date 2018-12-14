from flask_restplus import Api

from .transaction import api as transaction
from .invoice import api as invoice
from .budget import api as budget
from .transaction_utility import api as transaction_utility
from .people import api as people

authorizations = {
	'amivapitoken' :{
		'type': 'apiKey',
		'in': 'header',
		'name': 'X-AMIV-API-TOKEN'
	}
}

api = Api(
    title='qTool API',
    version='0.1',
    description='qTool API',
    authorizations=authorizations,
    # All API metadatas
)

api.add_namespace(budget)
api.add_namespace(people)
api.add_namespace(invoice)
api.add_namespace(transaction)
api.add_namespace(transaction_utility)