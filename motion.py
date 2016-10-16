# source ~/.virtualenvs/cv/bin/activate python3 ~/Desktop/TesteCamera.py

import os
import telepot as tp
import time
import numpy as np
import cv2
from datetime import datetime
from gpiozero import Button
from gpiozero import MotionSensor
from signal import pause
import socket
s = socket.socket()
port = 12345
#hostname = socket.gethostname()
#print(hostname)
#s.bind("", port)
#s.bind((hostname, port))
s.bind(("192.168.4.100", port))
s.listen(5)
mensagem = "teste"
msg = bytes(mensagem, 'UTF-8')
print('pronto')

i = 1
x = []
y = []
z = []

alerta_on = False

def alerta():
	global alerta_on
	global mensagem_original

	if(alerta_on):
		alerta_on = False
		print("ALERTA")
		tmp = mensagem_original
		tmp['text'] = "Alerta - Sensor de Movimento"
		tmp['from']['username'] = '!!Alerta!!'
		tmp['from']['first_name'] = ''
		tmp['from']['last_name'] = ''
		bot.sendMessage(tmp['chat']['id'], 'Alerta! Alguém entrou/saiu da casa!!')
		log(str(datetime.now()) + " | " + str(tmp['from']['username']) + " | " + str(tmp['from']['id']) + " | " + str(tmp['text']))
		alerta_on = True
	else:
		pass

check = True
while check:
	print('1')
	c,addr=s.accept()
	print("got connection from " + str(addr))
	print('2')
	check = False
print('3')
'''
while True:
	a = c.recv(4)
	lerMensagem(a)
	time.sleep(0.1)
'''
mensagem_original = {}

# Token do bot (e objeto bot em si)
bot = tp.Bot('226097875:AAEQQGekoq8bmCy6KzvZTxrNEkZRi1OfPj8')
#bot = tp.Bot('265998436:AAG4zP0QXlRs9ZsiT1Q5Z1-symE9vGpdm2g')

# O botão está sendo pressionado?
button_on = False

# O programa está tirando fotos?
tirando_fotos = False

# O botão esta ligado na porta 2 (opcional)
button = Button(2)

pir = MotionSensor(4)

# Valores Hardcoded
esperaMaxima = 5
esperaMinima = 1
quantidadeMaximaFotos = 5
quantidadeMinimaFotos = 1

padraoFotos = 3
padraoEspera = 1

# Valores passíveis de edição
segundos_esperados = 2
frames_esperados = 7*segundos_esperados
nfotos = 3

start = False

def processar(msg):
	global button_on
	global frames_esperados
	global nfotos
	global tirando_fotos
	global start
	global alerta_on

	global esperaMaxima
	global esperaMinima
	global quantidadeMaximaFotos
	global quantidadeMinimaFotos

	global padraoFotos
	global padraoEspera
	# Mostrar cada mensagem do usuário
	#print(msg)
	#print('Try log')
	try:
		log(str(datetime.now()) + " | " + str(msg['from']['username']) + " | " + str(msg['from']['id']) + " | " + str(msg['text']))
		#log("Isso é um teste")
		#print("Log Tipo 1")
	except KeyError:
		#print('Key Error 1')
		try:
			#print("teste2")
			log(str(datetime.now()) + " | " + str(msg['from']['first_name']) + " " + str(msg['from']['last_name']) + " | " + str(msg['from']['id']) + " | " + str(msg['text']))
			print("Log Tipo 2")
		except KeyError:
			#print('Key Error 2')
			try:
				#print("teste3")
				log(str(datetime.now()) + " | " + str(msg['from']['first_name']) + " | " + str(msg['from']['id']) + " | " + str(msg['text']))
				print("Log Tipo 3")
			except KeyError:
				#print("teste4")
				#print('Key error 3')
				log('Outro')
				print("Log Tipo 4")

	########################################### Interpretar opção ########################################
	mensagem = msg['text'].lower()
	
	if(mensagem == 'tirar fotos'):
		#print('1')
		while(tirando_fotos):
			#print('esperando - mensagem')
			time.sleep(1)
		tirarFotos(msg)

	elif(mensagem.find('espera') >= 0):
		try:
			valor = int(mensagem.split(" ", 1)[1])
			if valor > esperaMaxima:
				bot.sendMessage(msg['chat']['id'], 'O valor excede o limite máximo (' + str(esperaMaxima) + ' segundos)')
				valor = esperaMaxima
			if valor < esperaMinima:
				bot.sendMessage(msg['chat']['id'], 'O valor excede o limite mínimo (' + str(esperaMinima) + ' segundos)')
				valor = esperaMinima
			segundos_esperados = valor
			frames_esperados = 7*segundos_esperados
			bot.sendMessage(msg['chat']['id'], 'Espera configurada para ' + str(valor) + ' segundos')
		except Exception:
			#print(traceback.print_exc())
			bot.sendMessage(msg['chat']['id'], 'Valor não reconhecido' + '\n' + 'O comando deve ser executado da seguinte forma:' + '\n' + 'Ex: \"espera ' + str(esperaMaxima) + '\"')
	
	elif(mensagem.find('quantidade') >= 0):
                try:
                        valor = int(mensagem.split(" ", 1)[1])
                        if valor > quantidadeMaximaFotos:
                                bot.sendMessage(msg['chat']['id'], 'O valor excede o limite máximo (' + str(quantidadeMaximaFotos) + ' fotos)')
                                valor = quantidadeMaximaFotos
                        if valor < quantidadeMinimaFotos:
                                bot.sendMessage(msg['chat']['id'], 'O valor excede o limite mínimo (' + str(quantidadeMinimaFotos) + ' fotos)')
                                valor = quantidadeMinimoFotos
                        nfotos = valor
                        bot.sendMessage(msg['chat']['id'], 'Quantidade de fotos configurada para ' + str(valor) + ' fotos')
                except Exception:
                        #print(traceback.print_exc())
                        bot.sendMessage(msg['chat']['id'], 'Valor não reconhecido' + '\n' + 'O comando deve ser executado da seguinte forma:' + '\n' + 'Ex: \"quantidade ' + str(quantidadeMinimaFotos) + '\"')

		#receberEspera(msg)
	#elif(mensagem.find('quantidade')):
		#print('3')
		#receberQuantidade(msg)
	
	#elif(mensagem == '622345'):
		#print('4')
		#kill()
	elif(mensagem == '/start'):
		global mensagem_original
		mensagem_original = msg
		bot.sendMessage(msg['chat']['id'], 'Sistema inicializado' + '\n' + 'Digite "help" para mostrar a lista de comandos')
		button_on = True
		alerta_on = True
		start = True
		#bot.sendMessage(msg['chat']['id'], 'Ola ' + str(msg['from']['first_name']) + '! Bem vindo ao Security Bot')
	elif(mensagem == 'help'):
		bot.sendMessage(msg['chat']['id'], 'Comandos:'
+ '\n\n' + '1) "tirar fotos":'
+ '\n' + 'Tirar fotos e enviar'
+ '\n\n' + '2) "quantidade N":'
+ '\n' + 'Configurar a quantidade de fotos para N fotos (' + str(quantidadeMinimaFotos) + ' foto ~ ' + str(quantidadeMaximaFotos) + ' fotos)' + '\n' + 'Padrão: ' + str(padraoFotos)
+ '\n\n' + '3) "espera N":'
+ '\n' + 'Configurar a quantidade de segundos esperados entre fotos (' + str(esperaMinima) + 's~' + str(esperaMaxima) + 's)' + '\n' + 'Padrão: ' + str(padraoEspera)
)
	else:
		print(mensagem)

		#bot.sendMessage(msg['chat']['id'], 'Comando não identificado' + '\n\n' + 'Digite "help" para mostrar a lista de comandos')
		
	#####################################################################################################
	

