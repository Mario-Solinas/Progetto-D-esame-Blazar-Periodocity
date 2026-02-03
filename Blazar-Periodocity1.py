
         #Blazar-Periodocity1: analisi di Fourier delle curve di luce settimanali delle quattro sorgenti Blazar prese in esame 

#import dei moduli necessari:

import sys, os
import numpy as np
import pandas as pd
from scipy import constants, fft, optimize
import matplotlib.pyplot  as plt

import argparse


def parse_arguments():

    parser = argparse.ArgumentParser(description='Plot and fit noise data.',
                                     usage      ='python3 lightcurve_fft.py  --option')
    parser.add_argument('--lc',        action='store_true',    help='Plot input Light Curves')
    parser.add_argument('--psplot',    action='store_true',    help='Plots about  FFT and Power Spectrum')
    parser.add_argument('--psfit',     action='store_true',    help='Perform and Plot Power Spectrum Fit')
    parser.add_argument('--psfilter',  action='store_true',    help='Apply and Plot Power Spectrum Filter')

    
    return  parser.parse_args(args=None if sys.argv[1:] else ['--help'])
