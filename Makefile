CONTAINERS_PATH=container
CONTAINER_GENERATOR_PATH=${CONTAINERS_PATH}/generator
CONTAINER_FINAL_MODEL_PATH=${CONTAINERS_PATH}/final_model
CONTAINER_CONSUMER_PATH=${CONTAINERS_PATH}/consumer
PYTHON_PATH=python
PYTHON_GENERATOR_PATH=${PYTHON_PATH}/generator
PYTHON_FINAL_MODEL_PATH=${PYTHON_PATH}/final_model
PYTHON_CONSUMER_PATH=${PYTHON_PATH}/consumer
SMA_CONSUMER_NAME=sma_consumer
SMA_GENERATOR_NAME=sma_generator
SMA_FINAL_MODEL_NAME=sma_final_model

build_consumer:
	-rm ${PYTHON_CONSUMER_PATH}/users.db
	-cp -rf ${PYTHON_CONSUMER_PATH} ${CONTAINER_CONSUMER_PATH}/consumer
	-docker build -t ${GCR_REGION}/${GCP_PROJECT}/sma_consumer ${CONTAINER_CONSUMER_PATH}
	-rm -rf ${CONTAINER_CONSUMER_PATH}/consumer

build_generator:
	-cp -rf ${PYTHON_GENERATOR_PATH} ${CONTAINER_GENERATOR_PATH}/generator
	-docker build -t ${GCR_REGION}/${GCP_PROJECT}/sma_generator ${CONTAINER_GENERATOR_PATH}
	-rm -rf ${CONTAINER_GENERATOR_PATH}/generator

build_final_model:
	-cp -rf ${PYTHON_FINAL_MODEL_PATH} ${CONTAINER_FINAL_MODEL_PATH}/final_model
	-docker build -t ${GCR_REGION}/${GCP_PROJECT}/sma_final_model ${CONTAINER_FINAL_MODEL_PATH}
	-rm -rf ${CONTAINER_FINAL_MODEL_PATH}/final_model

build_all: build_generator build_consumer

run_consumer:
	-docker run -d --name ${SMA_CONSUMER_NAME} --env-file .env --rm -p 8002:8002 --env PORT=8002 ${GCR_REGION}/${GCP_PROJECT}/sma_consumer

run_generator:
	-docker run -d --name ${SMA_GENERATOR_NAME} --env-file .env --rm -p 8001:8001 --env PORT=8001  ${GCR_REGION}/${GCP_PROJECT}/sma_generator

run_final_model:
	-docker run -d --name ${SMA_FINAL_MODEL_NAME} --env-file .env --rm -p 8001:8001 --env PORT=8001  ${GCR_REGION}/${GCP_PROJECT}/sma_final_model

stop_containers:
	-docker stop ${SMA_GENERATOR_NAME}
	-docker stop ${SMA_CONSUMER_NAME}
	-docker stop ${SMA_FINAL_MODEL_NAME}

up_consumer:
	-cp -rf ${PYTHON_CONSUMER_PATH} ${CONTAINER_CONSUMER_PATH}/consumer
	-gcloud run deploy --env-vars-file .env-consumer.yaml --cpu=2 --memory=2G --max-instances=1 --source=/home/lico/code/gentacs/SMA/container/consumer --region=europe-southwest1
	-rm -rf ${CONTAINER_CONSUMER_PATH}/consumer
