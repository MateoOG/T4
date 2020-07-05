
# Se importan las libreiras necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from scipy import signal


listaBits= []

# Se leen los datos del archivo que contiene los bits

Leerdatos = pd.read_csv('bits10k.csv') # se leen los datos del archivo que contiene los bits
  
DF = pd.DataFrame(Leerdatos) # se convierten los datos en un DataFrame

CC = DF.values.tolist()# se pasa del DataFrame a lista


# se almacenan los valores de los bits en una lista
for i in range(0,len(CC)):
    listaBits.append((sum(CC[i])))




N = len(listaBits)    # número de bits en la lista
    

pb = 5 # número de bits a visualizar
    
# Se genera la señal modulada BPSK

f = 5000 # Hz  # Frecuencia de operación

# Duración del período de cada símbolo (onda)
T = 1/f # 1 ms

# Número de puntos de muestreo por período
p = 50

# Puntos de muestreo para cada período
tp = np.linspace(0, T, p)

# Creación de la forma de onda de la portadora
sinus = np.sin(2*np.pi * f * tp)

# Visualización de la forma de onda de la portadora
plt.plot(tp, sinus)
plt.title('Onda Portadora')
plt.xlabel('Tiempo / s')
plt.savefig('Onda Portadora.png')
plt.show()

# Frecuencia de muestreo
fs = p/T # 50 kHz

# Creación de la línea temporal para toda la señal enviada:  Tx
t = np.linspace(0, N*T, N*p)

# Inicializar el vector de la señal modulada Tx
senal = np.zeros(t.shape)

# Creación de la señal modulada BPSK
for k, b in enumerate(listaBits):
    if b == 1:
        senal[k*p:(k+1)*p] = b * sinus
    else:
        senal[k*p:(k+1)*p] = -sinus
        

# Visualización de los primeros bits modulados
plt.figure()
plt.plot(senal[0:pb*p])
plt.title('Primeros 5 bits de la lista mudulados')
plt.savefig('Primeros 5 bits de la lista mudulados.png')
plt.show()



# Potencia instantánea
Pinst = senal**2

# Potencia promedio a partir de la potencia instantánea (W)
Ps = integrate.trapz(Pinst, t) / (N * T)



# acá se hace la decodificación para cada uno de los SNR solicitados
ListaSNR = []
ListaBER = []
 
A = True
while A == True:
    
    
# Relación señal-a-ruido deseada
    SNR = int(input('ingrese relación señal a ruido - SNR deseada:  desde -2 hasta 3 dB:'))
    ListaSNR.append(SNR)
# Potencia del ruido para SNR y potencia de la señal dadas
    Pn = Ps / (10**(SNR / 10))

# Desviación estándar del ruido
    sigma = np.sqrt(Pn)

# Crear ruido (Pn = sigma^2)
    ruido = np.random.normal(0, sigma, senal.shape)

# Simular "el canal": señal recibida
    Rx = senal + ruido

# Visualización de los primeros bits recibidos
#pb = 5
    plt.figure()
    plt.title('Primeros 5 btis recibidos')
    plt.plot(Rx[0:pb*p])
    plt.savefig('Primeros 5 btis recibidos.png')
    plt.show()





# Antes del canal ruidoso
    fw, PSD = signal.welch(senal, fs, nperseg=1024)
    plt.figure()
    plt.semilogy(fw, PSD)
    plt.title('Desidad espectral de potencia antes del canal')
    plt.xlabel('Frecuencia / Hz')
    plt.ylabel('Densidad espectral de potencia / V**2/Hz')
    plt.savefig('Desidad espectral de potencia antes del canal.png')
    plt.show()

# Después del canal ruidoso
    fw, PSD = signal.welch(Rx, fs, nperseg=1024)
    plt.figure()
    plt.semilogy(fw, PSD)
    plt.title('Desidad espectral de potencia después del canal')
    plt.xlabel('Frecuencia / Hz')
    plt.ylabel('Densidad espectral de potencia / V**2/Hz')
    plt.savefig('Desidad espectral de potencia después del canal.png')
    plt.show()








    
    
    bits = np.asarray(listaBits) # se convierte la lista de bits en un vector

# Pseudo-energía de la onda original (esta es suma, no integral)
    Es = np.sum(sinus**2)

# Inicialización del vector de bits recibidos
    bitsRx = np.zeros(bits.shape)

# Decodificación de la señal por detección de energía
    for k, b in enumerate(bits):
        Ep = np.sum(Rx[k*p:(k+1)*p] * sinus)
        if Ep > Es/2:
            bitsRx[k] = 1
        else:
            bitsRx[k] = 0

    err = np.sum(np.abs(bits - bitsRx))
    BER = err/N
    ListaBER.append( BER)

    print('Hay un total de {} errores en {} bits para una tasa de error de {}.'.format(err, N, BER))

    
    
    if SNR == 3:
        A = False
    
    
# acá se sale del While
print('Para cada uno de los los SNR seleccionados:' , ListaSNR, 'dB')  
print('Hay una BER de:' ,ListaBER, 'En su respectivo orden para cada SNR seleccionado')  
print('La pontencia promedio calculada es:' ,Ps)



plt.plot(ListaSNR,ListaBER)
plt.title('SNR vs BER')
plt.ylabel('BER')
plt.xlabel('SNR')
plt.savefig('SNR vs BER.png')
plt.show()


