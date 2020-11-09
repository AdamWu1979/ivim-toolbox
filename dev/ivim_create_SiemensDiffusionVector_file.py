#!/usr/bin/env python3.6

import argparse
import os
from datetime import datetime
import numpy as np


def main(bvalsRequested, nbRep, unitVectDir, oFname):
    """Main."""

    # create file
    fileObj = open(oFname+'.txt', 'w')

    # write heading
    username = os.getlogin()
    fileObj.write('#-------------------------------------------------------------------------------\n'
                '# DWI Siemens orientation file for IVIM\n'
                '# Author: '+username+'\n'
                '# Date: '+datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")+'\n'
                '# \n'
                '# If run with b = '+str(max(bvalsRequested))+', obtained b-values will be (s/mm2):\n'
                '# '+str(bvalsRequested)+'\n'
                '# Number of b-values: '+str(len(bvalsRequested))+'\n'
                '# Number of repetitions: '+str(nbRep)+'\n'
                '# Direction: '+str(unitVectDir)+'\n'
                '# Do not alternate positive and negative diffusion encoding directions\n'
                '#-------------------------------------------------------------------------------\n\n')

    # write characteristics of the diffusion file that will be read by the scanner
    fileObj.write('[directions='+str(len(bvalsRequested)*nbRep)+']\nCoordinateSystem = prs\nNormalisation = none\n')
    # NOT SUPPORTED ON VB17: fileID.write('Comment = To be run with b='+str(max(bvalsRequested))+'s/mm2\n')

    # compute vectors norms
    vectNorm = np.sqrt(bvalsRequested/max(bvalsRequested))

    # normalize unity vector to be sure (and get it as row vector)
    unitVectDir = unitVectDir/np.sqrt(np.sum(unitVectDir**2))

    # compute vectors to be written in the diffusion vector (requested norm from b-values * the direction)
    diff_vectors = np.tile(vectNorm, (3, 1)).T * np.tile(unitVectDir, (len(bvalsRequested), 1))

    # write vectors in file
    bvalsWritten = []  # matrix to record written b-values (for debugging)
    for i_vect in range(len(bvalsRequested)):
        for i_rep in range(nbRep):

            sign = 1
            fileObj.write('Vector[{:d}] = ( {:1.8f}, {:1.8f}, {:1.8f} )\n'.format(i_rep + i_vect*nbRep, sign*diff_vectors[i_vect, 0], sign*diff_vectors[i_vect, 1], sign*diff_vectors[i_vect, 2]))
            bvalsWritten.append(sign*bvalsRequested[i_vect])  # record written b-value for debugging

    # all done
    fileObj.close()
    print('\n>>> Diffusion vector file saved to: {}.txt'.format(oFname))


# ==========================================================================================
if __name__ == "__main__":

    # parse arguments
    parser = argparse.ArgumentParser(description='This program produces a diffusion vector file with the requested '
                                                 'diffusion-encoding directions and b-values and number of repetitions '
                                                 'per b-value to be used on Siemens MRI scanners in "free" diffusion mode.')

    optionalArgs = parser._action_groups.pop()
    requiredArgs = parser.add_argument_group('required arguments')

    requiredArgs.add_argument('-b', dest='bvalsRequested', help='List (separate items by commas) of b-values desired.', type=str, required=True)
    requiredArgs.add_argument('-r', dest='nbRep', help="Number of repetitions of each b-value.", type=int, required=True)
    requiredArgs.add_argument('-v', dest='unitVectDir', help="List (separate items by commas) of coordinates of a vector of norm 1 giving the desired diffusion gradient direction.", type=str, required=True)
    requiredArgs.add_argument('-o', dest='oFname', help="Output file name.", type=str, required=True)

    parser._action_groups.append(optionalArgs)

    args = parser.parse_args()

    # print citation
    print('\n\n'
          '\n****************************** <3 Thank you for using our toolbox! <3 ***********************************'
          '\n********************************* PLEASE CITE THE FOLLOWING PAPER ***************************************'
          '\nLévy S, Rapacchi S, Massire A, et al. Intravoxel Incoherent Motion at 7 Tesla to quantify human spinal '
          '\ncord perfusion: limitations and promises. Magn Reson Med. 2020;00:1-20. https://doi.org/10.1002/mrm.28195'
          '\n*********************************************************************************************************'
          '\n\n')

    # run main
    main(bvalsRequested=np.array(args.bvalsRequested.split(','), dtype=float), nbRep=args.nbRep, unitVectDir=np.array(args.unitVectDir.split(','), dtype=float), oFname=args.oFname)



