# Base image
FROM public.ecr.aws/lambda/python:3.9
# #public.ecr.aws/lambda/python:3.9 
# #python:3.9

# Set working directory
# WORKDIR /app

# RUN /usr/local/bin/python -m pip install --upgrade pip

# Copy files
COPY app.py ${LAMBDA_TASK_ROOT}
COPY best.pt ${LAMBDA_TASK_ROOT}
COPY requirements.txt .

# Install dependencies
# sudo apt install libopenblas-dev
# RUN sudo apt-get update && apt-get install -y cmake
# RUN  sudo apt install libopenblas-dev
# RUN yum -y install gcc gcc-c++ make
# # RUN pip3 install --upgrad pip
# RUN pip3 install cmake
# RUN pip3 install dlib
#--upgrade dlib
# RUN pip install -r requirements.txt
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# RUN aws configure set aws_access_key_id "dummy"
# RUN aws configure set aws_secret_access_key "dummy"
# RUN aws configure set region "us-east-1"
# RUN aws configure set output ""

# Run the application
# ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "app.handler" ]


# EXPOSE 8000
# ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-", "--timeout", "120"]
# CMD ["app:app"]