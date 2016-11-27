# -*- coding: utf-8 -*-
"""
Walk a directory tree starting at the --dir paramenter. Expand each zip 
file and Build a TSV table of tag from all extracted dcm files. Specific 
tags to collect are listed in tags file 

Output result to standard out.
"""
from __future__ import print_function

from process_dcm import loadTagNames, outputFieldNames, collectDicomTags
import os,sys
import argparse
import zipfile
from os.path import join
import time

def scanZipFiles(args):
    dcmFileCount = 0
    zipFileCount = 0

    tagNames=loadTagNames(args)

    outputFieldNames(args, tagNames)
    
    for scrroot, scrdirs, scrfiles in os.walk(args.dir):
        for zip_file in scrfiles:
            if args.verbosity>=2:
                print("Extracting from file: ",zip_file,file=sys.stderr)
            filename, extension = os.path.splitext(zip_file)
            if extension == '.zip':
                zipFileCount += 1
                try:
                    #Open the file and extract the .dcm files to scratch directory                                                                                                   
                    zf = zipfile.ZipFile(join(scrroot,zip_file))
                    zf.extractall(args.scratch)

                    for dcmroot, dcmdirs, dcmfiles in os.walk(args.scratch):
                        for dcmfile in dcmfiles:
                            filename, extension = os.path.splitext(dcmfile)
                            if extension == '.dcm':
                                dcmFileCount+=1
                                collectDicomTags(args,tagNames,dcmroot,dcmfile,zip_file)
                            os.remove(join(dcmroot,dcmfile))
                    zf.close()
                except (zipfile.BadZipfile):
                    print("Error opening file {} ".format(zip_file),file=sys.stderr)
    return (dcmFileCount, zipFileCount)

if __name__ == '__main__':    
    parser = argparse.ArgumentParser(description="Build DICOM image metadata table")
    parser.add_argument ( "-v", "--verbosity", action="count",default=0,help="increase output verbosity" )
    parser.add_argument ( "-d", "--dir", type=str, help="path to directory containing DICOM files", 
                          default='./images')
    parser.add_argument ( "-t", "--tags", type=str, help="path to file contain tag names", 
                          default='./tags.txt')
    parser.add_argument ( "-s", "--scratch", type=str, help="path to scratch directory", 
                          default='./scratch')
    args = parser.parse_args()
    
    t0 = time.time()
    fileCount = scanZipFiles(args)
    t1 = time.time()
    
    if args.verbosity>0:
        print("{} zip files and {} dcm files process in {} seconds".format(fileCount[1],fileCount[0],t1-t0),file=sys.stderr)

   

            
