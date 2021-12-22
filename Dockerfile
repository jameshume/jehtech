FROM node

RUN npm install uglify-js   -g
RUN npm install @babel/core @babel/cli  -g
RUN npm install @babel/preset-env -g
RUN npm install mathjax@3 -g
RUN npm install yargs@3 -g
RUN apt-get update
RUN apt-get install -y python3-pip
RUN pip3 install lxml
