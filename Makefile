build.vs-code:
	docker compose -f docker-compose.local.yml build vs-code

build.notebook:
	docker compose -f docker-compose.local.yml build notebook

build.all:
	docker compose -f docker-compose.local.yml build

run.vscode:
	docker compose -f docker-compose.local.yml up --remove-orphans -d vscode-server

run.notebook:
	docker compose -f docker-compose.local.yml up --remove-orphans notebook
