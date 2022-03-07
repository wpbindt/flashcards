# these will speed up builds, for docker-compose >= 1.25
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1


DOCKER_COMPOSE_TEST=docker-compose -p flashcards_test -f docker-compose.yml
DOCKER_COMPOSE_TEST_RUN=${DOCKER_COMPOSE_TEST} run --rm
DOCKER_COMPOSE_TEST_KILL=${DOCKER_COMPOSE_TEST} kill

DOCKER_COMPOSE_E2E=${DOCKER_COMPOSE_TEST} -f docker-compose.e2e.yml


.PHONY: all
all: down build up

.PHONY: build
build:
	docker-compose build --quiet

.PHONY: up
up:
	docker-compose up -d --quiet-pull

.PHONY: down
down:
	docker-compose down --remove-orphans

.PHONY: test
test: linting mypy unit-tests

.PHONY: unit-tests
unit-tests:
	${DOCKER_COMPOSE_TEST_RUN} --no-deps flashcards pytest /tests/unit

.PHONY: mypy
mypy:
	${DOCKER_COMPOSE_TEST_RUN} --no-deps flashcards mypy --install-types --non-interactive /tests /flashcards

.PHONY: linting
linting:
	${DOCKER_COMPOSE_TEST_RUN} --no-deps flashcards flake8 --max-line-length 120 /tests /flashcards
