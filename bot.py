from re import A
from select import select
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
from sqlite3 import Error
import datetime
from datetime import datetime


TELEGRAM_TOKEN = "Insira seu token aqui"
sim = 0
bot = telebot.TeleBot(TELEGRAM_TOKEN)
a = 0

dic = dict(
AC = "Acre",		
AL = "Alagoas",	  	
AP = "Amapá",		
AM = "Amazonas",		
BA = "Bahia",		
CE = "Ceará",	
DF = "Distrito Federal",
ES = "Espírito Santo",		
GO = "Goiás",		
MA = "Maranhão",		
MT = "Mato Grosso",		
MS = "Mato Grosso do Sul",
MG = "Minas Gerais",		
PA = "Pará",		
PB = "Paraíba",	
PR = "Paraná",		
PE = "Pernambuco",		
PI = "Piauí",		
RJ = "Rio de Janeiro",	
RN = "Rio Grande do Norte",	
RS = "Rio Grande do Sul",		
RO = "Rondônia",		
RR = "Roraima",		
SC = "Santa Catarina",		
SP = "São Paulo",		
SE = "Sergipe",		
TO = "Tocantins"
)


def ConexaoBanco():
    caminho = "/app/Telegram_bot.db"
    con = None
    try:
        con = sqlite3.connect(caminho, check_same_thread=False)
    except Error as ex:
        print(ex)
    return con
 
vcon = ConexaoBanco()



def inserir(conexao, sql):
    try:
        c = conexao.cursor()
        c.execute(sql)
        conexao.commit()
    except Error as ex:
        print(ex)


#avaliações do usuario

@bot.callback_query_handler(lambda query: query.data == "aval5" or query.data == "aval4" or query.data == "aval3" or query.data == "aval2" or query.data == "aval1")
def aval5(query):
    global a
    if(query.data == "aval5"):
        vsql =f"""update tab_main set avaliacao = 5 where ID = {a}"""     
    elif(query.data == "aval4"):
        vsql =f"""update tab_main set avaliacao = 4 where ID = {a}"""
    elif(query.data == "aval3"):
        vsql =f"""update tab_main set avaliacao = 3 where ID = {a}"""
    elif(query.data == "aval2"):
        vsql =f"""update tab_main set avaliacao = 2 where ID = {a}"""
    else:
        vsql =f"""update tab_main set avaliacao = 1 where ID = {a}"""
        
    inserir(vcon, vsql) 

    bot.send_message(query.message.chat.id, "Agradecemos sua Avaliação!.\nCaso conheça alguém na mesma situação, mande o link do Bot cripto: https://t.me/Criptoati_bot\n\n\nCaso queira refazer o teste, basta enviar a palavra (Menu)")





def aval():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton(1, callback_data="aval1"),
                               InlineKeyboardButton(2, callback_data="aval2"),
                                                InlineKeyboardButton(3, callback_data="aval3"),
                                                                InlineKeyboardButton(4, callback_data="aval4"),
                                                                                InlineKeyboardButton(5, callback_data="aval5"))
    return markup



#total de sim = 16
#Calculando as probabilidades
@bot.callback_query_handler(lambda query: query.data == "NAO11" or query.data =="SIM11")
def Pergun7(query):
    global a
    global sim

    if(query.data == "SIM11"):
        sim += 1
        sql =f"""update tab_main set Pergunta11 = 'Sim' where ID = {a}"""
    else:
        sql =f"""update tab_main set Pergunta11 = 'Não' where ID = {a}"""
        
    inserir(vcon, sql)

    data_atual = datetime.now()
    data = data_atual.strftime('%d/%m/%Y %H:%M')

    datasql =f"""update tab_main set DataFIm = '{data}' where ID = {a}"""
    inserir(vcon,datasql)


    bot.send_message(query.message.chat.id, "Verificando sua situação")
    if sim <= 4:
        bot.send_message(query.message.chat.id, "Seu investimento tem baixa chance de ser fraudulento...")
        bot.send_message(query.message.chat.id, "De 0 a 5, qual a sua avaliação do bot cripto?", reply_markup=aval())
    elif sim >= 5 and sim <= 8:
        bot.send_message(query.message.chat.id, "Seu investimento é duvidoso, pesquise mais sobre a empresa e o investimento...")
        bot.send_message(query.message.chat.id, "De 0 a 5, qual a sua avaliação do bot cripto?", reply_markup=aval())
    else:
        bot.send_message(query.message.chat.id, "Seu investimneto tem grandes chances de ser fraudulento...")
        bot.send_message(query.message.chat.id, "De 0 a 5, qual a sua avaliação do bot cripto?", reply_markup=aval())


