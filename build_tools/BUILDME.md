# Build

The build uses a Docker image to eliminate build environment differences and general
dependency differences. Generally built on a Windows machine, untested running in *nix
environment.

Now using docker-compose.

From the `build_tools` directory:

* To run a build of the website do `docker-compose up make`
* To build the container and then do a build of the website do `docker-compose up --build make`

The docker-compose file will do a bind-mount for you so that the root of the jehtech repository is
mapped to `/jehtech` in the Docker image. The `RUN` command will execute a script that will change
directory to `/jehtech/build_tools` and execute `make all`

To deploy to the AWS S3 bucket the `build_tools` folder needs the file `aws_jehtech_uploader_credentials.json`
which will have the following contents:

```
{
    "access_key_id": "your-access-key-id-goes-here",
    "access_key": "your-access-key-goes-here"
}
```

The **access_key is secret: never commit to your repository!**.

To do the deploy from the command line use `docker-compose up upload`.
