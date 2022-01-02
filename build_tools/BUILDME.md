# Build

The build uses a Docker image to elliminate build environment differences and general
dependency differences. Generally build on a Windows machine, untested running in *nix
environment.

To build the container, from the `build_tools` directory type:

```
docker image build -t jehtech:vX.Y .
```

To build the site, from the root of the repository checkout, assuming in the following
example that it has been checkout out to `C:\Users\Brian\Documents\jehtech2`, type:

```
docker container run --rm -it -v //c/Users/brian/Documents/jehtech2:/jehtech jehtech:v1.0 bash
```

