import certifi
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from base_utils.exception import ImproperConfigurationError
import asyncio
from config import host,username,password,db_name,prod

client: AsyncIOMotorClient | None = None

async def init(test: bool, loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()) -> None:
	global client
	global db_name
	conn_params = {
		'host': host,
		'username': username,
		'password': password
	}
	
	if all(conn_params.values()):
		client = AsyncIOMotorClient(
    	host=f"mongodb+srv://{conn_params['host']}/?retryWrites=true&w=majority",
			username=conn_params['username'],
			password=conn_params['password'],
			uuidRepresentation='standard',
			tlsCAFile=certifi.where(),
			io_loop=loop,
		)
  
		print(await client.server_info())
	else:
		raise ImproperConfigurationError('Problem with MongoDB environment variables')

	db_name = db_name
	if prod == 'false' and not test:
		db_name += '_dev'
	elif prod == 'false' and test:
		db_name += '_test'
  
	if db_name is not None:
		await init_beanie(database=client[db_name], document_models=[
			"user_eval.models.UserEval",
			"template.models.Template",
			"template.requirement.models.Requirement",
			"template.requirement.models.RequirementView",
			"template.requirement.models.RequirementCategoryTopicView",
			"user_role.models.UserRole",
    ],
    allow_index_dropping = True,
    recreate_views=True
    )

		return client, db_name
	else:
		raise ImproperConfigurationError('Problem with MongoDB environment variables')
    