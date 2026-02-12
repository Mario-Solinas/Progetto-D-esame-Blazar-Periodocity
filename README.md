# Progetto-D-esame-Blazar-Periodocity

Il seguente progetto è suddiviso rispettivamente in 4 file e cartelle: 

-file README.md (il suddetto)

-cartella dati_csv: contiene tutti i file weekly e monthly per sorgente (2 per sorgente)

-Blazar-Periodocity_weekly.py: contiene lo script python  con la realizzazione delle richieste previste per i datasheet settimanali di ciascuna sorgente.

-Blazar-Periodocity_monthly.py: contiene lo script python  con con la realizzazione delle richieste previste  per i datasheet mensili di ciascuna sorgente.

La struttura dei file Blazar-Periodocity_weekly.py e Blazar-Periodocity_monthly.py è del tutto simmetrica: le funzioni e le funzionalità implementate sono le medesime. Anzitutto è riportato l'importo dei moduli python necessari, alla quale si aggiungono brevi didascalie introduttive per le funzioni utilizzate. La funzione speciale "arse_arguments" permette all'utente di selezionare le opzionalità contenenti quattro diverse analisi dati:

1)'--gplot' : per l'analisi grafica delle Curve di Luce

2)'--FFT_PSplot': per l'analisi di Fourier e dello spettro di Potenza.

3)'--CLS': per genearare  Curve di Luce Sintetiche e calcolare  la probabilità, a partire da punti di massimo di potenza spettrale  casuali (randomici) , di ottenere un picco >= del picco di potenza ricavato dai dati effettivi osservabili per ciascuna sorgente. Nel main sarà riportato anche un grafico esplicativo di confronto, per evidenziare la dipendenza delle percentuali ottenute dal numero N di simulazioni effettuate.

4) '--Fit_Blazar': Sebbene non esplicitamente richiesta nel progetto, tenendo in considerazione  le percentuali ottenute per la significatività dei picchi di potenza osservabili, tale funzionalità permette di indagare sulla tipologia di rumore presente nelle sorgenti osservabili e concludere quindi l'analisi spettrale. 


Le 4 optzionalità vengono definite successivamente nel main, a partire da una serie di blocchi if, che permettono quindi la possibilità di selezione.

In principio, accompagnate da commenti espliciti che facilitano la lettura e la comprensione della logica dei blocchi di istruzioni utilizzate, sono state definite, fuori dal main, ben 7 funzioni di supporto:

1) processa_sorgente: utilizzata per separare i dati "normali" di flusso, dagli upper limits, contrassegnati dal simbolo  "<"nei datasheet. Lo scopo è infatti selezionare 4 array di dati flusso-tempo dal datasheet della sorgente:
            
            normal_flux 

            normal_time 

            upper_flux 
         
            upper_time 

di modo da poter , successivamente nel main, plottare separatamente i grafici con i dati normali e contrassegnare in rosso i valori limiti superiori. I 4 array andranno mascherati,  per eliminare i possibili "Not a number=Nan" e valori contrassegnati dal simbolo "-". Verrà restituito infine, dalla funzione, un dizionario contenente i 4 array desiderati. 


2) calcola_upper: calcola semplicemente il numero totale di punti, di upper limits presenti in ciascuna sorgente e la loro relativa percentuale nel campione.


3) unisci_array: necessaria per unire gli array normal_flux- upper_flux e normal_time-upper_time e avere quindi due array di float data "puliti", ossia privi di ireggolarità (Nan, "-") da poter poi usare nei plot dei grafici relativi allo spettro di potenza.

4) calcola_fft_ps: dopo aver definito l'intervallo temporale e si noti l'utilizzo del valore mediano per ottenere quasi certamente un intervallo unico equispaziato, calcola i coefficienti di Fourier, le rispettive frequenze(mascherate positive) e la funzione Potenza Spettrale, PS, necessarie per l'analisi spettrale. Si noti, la sottrazione del valor medio nel calcolo della funzione stocastica da trasformare: tale scelta ricade nella volontà di analizzare la variabilità attorno al valor medio, dovuta al contributo stocastico della funzione di partenza (sarà motivata nella futura presentazione).


5) Nyquist: calcola, per ogni sorgente, la frequenza limite di Nyquist, che può essere infine controllata a partire dai grafici spettrali ottenuti nel main. 


6) curve_sintetiche: funzione necessaria al calcolo della probabilità di ottenere un picco >= del picco di potenza ricavato dai dati effettivi osservabili per ciascuna sorgente , a partire da max di potenza generati casualmente tramite la funzionalità np.random.shuffle di numpy, la quale permette di ordinare casualmente gli elementi di un array (flux_rand). Con 2 cicli for, si ottiene quindi per ogni valore N di simulazioni scelto, un array di picchi random, della quale viene calcolata la probabilità richiesta. 


7)fit_power_law: funzione utilizzata per il fit di potenza relativo alla correlazione con la funzione di fit f^{-beta}. Si cerca una linearizzazione logaritmica dei dati, la quale offrirà l'opportunità, mediante i valori di beta trovati, di stabilire per ciascuna sorgente, la presenza o meno di rumore. Ciò permette di verificare la natura stocastica dei dati di flusso osservati.


Nella funzione main infine, dopo aver salvato i datasheet in un opportuno dizionario, vengono eseguite le funzionalità previste nel parser, ottenendo i grafici corrispettivi richiesti. 


