
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
            
           flux_values = []

           upper_count = 0

           Energy_flux = sorgenti_dict[sorgente]['df']['Energy Flux [0.1-100 GeV](MeV cm-2 s-1)']

           time = sorgenti_dict[sorgente]['df']['Julian Date']


           for valore in Energy_flux:

                s = str(valore).strip()

                if s == '-':

                  flux_values.append(np.nan)

                elif s.startswith('<'):
			
                    upper_count += 1

                    try:

                        flux_values.append(float(s[1:].strip()))

                    except:

                        flux_values.append(np.nan)
                else:

                    try:

                       flux_values.append(float(s))

                    except:

                        flux_values.append(np.nan)

           flux = np.array(flux_values, dtype = float)

           mask = np.isfinite(time) & np.isfinite(flux)
       
           time = time[mask]
        
           flux = flux[mask] 


           ax.plot(time, flux, 'o-', color=colori,markersize=3, linewidth=1, label=sorgente)
            
           ax.legend(loc='upper right')

           ax.set_ylabel("Energy Flux (log-scale)")

           ax.set_yscale('log')
            
           

           total_points = len(flux)

           percentuale = (upper_count / total_points * 100) 

           print(sorgente)

           print(total_points,":punti totali")

           print(upper_count, ":upper limits")

           print( "percentuale:", percentuale, "%")


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










