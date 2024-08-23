.PHONY: sql/migrations
sql/migrations:
	@PYTHONPATH=`pwd` alembic revision --autogenerate -m "Initial migration"

.PHONY: sql/migrate
sql/migrate:
	@PYTHONPATH=`pwd` alembic upgrade heads
