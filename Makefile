
IMAGE_NAME = logpie
CONTAINER_NAME = logpie-app

# Caminho do docker-compose (switch entre Linux/macOS conforme README)
COMPOSE_FILE = docker-compose.yaml

.PHONY: build run stop logs clean shell

## 🔨 Build da imagem
build:
	docker compose -f $(COMPOSE_FILE) build

## 🚀 Sobe a stack em background
run:
	docker compose -f $(COMPOSE_FILE) up -d

## 🛑 Para os containers
stop:
	docker compose -f $(COMPOSE_FILE) down

## 📜 Mostra os logs em tempo real
logs:
	docker compose -f $(COMPOSE_FILE) logs -f

## 🧹 Limpa tudo (containers + volumes)
clean:
	docker compose -f $(COMPOSE_FILE) down -v --remove-orphans

## 🐚 Abre um shell dentro do container (pra debug)
shell:
	docker compose -f $(COMPOSE_FILE) exec app sh

lint:
	uv run black src/ tests/

lint-check:
	uv run black . --check

lint-dry:
	uv run black . --diff --color
