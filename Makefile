run:
	uv run uvicorn src.learn_backend.main:app --host 0.0.0.0 --port 8080 --reload

format:
	uv run ruff check --fix src
pg:
	docker compose -f docker-compose.yml up -d

pg-stop:
	docker compose -f docker-compose.yml down
