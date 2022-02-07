FROM node

RUN mkdir /scripts
COPY docker_script.sh /scripts

RUN npm install \
        @node-minify/core \
        @node-minify/cli \
        @node-minify/cssnano \
        @node-minify/uglify-es \
        @babel/core @babel/cli \
        @babel/preset-env \
        esm \
        mathjax@3 \
        yargs@3 \
        html-linter \
        html-validate -g \
    && apt-get update \
    && apt-get install -y python3-pip vim \
    && pip3 install lxml pillow pyhash awscli boto3 markdown

ENTRYPOINT [ "bash", "/scripts/docker_script.sh" ]