
        ##########################################################################################################################
                                                                                                                                
        #  Blazar-Periodocity1: analisi di Fourier delle curve di luce settimanali delle quattro sorgenti Blazar prese in esame  # 
                                                                                                                               
        ##########################################################################################################################
        

#################################
                               
# import dei moduli necessari:  #
                                   
#################################

import sys
import numpy as np
import pandas as pd
from scipy import constants, fft, optimize 
import matplotlib.pyplot as plt
import argparse


#####################################################################
#      Funzione per gestire le  opzioni tramite modulo argparse     #
#####################################################################



def parse_arguments():

    parser = argparse.ArgumentParser(description=' Blazar-Periodocity1 data analysis and plot.',
                                     usage      ='Blazar-Periodocity1.py  --option')

    parser.add_argument('--gplot',      action='store_true',   help='grafici relativi alle curve di luce delle quattro sorgenti')
    parser.add_argument('--FFTplot',    action='store_true',   help='grafici delle FFT delle curve di luce delle quattro sorgenti')
    parser.add_argument('--PSplot',     action='store_true',   help='grafici degli Spettri di Potenza delle curve di luce delle quattro sorgenti')
    parser.add_argument('--Fitplot',    action='store_true',   help='Fit relativi agli Spettri di Potenza e identificazione del rumore')
    parser.add_argument('--PSfilter',   action='store_true',   help='Filtri relativi ai quattro Spettri di Potenza')
    parser.add_argument('--CLSplot',    action='store_true',   help='Generazione di Curve di Luce Sintetiche e calcolo della probabilità del picco di potenza')
    
    return  parser.parse_args(args=None if sys.argv[1:] else ['--help'])


def main_Blazar():

    args = parse_arguments()

    #---------------------------------------------------------------#
    #              Dictionary con sorgenti e files      #
    #---------------------------------------------------------------#

    sorgenti_dict = {

	 "sorgente_1": {

            "nome_file":  "4FGL_J0137.0+4751_weekly_12_27_2024.csv",
	},
 
         "sorgente_2": {

            "nome_file":  "4FGL_J0442.6-0017_weekly_12_27_2024.csv",
	},
 

         "sorgente_3": {

            "nome_file":  "4FGL_J0449.4-4350_weekly_12_27_2024.csv",
        },

	 "sorgente_4": {

            "nome_file":  "4FGL_J1256.1-0547_weekly_12_27_2024.csv",
        },
    }
                
    #----------------------------------------------------------------#
    # Lettura files dei dati e aggiunta del dataframe df a dictionary#
    #----------------------------------------------------------------#

    for sorgente in sorgenti_dict:

        file_blazar = sorgenti_dict[sorgente]["nome_file"]

        df = pd.read_csv(file_blazar)

        sorgenti_dict[sorgente]["df"] = df

 

    print(sorgenti_dict["sorgente_1"]["nomefile"])
    print(sorgenti_dict["sorgente_1"]["df"])

    if args.gplot:
                
     print("Produco i grafici")

    if args.FFTplot:
           print("Produco le FFT")

    if args.PSplot:
           print("Produco gli spettri di potenza")


if __name__ == "__main__":
    main_Blazar()
