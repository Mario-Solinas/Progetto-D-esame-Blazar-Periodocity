###############################################################################################################################
          
#  Blazar-Periodocity_monthly: analisi di Fourier delle curve di luce mensili delle quattro sorgenti Blazar prese in esame # 
                                                                                                                                     
###############################################################################################################################
        

#################################

# import dei moduli necessari:  #

#################################

import sys
import numpy as np
import pandas as pd
from scipy import constants, fft , optimize
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import argparse


#####################################################################
#            Funzioni integrative  e di supporto                    #
#####################################################################


#####################################################################
#      Funzione per gestire le  opzioni tramite modulo argparse     #
#####################################################################

def parse_arguments():
        
    parser = argparse.ArgumentParser(description=' Blazar-Periodocity_montly data analysis and plot.',
                                     usage      ='Blazar-Periodocity_montly.py  --option')
    parser.add_argument('--gplot',      action='store_true',   help='grafici relativi alle curve di luce delle quattro sorgenti')
    parser.add_argument('--FFT_PSplot', action='store_true',   help='calcolo della FFT e grafici degli Spettri di Potenza delle curve di luce delle quattro sorgenti') 
    parser.add_argument('--CLS',        action='store_true',   help='Generazione di Curve di Luce Sintetiche e calcolo della probabità  del picco di potenza')
    parser.add_argument('--Fit_Blazar', action='store_true',   help='Fit relativi agli Spettri di Potenza e identificazione del rumore')

    return  parser.parse_args(args=None if sys.argv[1:] else ['--help'])


#----------------------------------------------------------------#
#     Funzione che separa i flux_data dagli upper limits         #
#----------------------------------------------------------------#

def processa_sorgente(df):

            # df: dataframe relativo a ciascuna sorgente

            #creo le liste per differenziare i dati "normali" dagli upper limits

            normal_flux = []

            normal_time = []

            upper_flux = []   
         
            upper_time = []

            #memorizzo i dataframe dei flussi e dei tempi 

           # Energy_flux = sorgenti_dict[sorgente]['df']['Energy Flux [0.1-100 GeV](MeV cm-2 s-1)']

            #time = sorgenti_dict[sorgente]['df']['Julian Date']

            #converto i valori di flusso in stringhe al fine di individuare i dati "-" , NaN e "<"

            for up, valore in  zip(df['Julian Date'], df['Energy Flux [0.1-100 GeV](MeV cm-2 s-1)']):

                s = str(valore).strip()

                if s == '-':

                   normal_flux.append(np.nan)

                   normal_time.append(up)

                elif s.startswith('<'):

                     try:
                        # elimino "<" e converto l'upper limit in float

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

            #converto in array le liste  con i dati selezionati (NaN e float)         

            flussi_normali = np.array(normal_flux, dtype = float)

            flussi_limiti = np.array(upper_flux, dtype = float)

            tempi_normali = np.array(normal_time, dtype = float)

            tempi_limiti = np.array(upper_time, dtype = float)

             

            #eseguo la maschera sui 4 array, selezionando solo dati reali (eliminazione dei NaN)

            mask1 = np.isfinite(tempi_normali ) & np.isfinite(flussi_normali)
       
            tempi_normali = tempi_normali[mask1]
        
            flussi_normali = flussi_normali[mask1]

            mask2 = np.isfinite(tempi_limiti) & np.isfinite( flussi_limiti)
       
            tempi_limiti =  tempi_limiti[mask2]
        
            flussi_limiti =  flussi_limiti [mask2] 
            
            #restituisce il dizionario con gli array corrispondenti alle chiavi stringhe aventi stesso nome

            return {'tempi_normali': tempi_normali, 'flussi_normali': flussi_normali,

                    'tempi_limiti': tempi_limiti, 'flussi_limiti': flussi_limiti }
            


