# -*- coding: utf-8 -*-
"""
Walk a directory tree starting at the root paramenter. Count the occurence of 
tags in all DICOM files found.

Output result to standard out.

Usage:  python countTags.py root [-v]

-v (optional): Verbose mode, prints extra stuff

"""
from __future__ import print_function

import os,sys
#import CountAFile
import zipfile
from os.path import join
import time
import dicom
import pickle
#from dicom.tag import Tag

MAXVALS = 50
IGNOREDVRS = ['FL','FD','OB','OD','OF','OL','OW','UC','UN','SQ']

def addValue(tag,elementValue):
    if tag[1] not in IGNOREDVRS:
        if tag[4].get(elementValue) == None:
            if tag[3]<MAXVALS:
                tag[4][elementValue] = 1
                tag[3] += 1
        else:
            tag[4][elementValue] += 1
    

def countDicomTags(dcmfile, tags, verbose, zip_file):
    if verbosity>=3 :
        print("Processing file: ", dcmfile, file=sys.stderr)
    dataset = dicom.read_file(dcmfile, stop_before_pixels=True)
    try:
        for dataelement in dataset.iterall(): 
            de = dataelement
            #print(tags)
            
            if (de.tag.group%2 ==0): #Ignore private tags
                elementValue = str(de.value)
#                elementValue = (de.value)
                if tags.get(de.tag) == None:
                    if verbosity>=3:
                        print("**Adding element: ",de,file=sys.stderr)          
                    if de.VR not in IGNOREDVRS:
                        tags[de.tag] = [de.description(),de.VR,1,1,{elementValue:1}]
                    else:
                        tags[de.tag] = [de.description(),de.VR,1,0,{"":0}]
            
                else:
                    tags[de.tag][2] += 1
                    addValue(tags[de.tag], elementValue)
    except ValueError:
        print("Could not convert string to float in file {} from {}".format(dcmfile,zip_file),file=sys.stderr)


def outputResults(fileCount):
    if verbosity>=1:
        print ("Files processed: ", fileCount)
    print("Group;Element;Description;VR;Tag Count;Value Count ")
    for tag in tags:
        print("{0:#05x};{1:#05x};{2:s};{3:s};{4:d};{5:d}".format(tag.group,tag.element,tags[tag][0],tags[tag][1],tags[tag][2],tags[tag][3]),end="")
        for elementValue in tags[tag][4]:
            print(";{0:s}({1:d})".format(elementValue,tags[tag][4][elementValue]),end="")
        print("")

def saveTags(saveto='savedTagstruct.txt'):
    afile = open(saveto, 'wb')
    pickle.dump(tags, afile)
    afile.close()
    

def scanAll(path,verbosity,tags):
    fileCount=0
    for scrroot, scrdirs, scrfiles in os.walk(sys.argv[1]):
        for zip_file in scrfiles:
            if verbosity>=2:
                print("Extracting from file: ",zip_file,file=sys.stderr)
            filename, extension = os.path.splitext(zip_file)
            if extension == '.zip':
                try:
                    #Open the file and extract the .dcm file                                                                                                   
                    zf = zipfile.ZipFile(join(scrroot,zip_file))
                except (zipfile.BadZipfile):
                    print("Error opening file {} ".format(zip_file),file=sys.stderr)
                else:
                    zf = zipfile.ZipFile(join(scrroot,zip_file))
                    zf.extractall(scratch)

                    for dcmroot, dcmdirs, dcmfiles in os.walk(scratch):
                        for dcmfile in dcmfiles:
                            filename, extension = os.path.splitext(dcmfile)
                            if extension == '.dcm':
                                fileCount+=1
                                countDicomTags(join(dcmroot,dcmfile),tags,verbosity,zip_file)
                            os.remove(join(dcmroot,dcmfile))
                    zf.close()
                    if verbosity>=4:
                        outputResults(fileCount)
    return fileCount

if __name__ == '__main__':
    verbosity=0
    tags={}
#    fileCount=0
    scratch = './scratch'

    if not 1 < len(sys.argv) < 4:
        print(__doc__)
        sys.exit()
    path = sys.argv[1]

    # Verbose mode:
    if len(sys.argv) == 3:
        if sys.argv[2] == "-v":  # user asked for all info
            verbosity=1
        elif sys.argv[2] == "-vv":
            verbosity=2
        elif sys.argv[2] == "-vvv":
            verbosity=3
        elif sys.argv[2] == "-vvvv":
            verbosity=4
        else:  # unknown command argument
            print(__doc__)
            sys.exit()

    t0 = time.time()
    fileCount = scanAll(path, verbosity, tags)
    t1 = time.time()
    
    if verbosity>=1:
        print("Elapsed time: {} seconds".format(t1-t0))

    saveTags()
    outputResults(fileCount)
   

            