#Pergunta 11
def pergunta11():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("SIM", callback_data="SIM11"),
                               InlineKeyboardButton("NÃO", callback_data="NAO11"))
    return markup

@bot.callback_query_handler(lambda query: query.data == "NAO10" or query.data =="SIM10")
def Pergun11(query):
    global a
    global sim

    if(query.data == "SIM10"):
        sim += 2
        sql =f"""update tab_main set Pergunta10 = 'Sim' where ID = {a}"""
    else:
        sql =f"""update tab_main set Pergunta10 = 'Não' where ID = {a}"""
        
    inserir(vcon, sql)

    bot.send_message(query.message.chat.id, "Pergunta 11\n\n\nFoi mostrado a você a situação de outros investidores que enriqueceram com o investimento?", reply_markup=pergunta11())



#Pergunta 10
def pergunta10():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("SIM", callback_data="SIM10"),
                               InlineKeyboardButton("NÃO", callback_data="NAO10"))
    return markup

@bot.callback_query_handler(lambda query: query.data == "NAO9" or query.data =="SIM9")
def Pergun10(query):
    global a
    global sim

    if(query.data == "SIM9"):
        sim += 2
        sql =f"""update tab_main set Pergunta9 = 'Sim' where ID = {a}"""
    else:
        sql =f"""update tab_main set Pergunta9 = 'Não' where ID = {a}"""
        
    inserir(vcon, sql)

    bot.send_message(query.message.chat.id, "Pergunta 10\n\n\nFoi te oferecido uma informação exclusiva/secreta?", reply_markup=pergunta10())



#Pergunta 9
def pergunta9():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("SIM", callback_data="SIM9"),
                               InlineKeyboardButton("NÃO", callback_data="NAO9"))
    return markup

@bot.callback_query_handler(lambda query: query.data == "NAO8" or query.data =="SIM8")
def Pergun9(query):
    global a
    global sim

    if(query.data == "SIM8"):
        sim += 2
        sql =f"""update tab_main set Pergunta8 = 'Sim' where ID = {a}"""
    else:
        sql =f"""update tab_main set Pergunta8 = 'Não' where ID = {a}"""
        
    inserir(vcon, sql)

    bot.send_message(query.message.chat.id, "Pergunta 9\n\n\nÉ um investimento escasso que incentiva a tomar uma decisão rápida?", reply_markup=pergunta9())



#Pergunta 8
def pergunta8():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("SIM", callback_data="SIM8"),
                               InlineKeyboardButton("NÃO", callback_data="NAO8"))
    return markup

@bot.callback_query_handler(lambda query: query.data == "NAO7" or query.data =="SIM7")
def Pergun8(query):
    global a
    global sim

    if(query.data == "SIM7"):
        sim += 1
        sql =f"""update tab_main set Pergunta7 = 'Sim' where ID = {a}"""
    else:
        sql =f"""update tab_main set Pergunta7 = 'Não' where ID = {a}"""
        
    inserir(vcon, sql)

    bot.send_message(query.message.chat.id, "Pergunta 8\n\n\nVocê foi convidado por um amigo/conhecido para fazer parte do investimento?", reply_markup=pergunta8())


