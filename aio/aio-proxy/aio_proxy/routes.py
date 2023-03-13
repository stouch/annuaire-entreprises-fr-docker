import os

from aiohttp import web
from dotenv import load_dotenv
from elasticsearch_dsl import connections

from aio_proxy.response.build_response import api_response
from aio_proxy.search.geo_search import geo_search
from aio_proxy.search.parameters import extract_geo_parameters, extract_text_parameters
from aio_proxy.search.text_search import text_search

load_dotenv()

# Get env variables
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_USER = os.getenv("ELASTIC_USER")
ELASTIC_URL = os.getenv("ELASTIC_URL")

# Connect to Elasticsearch
if (ELASTIC_USER and ELASTIC_PASSWORD):
    connections.create_connection(
        hosts=[ELASTIC_URL],
        http_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
        retry_on_timeout=True,
    )
else:
    connections.create_connection(
        hosts=[ELASTIC_URL],
        retry_on_timeout=True,
    )

routes = web.RouteTableDef()


@routes.get("/search")
async def search_text_endpoint(request):
    return api_response(
        request, extract_function=extract_text_parameters, search_function=text_search
    )


@routes.get("/near_point")
async def near_point_endpoint(request):
    return api_response(
        request, extract_function=extract_geo_parameters, search_function=geo_search
    )
