CONTAINERS_PATH=container
CONTAINER_GENERATOR_PATH=${CONTAINERS_PATH}/generator
CONTAINER_CONSUMER_PATH=${CONTAINERS_PATH}/consumer
PYTHON_PATH=python
PYTHON_GENERATOR_PATH=${PYTHON_PATH}/generator
PYTHON_CONSUMER_PATH=${PYTHON_PATH}/consumer


build_consumer:
	-cp -rf ${PYTHON_CONSUMER_PATH} ${CONTAINER_CONSUMER_PATH}/consumer
	-docker build -t ${GCR_REGION}/${GCP_PROJECT}/sma_consumer ${CONTAINER_CONSUMER_PATH}
	-rm -rf ${CONTAINER_CONSUMER_PATH}/consumer

build_generator:
	-cp -rf ${PYTHON_GENERATOR_PATH} ${CONTAINER_GENERATOR_PATH}/generator
	-docker build -t ${GCR_REGION}/${GCP_PROJECT}/sma_generator ${CONTAINER_GENERATOR_PATH}
	-rm -rf ${CONTAINER_GENERATOR_PATH}/generator

build_all: build_generator build_consumer
