FROM --platform=linux/x86_64 ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive

# Install all the Python and Java requirements.
RUN apt-get update
RUN apt-get install --yes software-properties-common wget
RUN apt-get update
RUN wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public | apt-key add -
RUN echo "deb https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | tee /etc/apt/sources.list.d/adoptium.list
RUN apt-get update
RUN apt-get install --yes git ca-certificates-java temurin-17-jdk python3-pip
ARG JCC_JDK=/usr/lib/jvm/temurin-17-jdk-amd64

# Create our workspace.
RUN mkdir -p /workspace

# Install just lucene.
RUN pip install --upgrade pip
RUN git clone https://github.com/hscells/pylucene-packaged.git
RUN cd pylucene-packaged && pip install dist/lucene-9.4.1-cp310-cp310-linux_x86_64.whl && cd ..

# Install Python dependencies.
COPY requirements.txt /workspace/requirements.txt
RUN tail -n +2 /workspace/requirements.txt > /workspace/requirements1.txt
RUN cat /workspace/requirements1.txt
RUN pip install -r /workspace/requirements1.txt

# Add the rest of the files.
COPY *.py /workspace/
COPY .streamlit/config.toml /root/.streamlit/config.toml

# Who knows why this is necessary.
ARG LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/python3.10/dist-packages/libjcc3.so
RUN cp /usr/local/lib/python3.10/dist-packages/libjcc3.so /usr/lib/
RUN cp /usr/local/lib/python3.10/dist-packages/libjcc3.so /usr/lib64/

# Run the application.
WORKDIR /workspace
CMD ["streamlit", "run", "app.py"]