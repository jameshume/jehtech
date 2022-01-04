"""
The S3 sync will upload files that are newer than those in the bucket, which is great
except when JEHTech is checked out and updated on multiple machines or JEHTech is rebuilt
from scratch for whatever reason. To figure out which files are truely different a dictionary
of file paths to hashes is kept. One on the server and one locally. Thus, file difference
can be found and only changed files need be uploaded and then synced in CLoudFront.

This module just generates the dictionary and pickles it to the output directory.
"""
import os
import pickle
import sys
from pathlib import Path
import pyhash

def YieldFiles(dirToScan):
    for rootDir, _, files in os.walk(dirToScan):
        for fname in files:
            yield Path(rootDir) / fname
 
def HashFile(file_path):
    # Taken from https://stackoverflow.com/a/55542529
    hasher = pyhash.fnv1_32()
    return hasher(open(file_path, 'rb').read())

def GenerateHashDict(root_dir):
    hash_dict = {}
    for file_path in YieldFiles(root_dir):
        hash_dict[str(file_path.relative_to(root_dir))] = HashFile(file_path)
    return hash_dict

def SaveHashDict(filename, hash_dict):
    with open(filename, 'wb') as handle:
        pickle.dump(hash_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

def LoadHashDict(filename):
     with open(filename, 'rb') as handle:
            return pickle.load(handle)

if __name__ == '__main__':
    if sys.argv[1] == 'create_hash_file':
        SaveHashDict(sys.argv[3], GenerateHashDict(sys.argv[2]))
    elif sys.argv[1] == 'dump_hash_file':
        import pprint
        print(pprint.pformat(LoadHashDict(sys.argv[2])))
    
