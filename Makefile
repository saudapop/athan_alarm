dev:
	docker-compose up -d --build && \
	cd client && \
	npm i && \
	npm start;
teardown:
	docker-compose down --remove-orphans && docker rmi $(docker images -q -f dangling=true)
