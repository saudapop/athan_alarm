dev:
	docker-compose -f docker-compose.dev.yml up -d --build && \
	cd client && \
	npm i && \
	npm start;
prod:
	docker-compose up -d --build
teardown:
	docker-compose down --remove-orphans && docker rmi $(docker images -q -f dangling=true)
