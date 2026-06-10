# MCP Server with PostgreSQL

A simple [MCP](https://modelcontextprotocol.io/) server built with [FastMCP](https://gofastmcp.com/getting-started/welcome). It exposes tools to query from a PostgreSQL database.

## Stack

- [FastMCP](https://gofastmcp.com/) — MCP server framework (similar idea to FastAPI, but for MCP tools)
- [SQLAlchemy 2](https://docs.sqlalchemy.org/) — async ORM 
- [Alembic](https://alembic.sqlalchemy.org/) — database migrations
- [pytest](https://docs.pytest.org/) + [pytest-asyncio](https://pytest-asyncio.readthedocs.io/) — integration tests, unit tests...
- [Docker Compose](https://docs.docker.com/compose/) — local Postgres for development
- [uv](https://docs.astral.sh/uv/) — dependency and virtualenv management

## Project structure

```
├── main.py                 # Entry point (stdio transport)
├── server.py               # MCP tools and server logic
├── db.py                   # SQLAlchemy models, Db session manager, seed data
├── settings.py             # Pydantic settings (.env)
├── docker-compose-dev.yml  # Local PostgreSQL
├── migrations/             # Alembic migrations
└── tests/
    └── test_server.py      # MCP connection and tool listing test
```

## Setup


### Environment variables

Create a `.env` file in the project root:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=mcp
POSTGRES_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/mcp
```

`POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB` are used by the Postgres container. `POSTGRES_URL` is used by the application and Alembic.

Optional:

```env
environment=Dev
```

### Start PostgreSQL

```bash
docker compose -f docker-compose-dev.yml up -d
```

- [FastMCP docs](https://gofastmcp.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [uv documentation](https://docs.astral.sh/uv/)
- [Alembic documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy 2.0 ORM](https://docs.sqlalchemy.org/en/20/orm/)

