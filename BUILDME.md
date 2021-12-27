# WSL Ubuntu 20

# Build System
The build system now assumes a Linux (like) environment. For me, this normally means WSL. The
Makefile will take the source from the "src" directory and create a "built" directory containing all
of the required artifacts.

The HTML files have the following done to "compile" them:
	1. The _links.html content is inserted into the page,
	2. CSS/JS link placeholders are replaced by actual HTML tags that link to the correct places,
	3. The IMG_DIR tag is replaced so that it "points" to the built images directory (images are
	   watermarked in the built directory, assuming they are JEHTech originals).