#----------------------------------------------------------------#
#     Funzione per il calcolo dei p.t totali, upper limits e %   #
#----------------------------------------------------------------#

  
def calcola_upper(flussi_normali, flussi_limiti, sorgente=""):

        total_points = len(flussi_normali) + len(flussi_limiti)
            
        if total_points >0:

           percentuale = (len(flussi_limiti) / total_points * 100) 

        print("\n", sorgente)

        print("\n", total_points,"punti totali")

        print("\n", len(flussi_limiti) , "upper limits")

        print("\n", "percentuale", percentuale, "%")

        return total_points, len(flussi_limiti), percentuale


#-------------------------------------------------------------------------------#
# Funzione che unisce i dati normali e upper limits in array singoli ordinati   #
#-------------------------------------------------------------------------------#


def unisci_array(dati_separati):

    # dati_separati: dizionario con i 4 array restituiti da processa_sorgente
    # tempi_normali, flussi_normali, tempi_limiti, flussi_limiti
        
    # estraggo i 4 array(già mascherati):

    tn = dati_separati['tempi_normali']

    tl = dati_separati['tempi_limiti']

    fn = dati_separati['flussi_normali']

    fl = dati_separati['flussi_limiti']

    # li concateno a due a due e creo un array che mostra l'indice corretto di ordinamento:
    
    tempi_totali = np.concatenate([tn, tl])

    flussi_totali = np.concatenate([fn, fl])

    indice_valori_ordinati = np.argsort(tempi_totali)

    # ottengo infine gli array uniti e ordinati

    tempi_ordinati = tempi_totali[indice_valori_ordinati]

    flussi_ordinati = flussi_totali[indice_valori_ordinati]

    return tempi_ordinati, flussi_ordinati

#----------------------------------------------------------#
# Funzione per il calcolo delle FFT e dei Power Spectrums  #
#----------------------------------------------------------#

def calcola_fft_ps (time, E_flux):


   # definisco l'intervallo minimo dt temporale del mio campione (30 giorni) usando la mediana dell'array differenze

    dt = np.median(np.diff(time)) 

    #calcolo la FFT per fluttuazioni attorno al valor medio

    E_flux = E_flux - np.mean(E_flux)     

    ck = fft.fft(E_flux) #coefficenti ck

    fk = fft.fftfreq(len(E_flux), d=dt) # frequenze fk


    #maschero solo le frequenze positive f>0:

    mask = fk > 0

    fk = fk[mask]

    ck = ck[mask]

    #Power Spectrum

    PS = np.abs(ck)**2
    
    return  fk , PS, dt


#----------------------------------------------------------#
# Funzione per il calcolo della frequenza di Nyquist       #
#----------------------------------------------------------#

def Nyquist(sorgente, dt):

    freq_Ny = 1/(2*dt)

    print("\n", sorgente)

    print("frequenza di Nyquist:" , freq_Ny, "1/g")

    return freq_Ny

#--------------------------------------------------------------------------------------------#
# Funzione che genera Curve di Luce Sintetiche e verifica la significatività del picco       #
#--------------------------------------------------------------------------------------------#

def curve_sintetiche(time, E_flux, Nsim_list, sorgente):

    # chiamo la funzione calcola_fft_ps per ottenere lo  Spettro dei dati osservati

    fk_osservati, PS_osservati, dt = calcola_fft_ps(time, E_flux)

    # picco massimo dello spettro dei dati osservati

    P0 = np.max(PS_osservati)

    print("\n", sorgente)

    print("Picco massimo reale P0 =", P0)

    # creo lista vuota per le percentuali dei massimi randomici

    p_values = []

    # ciclo for per la lista degli N diversi numeri di simulazioni 

    for Nsim in Nsim_list:

        # creo lista vuota per i massimi randomici

        Pmax_rand = []

        # ciclo for per gli N massimi randomici

        for _ in range(Nsim):

            # copia del flusso

            flux_rand = E_flux.copy()

            # mescolamento casuale dell'array E_flux (rompe le  correlazioni temporali)

            np.random.shuffle(flux_rand)

            # calcolo lo spettro della curva randomizzata 

            _, PS_rand, _ = calcola_fft_ps(time, flux_rand)

            # aggiungo il massimo randomico alla lista Pmax_rand

            Pmax_rand.append(np.max(PS_rand))
        
        # converto la lista piena dei max randomici in array 

        Pmax_rand = np.array(Pmax_rand)

        # calcolo la percentuale delle curve randomiche che hanno picco >=P0

        p = (np.sum(Pmax_rand >= P0) / Nsim)*100

        # aggiungo la percentuale trovata alla lista

        p_values.append(p)

        print("\n", "N","=",  Nsim, ",", "percentuale" , "=", p )

        print("Max random medio:", np.mean(Pmax_rand))

        print("Max random massimo:", np.max(Pmax_rand))

    return p_values    


