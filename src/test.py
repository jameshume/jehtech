import subprocess
#args=["java", "-jar", "yuicompressor-2.4.8.jar", "css\\jeh-tech.css", "-o", "jonh22.css"]
args=["java", "-jar", "yuicompressor-2.4.8.jar", "-o", "css\\jonh33.css", "css\\jddeh-tech.css"]
args=["java", "-jar", "yuicompressor-2.4.8.jar", "-o", "__deployed\\junk.css", "__deployed\\jeh-monolith.css.uncompressed"]#"__deployed\\jeh-monolith.css", "__deployed\\jeh-monolith.css.uncompressed"]
subprocess.call(args)
