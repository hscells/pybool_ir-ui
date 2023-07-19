docker-build:
	docker build --tag "pbir-ui" -f docker/Dockerfile .

docker-run:
	docker run --rm -it --platform linux/x86_64 \
	 -p 8080:8501 \
	 -v ./.env:/workspace/.env \
	 -v ./config-pubmed.toml:/workspace/config-pubmed.toml \
	 -v ./index-pubmed:/workspace/index-pubmed \
	 pbir-ui