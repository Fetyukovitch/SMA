CONTAINERS_PATH=container
CONTAINER_GENERATOR_PATH=${CONTAINERS_PATH}/generator
CONTAINER_CONSUMER_PATH=${CONTAINERS_PATH}/consumer
PYTHON_PATH=python
PYTHON_GENERATOR_PATH=${PYTHON_PATH}/generator
PYTHON_CONSUMER_PATH=${PYTHON_PATH}/consumer
SMA_CONSUMER_NAME=sma_consumer
SMA_GENERATOR_NAME=sma_generator

build_consumer:
	-cp -rf ${PYTHON_CONSUMER_PATH} ${CONTAINER_CONSUMER_PATH}/consumer
	-docker build -t ${GCR_REGION}/${GCP_PROJECT}/sma_consumer ${CONTAINER_CONSUMER_PATH}
	-rm -rf ${CONTAINER_CONSUMER_PATH}/consumer

build_generator:
	-cp -rf ${PYTHON_GENERATOR_PATH} ${CONTAINER_GENERATOR_PATH}/generator
	-docker build -t ${GCR_REGION}/${GCP_PROJECT}/sma_generator ${CONTAINER_GENERATOR_PATH}
	-rm -rf ${CONTAINER_GENERATOR_PATH}/generator

build_all: build_generator build_consumer

run_consumer:
	-docker run -d --name ${SMA_CONSUMER_NAME} --env-file .env --rm -p 8000:8000 ${GCR_REGION}/${GCP_PROJECT}/sma_consumer

run_generator:
	-docker run -d --name ${SMA_GENERATOR_NAME} --env-file .env --rm -p 8001:8001 --env PORT=PORT=8001  ${GCR_REGION}/${GCP_PROJECT}/sma_generator

stop_containers:
	-docker stop ${SMA_GENERATOR_NAME}
	-docker stop ${SMA_CONSUMER_NAME}