################### Opção 1 - Tirar fotos #############################
def tirarFotos(msg):
	global frames_esperados
	global nfotos
	global tirando_fotos
	tirando_fotos = True
	
	bot.sendMessage(msg['chat']['id'], 'Comando interpretado: tirar fotos')

	cap = cv2.VideoCapture(0)
	#bot.sendMessage(msg['chat']['id'], 'Tirando fotos...')
	
	Fotos_tiradas = 0
	a = 1
	
	dirname = 'Fotos'
	if(not(os.path.exists(dirname))):
		os.mkdir(dirname)

	frames_pulados = 30
	for i in range(frames_pulados):
		cap.read()

	bot.sendMessage(msg['chat']['id'], 'Tirando fotos')
	while(Fotos_tiradas < nfotos):

		# Tirar uma foto	   
		ret, frame = cap.read()
		
		# Gravar a foto em disco --> "Foto N.jpg"
		filename = 'Foto ' + str(a) + '.jpg'
		#print(os.path.join(dirname, filename))
		cv2.imwrite(os.path.join(dirname, filename), frame)
		
		# Mandar mensagem "Foto N tirada"
		bot.sendMessage(msg['chat']['id'], 'Foto ' + str(int(a)) + '/' + str(nfotos) + ' tirada')

		# Aumentar o número de fotos tiradas
		Fotos_tiradas = Fotos_tiradas + 1
	 
		a = a + 1
		   
		# Pular N frames
		for i in range(frames_esperados):
			cap.read()

	# Nesse ponto, todas as fotos foram tiradas
	
	# Mandar mensagem "Fotos tiradas!"
	bot.sendMessage(msg['chat']['id'], 'Fotos tiradas!')
	
	# Mandar mensagem "Enviando..."
	bot.sendMessage(msg['chat']['id'], 'Enviando...')

	# Enviar cada foto
	os.chdir('Fotos')
	for i in range(nfotos):
		foto = open('Foto ' + str(i+1) + '.jpg', 'rb')
		bot.sendPhoto(msg['chat']['id'], ('Foto ' + str(nfotos+1) + '.jpg', foto))
	
	os.chdir('/home/pi/CamSegBot/CamSegBot')
	# Mandar mensagem "Enviado!"
	bot.sendMessage(msg['chat']['id'], 'Enviado!')
	
	# Desligar a câmera
	cap.release()

	tirando_fotos = False

################### Opção 2 - Receber espera #############################
def log(message):
	#print(message)
	try:
		log = open('log.txt', 'a')
		log.write(message + '\n')

	except Exception:
		pass
		#print(traceback.print_exc())

################################# Esperar as mensagens  ###########################################
def mandarSinal():
	global button_on
	global mensagem_original
	global tirando_fotos
	print("entrou no log")
	tmp = mensagem_original
	tmp['text'] = "tirar fotos"
	tmp['from']['username'] = '!!PanicButton!!'
	tmp['from']['first_name'] = ''
	tmp['from']['last_name'] = ''
	bot.sendMessage(tmp['chat']['id'], 'Botão Pressionado!!')
	while(tirando_fotos):
		time.sleep(1)
		#print('esperando - botão')
	processar(tmp)
	for i in range(10):
		#print('Cooldown: ' + str(i))
		time.sleep(1)
	button_on = True

def handle(msg):
	processar(msg)
   
bot.message_loop(handle)
os.system("clear")
print('Listening...')

umafoto = True
while(True):
	
	if(pir.motion_detected):
		if(umafoto):
			print("Foto")
			alerta()
			umafoto = False
	
	else:
		if(not umafoto):
			print('Ready')
			umafoto = True
	time.sleep(0.1)
