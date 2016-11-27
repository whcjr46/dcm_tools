# -*- coding: utf-8 -*-
"""
Walk a directory tree starting at the --dir paramenter. Build a TSV table 
of tag values in each dcm file. Specific tags to collect 
are listed in tags file.

Output result to standard out.
"""
from __future__ import print_function
from process_dcm import loadTagNames, outputFieldNames, collectDicomTags
import os,sys
import argparse
from os.path import join
import time

def scanDCMFiles(args):
    dcmFileCount = 0

    tagNames=loadTagNames(args)

    outputFieldNames(args, tagNames)
    
    for dcmroot, dcmdirs, dcmfiles in os.walk(args.dir):
        zip_file=dcmroot.rpartition('/')[2]+'.zip'
        for dcmfile in dcmfiles:
            filename, extension = os.path.splitext(dcmfile)
            if extension == '.dcm':
                dcmFileCount+=1
                collectDicomTags(args,tagNames,dcmroot,dcmfile,zip_file)
    return dcmFileCount

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
    fileCount = scanDCMFiles(args)
    t1 = time.time()
    
    if args.verbosity>0:
        print("{} file process in {} seconds".format(fileCount,t1-t0),file=sys.stderr)

   

            
