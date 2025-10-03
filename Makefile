.PHONY: run-dev

NAME=""

run-dev:
	docker compose -f compose.dev.yml up --build
	
generate-migrations:
	rm -f bytebox_temp.db
	DATABASE_URL=sqlite:///./bytebox_temp.db uv run alembic upgrade head
	DATABASE_URL=sqlite:///./bytebox_temp.db uv run alembic revision --autogenerate -m "${NAME}"
	rm -f bytebox_temp.db