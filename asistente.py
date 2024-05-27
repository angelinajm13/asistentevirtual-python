import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia
import pyaudio
import subprocess


# opciones de voz
id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'
id2 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'


# escuchar el microfono y devolver el audio como texto
def transformar_audio_en_texto():
    # almacenar recognizer en variable
    r = sr.Recognizer()

    # configurar el microfono
    with sr.Microphone() as origen:
        # tiempo de espera
        r.pause_threshold = 0.8

        # informar que comenzó la grabación
        print("ya puedes hablar")

        # guardar lo que escuche como audio
        audio = r.listen(origen)

        try:
            # buscar en google
            pedido = r.recognize_google(audio, language="es-mx")

            # prueba de que pudo ingresar
            print("Dijiste: "+pedido)

            # devolver a pedido
            return pedido
        # en caso de que no comprenda el audio
        except sr.UnknownValueError:

            # prueba de que no comprendio el audio
            print("ups, no entendi")

            # devolver error
            return  "sigo esperando"

        # en caso de no resolver el pedido
        except sr.RequestError:
            # prueba de que no comprendio el audio
            print("ups, no hay servicio")

            # devolver error
            return "sigo esperando"

        # error inesperado
        except:
            # prueba de que no comprendio el audio
            print("ups, algo ha salido mañ")

            # devolver error
            return "sigo esperando"


# funcion para que el asistente pueda ser escuchado
def hablar(mensaje):

    # encender el motor pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id1)

    # pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# informar día de la semana
def pedir_día():
    # crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    # crear variable para el dia de la semana
    dia_semana = dia.weekday()
    print(dia_semana)


    # diccionario con nombre de dias
    calendario = {0: 'Lunes',
                  1: 'Martes',
                  2: 'Miércoles',
                  3: 'Jueves',
                  4: 'Viernes',
                  5: 'Sábado',
                  6: 'Domingo'}

    # decir el dia de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')


# informar hora
def pedir_hora():
    # crear variable con datos de la hora
    hora = datetime.datetime.now()
    hora = (f'En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos.')
    print(hora)

    # decir la hora
    hablar(hora)


# funcion saludo inicial
def saludo_inicial():
    #crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buen día'
    else:
        momento = 'Buenas tardes'
    # decir el saludo
    hablar(f'{momento} Angy, soy Helena, tu asistente ´personal. ¿En qué puedo ayudarte?')


# funcion central del asistente
def pedir_cosas():
    # activar saludo inicial
    saludo_inicial()

    # variable de corte
    comenzar = True

    #loop central
    while comenzar:
        # activamos el microfono y guardamos el pedido en un string
        pedido = transformar_audio_en_texto().lower()

        if 'abrir youtube' in pedido:
            hablar('Con gusto, estoy abriendo YouTube')
            webbrowser.open('https://www.youtube.com')
        elif 'abrir navegador' in pedido:
            hablar('Claro, abriendo navegador')
            webbrowser.open('https:www.google.com')
        elif 'qué día es hoy' in pedido:
            pedir_día()
        elif 'qué hora es' in pedido:
            pedir_hora()
        elif 'me puedes saludar' in pedido:
            hablar(saludo_inicial())
        elif 'dime' in pedido:
            pedido = pedido.replace('dime', '')
            hablar(pedido)
        elif 'busca en wikipedia' in pedido:
            try:
                hablar('Buscando en wikipedia')
                pedido = pedido.replace('busca en wikipedia', '')
                wikipedia.set_lang('es')
                resultado = wikipedia.summary(pedido, sentences=1)
                hablar('Encontré esto en Wikipedia: ')
                hablar(resultado)
            except:
                hablar('Lo siento, no encontré algo acerca de eso. ¿Me puedes repetir?')
        elif 'busca horóscopo' in pedido:
            hablar('Ya mismo estoy en eso')
            pedido = pedido.replace('busca', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
        elif 'busca en internet' in pedido:
            hablar('Ya mismo estoy en eso')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
        elif 'abre bloc de notas' in pedido:
            hablar('Abriendo bloc de notas')
            subprocess.Popen(['C:\Windows\System32\\notepad.exe'])
        elif 'reproducir' in pedido:
            try:
                hablar('Excelente, en un momento')
                pywhatkit.playonyt(pedido)
            except:
                hablar('Lo siento, no pude reproducirlo.')
        elif 'broma' in pedido:
            hablar(pyjokes.get_joke('es'))
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = { 'apple':'APPL',
                        'amazon':'AMZN',
                        'google':'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPreviousClose']
                hablar(f'La encontré, el precio de {accion} es {precio_actual}')
            except:
                hablar('Perdón pero no la he encontrado.')
        elif 'adiós' in pedido:
            hablar('Me voy a descansar, cualquier cosa me avisas')
            break


pedir_cosas()

