import whisper
import cohere
import os
import wave
import time
from datetime import datetime
from babel.dates import format_date
import pyaudio
from gtts import gTTS
import pygame
import warnings
from tqdm import tqdm
from docx import Document

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

# Configuração do cliente Cohere
co = cohere.Client('OO9QG57UjoEEwxA0E7x99HELb1fkmM6WIrnXQX64')

# Inicializar o modelo Whisper
modelo = whisper.load_model("base", device="cpu")

# Inicializar o pygame.mixer uma vez
pygame.mixer.init()

# Configurações de gravação
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
DURATION = 20
AUDIO_FILE = "audio_input.wav"

def gerarTexto(texto):
    """Gera texto formal a partir da entrada usando o Cohere."""
    try:
        response = co.generate(
            model='command-xlarge-nightly',
            prompt = f'Corrija o texto abaixo, ajustando apenas erros ortográficos, gramaticais, de acentuação e de pontuação. \
            Mantenha a estrutura, o estilo e as palavras o mais próximo possível do original, sem que haja substituição por outras palavras parecidas.\
            Criar um cabeçalho, com o tema abordado no texto. Além disso,\
            criar outro cabeçalho, escrevendo o nome da pessoa e seu número de matricula, conforme exemplo: Nome: nome da pessoa - Matrícula: número da matrícula\
            . Pular uma linha e iniciar o texto. Ao final do texto, criar uma linha para assinatura e, abaixo da linha, conter o nome da pessoa e seu número de matrícula.\
            :\n\nTexto: {texto}',
            max_tokens=500,
            temperature=0.7
        )
        return response.generations[0].text.strip()
    except Exception as e:
        print(f"Erro ao gerar texto: {e}")
        return "Erro ao processar o texto."

def gravar_audio():
    """Grava áudio por um período fixo e salva como arquivo WAV."""
    print("Aguarde... Estou ouvindo.")
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    print("\nGravando...\n")
    try:
        for _ in range(0, int(RATE / CHUNK * DURATION)):
            data = stream.read(CHUNK)
            frames.append(data)
    except Exception as e:
        print(f"Erro durante a gravação: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

    with wave.open(AUDIO_FILE, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))
    print("\nGravação concluída!\n")
    
    

def reconhecer_voz():
    """Processa o áudio gravado e retorna o texto reconhecido."""
    gravar_audio()
    try:
        resultado = modelo.transcribe(AUDIO_FILE)
        frase = resultado["text"]
        print(f"Você disse: {frase}")
        return frase
    except Exception as e:
        print(f"Erro ao transcrever áudio: {e}")
        return None
    finally:
        if os.path.exists(AUDIO_FILE):
            os.remove(AUDIO_FILE)



def reproduzir_resposta(resposta):
    """Gera áudio com a resposta e reproduz."""
    arquivo_audio = "resposta.mp3"
    
    # Remover o arquivo se ele existir
    if os.path.exists(arquivo_audio):
        os.remove(arquivo_audio)

    try:
        # Criar o arquivo de áudio usando gTTS
        tts = gTTS(text=resposta, lang='pt')
        tts.save(arquivo_audio)
        
        # Reproduzir o áudio
        pygame.mixer.music.load(arquivo_audio)
        pygame.mixer.music.play()
        
        # Esperar até que a reprodução seja concluída
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        
        # Liberar o arquivo de áudio
        pygame.mixer.music.unload()
        os.remove(arquivo_audio)
    except Exception as e:
        print(f"Erro ao reproduzir ou remover áudio: {e}")




def criarArquivoTexto(texto):
    """Função responsável por criar um arquivo Word (.docx) contendo o texto formatado."""
    # Garante que o diretório "arquivos" exista
    os.makedirs("arquivos", exist_ok=True)
    
    try:
        # Cria um novo documento Word
        document = Document()
        
        # Captura a data atual no formato desejado
        dataAtual = format_date(datetime.now(), format="d 'de' MMMM 'de' yyyy", locale="pt_BR")
        cabecalho = f"Rio de Janeiro, {dataAtual}"
        document.add_paragraph(cabecalho)  # Adiciona a data no início do documento

        
        # Divide o texto em linhas
        linhas = texto.splitlines()
        total_linhas = len(linhas)
        
        # Adiciona cada linha ao documento com uma barra de progresso
        for linha in tqdm(linhas, total=total_linhas, desc="Criando arquivo Word", ascii=True, ncols=80, unit="linha"):
            document.add_paragraph(linha)  # Adiciona uma linha como parágrafo
            time.sleep(0.5)  # Simula o tempo de escrita


        # Salva o arquivo Word
        caminho_arquivo = "arquivos/texto.docx"
        document.save(caminho_arquivo)
        
        print(f"\nArquivo Word criado com sucesso em: {caminho_arquivo}")
    except Exception as e:
        print(f"Erro ao criar o arquivo Word: {e}")

            
            

def main():
    """Loop principal do assistente."""
    try:
        while True:
            print("Assistente iniciado...")
            ativacao = reconhecer_voz()
            
            if ativacao:
                if "sair" in ativacao.lower():
                    print("Encerrando o programa.")
                    break
                
                # Gerar texto formal e responder
                texto_formatado = gerarTexto(ativacao)
                print(f"\nTexto formatado: {texto_formatado} \n")
                
                criarArquivoTexto(texto_formatado)
                
                #reproduzir_resposta(texto_formatado)
    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário.")
    finally:
        pygame.mixer.quit()

if __name__ == "__main__":
    main()
