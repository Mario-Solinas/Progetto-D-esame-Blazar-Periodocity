
        ##########################################################################################################################
                                                                                                                                
        #  Blazar-Periodocity_weekly: analisi di Fourier delle curve di luce settimanali delle quattro sorgenti Blazar prese in esame  # 
                                                                                                                               
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
    #                 Dictionary con sorgenti e files               #
    #---------------------------------------------------------------#

    sorgenti_dict = {

        "sorgente_1": {

            "nome_file": "dati_csv/4FGL_J0137.0+4751_weekly_12_27_2024.csv",
        },

        "sorgente_2": {

            "nome_file": "dati_csv/4FGL_J0442.6-0017_weekly_12_27_2024.csv",
        },

        "sorgente_3": {

            "nome_file": "dati_csv/4FGL_J0449.4-4350_weekly_12_27_2024.csv",  
        },

        "sorgente_4": {

            "nome_file": "dati_csv/4FGL_J1256.1-0547_weekly_12_27_2024.csv",
        },

    }

    #----------------------------------------------------------------#
    # Lettura files dei dati e aggiunta del dataframe df a dictionary#
    #----------------------------------------------------------------#

    for sorgente in sorgenti_dict:

        file_blazar = sorgenti_dict[sorgente]["nome_file"]

        df = pd.read_csv(file_blazar)

        sorgenti_dict[sorgente]["df"] = df


    #-------------------------------------------------------------#
    #                 Grafici delle Curve di Luce                 #   
    #-------------------------------------------------------------#

    if args.gplot == True:
                
       fig, axes = plt.subplots(4, 1, figsize=(8, 9), sharex=True)

       colors = ['#FF8C00', '#1E90FF', '#32CD32', '#8A2BE2']      
 
       for indx, sorgente in enumerate(sorgenti_dict):

            ax = axes[indx]

            colori = colors[indx]

            normal_flux = []

            normal_time = []

            upper_flux = []   
         
            upper_time = []

            Energy_flux = sorgenti_dict[sorgente]['df']['Energy Flux [0.1-100 GeV](MeV cm-2 s-1)']

            time = sorgenti_dict[sorgente]['df']['Julian Date']

            for up, valore in  zip(time, Energy_flux):

                s = str(valore).strip()

                if s == '-':

                   normal_flux.append(np.nan)

                   normal_time.append(up)

                elif s.startswith('<'):

                     try:

                        upper_flux.append(float(s[1:].strip()))

                        upper_time.append(up) 

                     except:

                        upper_flux.append(np.nan)
 
                else:

                     try:

                        normal_flux.append(float(s))

                        normal_time.append(up) 

                     except:

                        normal_flux.append(np.nan)

                    

            flussi_normali = np.array(normal_flux, dtype = float)

            flussi_limiti = np.array(upper_flux, dtype = float)

            tempi_normali = np.array(normal_time, dtype = float)

            tempi_limiti = np.array(upper_time, dtype = float)



            mask1 = np.isfinite(tempi_normali ) & np.isfinite(flussi_normali)
       
            tempi_normali = tempi_normali[mask1]
        
            flussi_normali = flussi_normali [mask1] 

            mask2 = np.isfinite(tempi_limiti) & np.isfinite( flussi_limiti)
       
            tempi_limiti =  tempi_limiti[mask2]
        
            flussi_limiti =  flussi_limiti [mask2] 
            

            if len(tempi_normali) > 0:         

               ax.plot(tempi_normali, flussi_normali , linestyle='', marker = 'o', markersize=6,  color=colori, label=sorgente)

            if len(tempi_limiti) > 0:

               ax.plot(tempi_limiti, flussi_limiti  , color='red', linestyle='', marker='v', markersize=5,label='Upper limits')

             
             
            ax.legend(loc='upper right')

               
               
            ax.set_ylabel("Energy Flux (log-scale)")

            ax.set_yscale('log')

            
 
            total_points = len(flussi_normali) + len(flussi_limiti)

            percentuale = (len(flussi_limiti) / total_points * 100) 

            print(sorgente)

            print(total_points,"punti totali")

            print(len(flussi_limiti) , "upper limits")

            print( "percentuale", percentuale, "%")

            ax.set_title(sorgente)

       axes[-1].set_xlabel('Julian Date')

       plt.suptitle('Blazar Light Curves - weekly', fontsize=12)

       plt.tight_layout()

       plt.show()
       
    if args.FFTplot == True:

       print("Produco le FFT")

    if args.PSplot == True:

       print("Produco gli spettri di potenza")


if __name__ == "__main__":
    main_Blazar()










