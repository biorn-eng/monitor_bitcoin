from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import requests
import threading
import os
import sys

# CORES
co0 = "#4444"
co1 = "#000000"
co2 = "#ffffff"
fundo = "#000125"

# Função para atualizar a posição da janela
def update_position(event):
    janela.geometry(f'+{event.x_root}+{event.y_root}')

# Funções para manipulação da janela
def close_window():
    janela.destroy()


def start_move(event):
    janela.x = event.x
    janela.y = event.y

def do_move(event):
    x = janela.winfo_pointerx() - janela.x
    y = janela.winfo_pointery() - janela.y
    janela.geometry(f'+{x}+{y}')

# JANELA
janela = Tk()
janela.title('Bitcoin Price Tracker')
janela.geometry('300x100')

# Remove a borda padrão da janela
janela.overrideredirect(True)

# Define a cor de fundo da janela
janela.configure(bg=fundo)

# Define a posição inicial da janela
screen_width = janela.winfo_screenwidth()
screen_height = janela.winfo_screenheight()
window_width = 280
window_height = 200
x = screen_width - window_width
y = screen_height - window_height
janela.geometry(f'{window_width}x{window_height}+{x}+{y}')

# Frame para os controles personalizados
frame_top = Frame(janela, bg=co1, height=30)
frame_top.pack(fill=X)

# Botão de fechar
close_btn = Button(frame_top, text='X', command=close_window, bg=co1, fg=co2, bd=0, font=('Arial', 10))
close_btn.pack(side=RIGHT)

# Função para buscar os dados da API em uma thread separada
# Função para buscar os dados da API em uma thread separada
def buscar_dados_api():
    api_link = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,eur,brl'
    try:
        response = requests.get(api_link)
        dados = response.json()
        
        # Adicionando print para depuração
        print(dados)  # Imprime a resposta da API para depuração

        # Atualiza os valores na interface
        valor_usd = float(dados['bitcoin']['usd'])
        valor_formatado_usd = "${:,.3f}".format(valor_usd)
        l_p_usd['text'] = 'Em Dolar:' + valor_formatado_usd

        valor_brl = float(dados['bitcoin']['brl'])
        valor_formatado_brl = "R${:,.3f}".format(valor_brl)
        l_p_real['text'] = 'Em Reais:' + valor_formatado_brl

        valor_eur = float(dados['bitcoin']['eur'])
        valor_formatado_eur = "€{:,.3f}".format(valor_eur)
        l_p_euro['text'] = 'Em Euro:' + valor_formatado_eur
    except Exception as e:
        print(f"Erro ao obter dados da API: {e}")

    # Agendar a próxima atualização após 1000ms (1 segundo)
    screen.after(20000, iniciar_thread)


# Função para iniciar a thread
def iniciar_thread():
    threading.Thread(target=buscar_dados_api).start()

# Frame principal da janela
frame_cima = Frame(janela, width=300, height=50, bg=co1, pady=0, padx=0, relief='flat')
frame_cima.pack()

screen = Frame(janela, width=300, height=150, bg=fundo, pady=0, padx=0, relief='flat')
screen.pack()

# CONFIGURANDO O FRAME CIMA
try:
    # Caminho da imagem ajustado
    caminho_base = getattr(sys, '_MEIPASS', os.path.abspath("."))
    caminho_imagem = os.path.join(caminho_base, 'images/bit2.png')

    imagem = Image.open(caminho_imagem)
    imagem = imagem.resize((30, 30), Image.LANCZOS)
    imagem = ImageTk.PhotoImage(imagem)

    l_icon = Label(frame_cima, image=imagem, compound=LEFT, bg=co1, relief=FLAT)
    l_icon.place(x=10, y=6)
except Exception as e:
    print(f"Erro ao carregar a imagem: {e}")

l_name = Label(frame_cima, text='Bitcoin Price Tracker', bg=co1, fg=co2, relief=FLAT, anchor='center', font=('Arial', 16))
l_name.place(x=50, y=5)

# CONFIGURANDO SCREEN
l_p_usd = Label(screen, text='', bg=fundo, fg=co2, relief=FLAT, anchor='center', font=('Arial', 14))
l_p_usd.place(x=10, y=18)

l_p_real = Label(screen, text='', bg=fundo, fg=co2, relief=FLAT, anchor='center', font=('Arial', 12))
l_p_real.place(x=10, y=60)

l_p_euro = Label(screen, text='', bg=fundo, fg=co2, relief=FLAT, anchor='center', font=('Arial', 12))
l_p_euro.place(x=10, y=80)

# Eventos para arrastar a janela
frame_top.bind('<Button-1>', start_move)
frame_top.bind('<B1-Motion>', do_move)

# Inicia a primeira atualização
iniciar_thread()

janela.mainloop()