#Pergunta 7
def pergunta7():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("SIM", callback_data="SIM7"),
                               InlineKeyboardButton("NÃO", callback_data="NAO7"))
    return markup

@bot.callback_query_handler(lambda query: query.data == "SIM6" or query.data == "NAO6")
def Pergu7(query):  
    global a
    global sim 
    if(query.data == "SIM6"):
        sql =f"""update tab_main set Pergunta6 = 'Sim' where ID = {a}"""
        sim += 1
    else:
        sql =f"""update tab_main set Pergunta6 = 'Não' where ID = {a}"""
        
    inserir(vcon, sql)
    
    bot.send_message(query.message.chat.id, "Pergunta 7\n\n\nVocê foi chamado para algum evento específico sobre o investimento?", reply_markup=pergunta7())





#Pergunta 6
def pergunta6():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("SIM", callback_data="SIM6"),
                               InlineKeyboardButton("NÃO", callback_data="NAO6"))
    return markup

@bot.callback_query_handler(lambda query: query.data == "SIM5" or query.data == "NAO5")
def Pergu6(query):
    global a
    global sim
    if(query.data == "SIM5"):
        sql =f"""update tab_main set Pergunta5 = 'Sim' where ID = {a}"""
        sim += 2
    else:
        sql =f"""update tab_main set Pergunta5 = 'Não' where ID = {a}"""

    inserir(vcon, sql)
    
    bot.send_message(query.message.chat.id, "Pergunta 6\n\n\nFoi solicitado a você alguma senha pessoal?", reply_markup=pergunta6())



#Pergunta 5
def pergunta5():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("SIM", callback_data="SIM5"),
                               InlineKeyboardButton("NÃO", callback_data="NAO5"))
    return markup

@bot.callback_query_handler(lambda query: query.data == "SIM4" or query.data ==  "NAO4")
def Pergu5(query):
    global a
    global sim 
    if(query.data == "SIM4"):
        sql =f"""update tab_main set Pergunta4 = 'Sim' where ID = {a}"""
    else:
        sql =f"""update tab_main set Pergunta4 = 'Não' where ID = {a}"""
        sim += 1

    inserir(vcon, sql)

    bot.send_message(query.message.chat.id, "Pergunta 5\n\n\nA compra será realizada por terceiros?", reply_markup=pergunta5())




#Pergunta 4
def pergunta4():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("SIM", callback_data="SIM4"),
                               InlineKeyboardButton("NÃO", callback_data="NAO4"))
    return markup

@bot.callback_query_handler(lambda query: query.data == "SIM3" or query.data == "NAO3")
def Pergu4(query):
    global a
    global sim 
    if(query.data == "SIM3"):
        sql =f"""update tab_main set Pergunta3 = 'Sim' where ID = {a}"""
    else:
        sql =f"""update tab_main set Pergunta3 = 'Não' where ID = {a}"""
        sim += 1

    inserir(vcon, sql)

    bot.send_message(query.message.chat.id, "Pergunta 4\n\n\nVocê seria capaz de convencer outra pessoa a fazer este investimento?", reply_markup=pergunta4())





#Pergunta 3
def pergunta3():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("SIM", callback_data="SIM3"),
                               InlineKeyboardButton("NÃO", callback_data="NAO3"))
    return markup

@bot.callback_query_handler(lambda query: query.data == "SIM2" or query.data =="NAO2")
def Pergu3(query):
    global a
    global sim 
    if(query.data == "SIM2"):
        sql =f"""update tab_main set Pergunta2 = 'Sim' where ID = {a}"""
        sim += 2
    else:
        sql =f"""update tab_main set Pergunta2 = 'Não' where ID = {a}"""

    inserir(vcon, sql)

    bot.send_message(query.message.chat.id, "Pergunta 3\n\n\nVocê pesquisou se a empresa tem cadastro na CVM?", reply_markup=pergunta3())



