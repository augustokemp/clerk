import os
import psycopg, voyageai
from dotenv import load_dotenv
from pgvector.psycopg import register_vector
from anthropic import Anthropic

load_dotenv()

conn = psycopg.connect(
    host=os.environ["POSTGRES_HOST"],
    port=5432,
    dbname=os.environ["POSTGRES_DB"],
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
)
register_vector(conn)

vo = voyageai.Client()
claude = Anthropic()