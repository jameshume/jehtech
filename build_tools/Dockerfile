FROM node

RUN npm install @node-minify/core @node-minify/cli @node-minify/cssnano @node-minify/uglify-es -g
RUN npm install @babel/core @babel/cli -g
RUN npm install @babel/preset-env -g
RUN npm install esm -g
RUN npm install mathjax@3 -g
RUN npm install yargs@3 -g
RUN npm install html-linter -g
RUN npm install html-validate -g
RUN apt-get update
RUN apt-get install -y python3-pip
RUN pip3 install lxml pillow pyhash awscli boto3 markdown