#Pergunta 2
def pergunta2():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("SIM", callback_data="SIM2"),
                               InlineKeyboardButton("NÃO", callback_data="NAO2"))
    return markup

@bot.callback_query_handler(lambda query: query.data == "SIM1" or query.data =="NAO1")
def Pergu2(query):
    global a
    global sim 
    if (query.data == "SIM1"):
        sql =f"""update tab_main set Pergunta1 = 'Sim' where ID = {a}"""
        sim += 2
    else:
        sql =f"""update tab_main set Pergunta1 = 'Não' where ID = {a}"""

    inserir(vcon, sql) 

    bot.send_message(query.message.chat.id, "Pergunta 2\n\n\nFoi dito que o investimento é de baixo risco?", reply_markup=pergunta2())




#Pergunta 1
def pergunta1():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("SIM", callback_data="SIM1"),
                               InlineKeyboardButton("NÃO", callback_data="NAO1"))
    return markup

@bot.callback_query_handler(lambda query: query.data == "INICIAR")
def Inicio(query):
    global sim
    sim = 0
    bot.send_message(query.message.chat.id, "Pergunta 1\n\n\nO retorno oferecido é elevado quando comparado a outros disponíveis nos bancos?", reply_markup=pergunta1())




def continuar():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Continuar!", callback_data="INICIAR"))                                                                                                                                                                                                                                                                                                                                                                                                
    return markup


@bot.callback_query_handler(lambda query: query.data != "IN")
def Inicio(query):
    global a
    estado = (dic[query.data])
    vsql =f"""update tab_main set Estado = '{estado}' where ID = {a}"""
    inserir(vcon, vsql) 
    bot.send_message(query.message.chat.id, "Iniciando o questionario!", reply_markup=continuar())


#Seleção do estado brasileiro
def estadobotao():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    for x in dic:
        markup.add(InlineKeyboardButton(x, callback_data=x))
    return markup

@bot.callback_query_handler(lambda query: query.data == "IN")
def iniciandoteste(query):
    bot.send_message(query.message.chat.id, "Para meios acadêmicos, por favor! selecione a sigla do seu estado...", reply_markup=estadobotao())
    bot.send_message(query.message.chat.id, "Após selecionar seu estado, iniciaremos o questionario!")
   


#Contatar desenvolvedor
@bot.callback_query_handler(lambda query: query.data == "DEV")
def Dev(query):
    bot.send_message(query.message.chat.id, "Reporte o erro no Email a seguir: gabrieldsa1609@gmail.com")
    bot.send_message(query.message.chat.id, "Agradecemos o seu feedbeck!!!")


def verificar(mensagem):
    return True

#Mensagem menu
def Menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Iniciar", callback_data="IN"),
                               InlineKeyboardButton("Contatar desenvolvedor", callback_data="DEV"))
    return markup

@bot.message_handler(func=verificar)
def responder(mensagem):
    nome = str(mensagem.chat.first_name) +" "+ str(mensagem.chat.last_name)
    user_first_name = str(mensagem.chat.first_name)
    
    data_atual = datetime.now()
    data = data_atual.strftime('%d/%m/%Y %H:%M')
   
    sqlselect =f"""SELECT count(ID) FROM tab_main"""
    try:
        c = vcon.cursor()
        c.execute(sqlselect)
        global a
        a =  c.fetchone()[0]
        a += 1
        vsql =f"""INSERT INTO tab_main (Nome, ID) VALUES('{nome}', {a})"""
        inserir(vcon, vsql) 
        datasql =f"""update tab_main set DataInicio = '{data}' where ID = {a}"""
        inserir(vcon,datasql)
        vcon.commit()
    except Error as ex:
        print(ex)

    texto = f"""
...........................MENU...........................\n\n
Olá, {user_first_name}, seja bem vindo ao bot Cripto!

Se caso encontrar algum erro, por favor, contate o desenvolvedor"""
    bot.reply_to(mensagem, texto, reply_markup=Menu())



bot.polling()
