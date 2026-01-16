.PHONY: migrate upgrade

# Gera uma nova migração (use: make migrate m="Descrição")
migrate:
    alembic revision --autogenerate -m "$(m)"

# Aplica as migrações pendentes
upgrade:
    alembic upgrade head

# Mostra o status das migrações
status:
    alembic current

# Reverte a última migração (cuidado!)
downgrade:
    alembic downgrade -1


alembic:
    alembic revision --autogenerate -m "Atualização de tabelas"
	alembic upgrade head