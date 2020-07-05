# Tarea-No.-4-MPSS



# 1.
Crear un esquema de modulación BPSK para los bits presentados. Esto implica asignar una forma de onda sinusoidal normalizada (amplitud unitaria) para cada bit y luego una concatenación de todas estas formas de onda:

La forma de la onda portadora es la siguiente:


![Portadora](https://github.com/MateoOG/Tarea-No.-4-MPSS/blob/master/Onda%20Portadora.png)


Para crear esta onda se usó el siguiente código:
```
sinus = np.sin(2*np.pi * f * tp)
```
Donde: f es la frecuencia de operación y tp es la cantidad de puntos de muesteo para cada periodo


Los primeros 5 bits de la lista modulados se muestran en la siguiente figura:
![Primeros 5 bits modulados](https://github.com/MateoOG/Tarea-No.-4-MPSS/blob/master/Primeros%205%20bits%20de%20la%20lista%20modulados.png)

Para lograr la modulación se usó el siguiente fragmento de código:

```
for k, b in enumerate(listaBits):
    if b == 1:
        senal[k*p:(k+1)*p] = b * sinus
    else:
        senal[k*p:(k+1)*p] = -sinus
        
```    


# 2.
Calcular la potencia promedio de la señal modulada generada:


La potencia promedio de la señal modulada es: 0.49

Para hallarla se usó el siguinete fragmento de código:
```
# Potencia instantánea
Pinst = senal**2

# Potencia promedio a partir de la potencia instantánea (W)
Ps = integrate.trapz(Pinst, t) / (N * T)
```

Donde t es la línea temporal de la señal enviada, N es el número de bits que se están transmitiendo, y T es el periodo de cada onda




# 3.
Simular un canal ruidoso del tipo AWGN (ruido aditivo blanco gaussiano) con una relación señal a ruido (SNR) desde -2 hasta 3 dB

Para crear esta señal que incluye ruido y la onda portadora se usó el siguiente código:
```  
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

# Simular "el canal": señal recibida = señal modulada + ruido
    Rx = senal + ruido
    
    if SNR == 3:
        A = False

```  

De esta forma se puede modificar el valor de SNR entre -2 y 3.


El resultado gráfico de esta simulación para cado uno de los valores de SNR (-2,-1,0,1,2,3) usados es respectivamente:

![5 Bits recibidos para SNR = -2](https://github.com/MateoOG/Tarea-No.-4-MPSS/blob/master/Primeros%205%20btis%20recibidos%20(SNR%20%3D-2).png)

![5 Bits recibidos para SNR = -1](https://github.com/MateoOG/Tarea-No.-4-MPSS/blob/master/Primeros%205%20btis%20recibidos(SNR%20%3D-1).png)

![5 Bits recibidos para SNR = 0](https://github.com/MateoOG/Tarea-No.-4-MPSS/blob/master/Primeros%205%20btis%20recibidos(SNR%20%3D0).png)

![5 Bits recibidos para SNR = 1](https://github.com/MateoOG/Tarea-No.-4-MPSS/blob/master/Primeros%205%20btis%20recibidos(SNR%20%3D1).png)

![5 Bits recibidos para SNR = 2](https://github.com/MateoOG/Tarea-No.-4-MPSS/blob/master/Primeros%205%20btis%20recibidos(SNR%20%3D2).png)

![5 Bits recibidos para SNR = 3](https://github.com/MateoOG/Tarea-No.-4-MPSS/blob/master/Primeros%205%20btis%20recibidos(SNR%20%3D3).png)




# 4.
Graficar la densidad espectral de potencia de la señal con el método de Welch (SciPy), antes y después del canal ruidoso:



La densidad espectral de potencia antes del canal es:

![Función Ajustada de Densidad Marginal de X ](https://github.com/MateoOG/Tarea-No.-4-MPSS/blob/master/Desidad%20espectral%20de%20potencia%20antes%20del%20canal.png)


La densidad espectral de potencia después del canal es:

![Función Ajustada de Densidad Marginal de Y](https://github.com/MateoOG/Tarea-No.-4-MPSS/blob/master/Desidad%20espectral%20de%20potencia%20despu%C3%A9s%20del%20canal.png)



Estas dos gráficas muestran que el ruido que introduce el canal ruidoso afecta directamente el comportamiento de la potencia de la señal y se relación con la frecuencia.





# 5.
Demodular y decodificar la señal y hacer un conteo de la tasa de error de bits (BER, bit error rate) para cada nivel SNR:


Para realizar este punto se ejecutó el siguiente fragmento de código:


```  
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
```  


La parte del código ```np.sum(Rx[k*p:(k+1)*p]``` es negativo cuando se modula un cero, por eso funciona de maera óptima el for del código anterior.

Para cada uno de los los SNR seleccionados: [-2, -1, 0, 1, 2, 3] dB:

Hay una BER de: [0.0012, 0.0001, 0.0001, 0.0, 0.0, 0.0], en su respectivo orden para cada SNR seleccionado



# 6.
Graficar BER versus SNR:

El resultado gráfico de esta relación es:


![SNR vs BER](https://github.com/MateoOG/Tarea-No.-4-MPSS/blob/master/SNR%20vs%20BER.png)


Esta gráfica lo que nos dice es que entre más grande sea el SNR menor error (BER: bit error rate) de transferencia  de bits habrá.




