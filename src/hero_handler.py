from src.routes.hero_route import router as router_user
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.logging import correlation_paths
from sqlmodel import create_engine

logger = Logger()
app = APIGatewayHttpResolver()
app.include_router(router_user)

connection_url = 'postgresql+psycopg2://admin:password@{}:5432'.format('host.docker.internal')
engine = create_engine(connection_url) #echo=True to debug


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_HTTP)
def handler(event: dict, context: LambdaContext) -> dict:
    app.append_context(engine = engine)
    return app.resolve(event, context)