#-----------------------------------------------------------------#
#           Funzione per il fit di riconoscimento del Rumore      #
#-----------------------------------------------------------------#


def fit_power_law(fk, PS, sorgente):
    
    #Fit dello spettro di potenza con legge di potenza:  f^{-beta}#

    logf = np.log10(fk)

    logP = np.log10(PS)
    
    # definisco il modello lineare del fit

    def linear_model(x, a, b):

        return a * x + b

    # array dei parametri del fit
    
    popt, pcov = curve_fit(linear_model, logf, logP)

    a= popt[0]

    b= popt[1]

    a_err = np.sqrt(pcov[0, 0])

    b_err = np.sqrt(pcov[1, 1])  

    beta = -a     

    beta_err = a_err 

    print("\n", sorgente)

    print("Indice di rumore beta" , "=" , beta,  "±",  beta_err)

    # curva di fit

    logP_fit = linear_model(logf, a, b)

    return logP_fit, beta, beta_err
        
    

#####################################################################
#      Funzione principale: main_Blazar_monthly                        #
#####################################################################

def main_Blazar_monthly ():

    args = parse_arguments()

    #---------------------------------------------------------------#
    #                 Dictionary con sorgenti e files               #
    #---------------------------------------------------------------#

    sorgenti_dict = {
        "sorgente_1": {
            "nome_file": "dati_csv/4FGL_J0137.0+4751_monthly_12_27_2024.csv",
        },
        "sorgente_2": { "nome_file": "dati_csv/4FGL_J0442.6-0017_monthly_12_27_2024.csv",
        },
        "sorgente_3": {
            "nome_file": "dati_csv/4FGL_J0449.4-4350_monthly_12_27_2024.csv",
        },
        "sorgente_4": {
            "nome_file": "dati_csv/4FGL_J1256.1-0547_monthly_12_27_2024.csv",
        },
    }

    #----------------------------------------------------------------#
    # Lettura files dei dati e aggiunta del dataframe df a dictionary#
    #----------------------------------------------------------------#

    for sorgente in sorgenti_dict:

        file_blazar = sorgenti_dict[sorgente]["nome_file"]

        df_sorgente = pd.read_csv(file_blazar)

        sorgenti_dict[sorgente].update({'df':df_sorgente})

    #-------------------------------------------------------------#
    #                 Grafici delle Curve di Luce                 #
    #-------------------------------------------------------------#

    if args.gplot  == True:

         fig, axes = plt.subplots(4, 1, figsize=(8, 9), sharex=True)

         colors = ['#FF8C00', '#1E90FF', '#32CD32', '#8A2BE2']

         for indx, sorgente in enumerate(sorgenti_dict):

            ax = axes[indx]
           
            colori = colors[indx]

            #chiamo la funzione processa_sorgente

            mydf = sorgenti_dict[sorgente]["df"]

            dati = processa_sorgente(mydf)

            tempi_normali = dati['tempi_normali']

            flussi_normali = dati['flussi_normali']

            tempi_limiti = dati['tempi_limiti']

            flussi_limiti = dati['flussi_limiti']
        

            #eseguo i plot dei dati "normali" e degli upper limits

            if len(tempi_normali) > 0:         

               ax.plot(tempi_normali, flussi_normali  , linestyle='', marker ='o', markersize=6, color=colori,  label=sorgente)

            if len(tempi_limiti) > 0:

               ax.plot(tempi_limiti, flussi_limiti  , color='red', linestyle='', markersize=5, marker='v', label='Upper limits')

             
             
            ax.legend(loc='upper right')    
               
            ax.set_ylabel("Energy Flux  (log-scale)")

            ax.set_yscale('log')

            #chiamo la funzione calcola_upper

            totali, upper, perc = calcola_upper(flussi_normali, flussi_limiti, sorgente)

         axes[-1].set_xlabel('Julian Date')

         plt.suptitle('Blazar Light Curves - monthly', fontsize=12)

         plt.tight_layout()

         plt.show()


    #-----------------------------------------------------------#
    #                 Calcolo delle FFT e Grafici PS            #
    #-----------------------------------------------------------#

    if args.FFT_PSplot == True or  args.Fit_Blazar == True:

       fig, axes = plt.subplots(4, 1, figsize=(8, 9), sharex=True)

       colors = ['#FF8C00', '#1E90FF', '#32CD32', '#8A2BE2']

       for indx, sorgente in enumerate(sorgenti_dict):

           ax = axes[indx]
           
           colori = colors[indx]

           # chiamo le funzioni processa_sorgente, unisci_array e salvo i data  negli array definitivi

           df_corrente = sorgenti_dict[sorgente]["df"] 
           
           dati_separati = processa_sorgente(df_corrente)

           time, E_flux = unisci_array(dati_separati)

           # chiamo la funzione calcola_fft_ps

           fk,PS,dt = calcola_fft_ps(time, E_flux)

           # chiamo la funzione Nyquist per il calcolo della frequenza di Nyquist  
       
           freq_Ny = Nyquist(sorgente, dt)


           # Grafico Spettrale
        
           ax.loglog(fk , PS, linestyle='-', marker='.',  markersize=2, color=colori,  label=sorgente)


           #-----------------------------------------------------------#
           #                 Calcolo e grafico del fit                 #
           #-----------------------------------------------------------#


           if args.Fit_Blazar == True:

              # Fit relativo all'identificazione del rumore:

              logP_fit, beta, beta_err =  fit_power_law(fk, PS, sorgente)
 
              # Fit Grafico di confronto
           
              ax.loglog(fk, 10**logP_fit, '-', color= colori, label=f'β = {beta:.2f} ± {beta_err:.2f}')

         
           ax.legend(loc='upper right')

           ax.set_ylabel("Power Spectrum (log-scale)")

       axes[-1].set_xlabel('Frequency [1/day] (log scale)')

       if args.Fit_Blazar == True:

        plt.suptitle('Blazar Monthly Spectrum - con Fit Power Law', fontsize=12)

       else:

        plt.suptitle('Blazar Monthly  Spectrum', fontsize=12)
    
       plt.tight_layout()

       plt.show()
                        
    #------------------------------------------------------------------------------#
    #      Generazione di Curve di Luce Sintetiche e calcolo della probabilità       #
    #------------------------------------------------------------------------------#
   
    if args.CLS == True:

       fig, axes = plt.subplots(4, 1, figsize=(8, 9), sharex=True)

       colors = ['#FF8C00', '#1E90FF', '#32CD32', '#8A2BE2']

       for indx, sorgente in enumerate(sorgenti_dict):

           ax = axes[indx]
           
           colori = colors[indx]

           # creo la lista con 7 valori arbitrari scelto del numero N di Curve di Luce Sintetiche 

           Nsim_list = [10000,20000,30000,50000,100000]

           # chiamo le funzioni processa_sorgente, unisci_array e salvo i data  negli array definitivi

           df_corrente = sorgenti_dict[sorgente]["df"] 
           
           dati_separati = processa_sorgente(df_corrente)

           time, E_flux = unisci_array(dati_separati)

           #chiamo la funzione curve_sintetiche per l'analisi della significatività del picco di potenza

           p_values = curve_sintetiche(time, E_flux, Nsim_list, sorgente)

          

           
if __name__ == "__main__":
    main_Blazar_monthly()
