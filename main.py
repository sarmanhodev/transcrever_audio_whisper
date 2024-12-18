import whisper
import os
import time
import speech_recognition as sr
from gtts import gTTS
import pygame
import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")


# Inicializar o modelo Whisper
modelo = whisper.load_model("base", device="cpu")


# Inicializar o pygame.mixer uma vez
pygame.mixer.init()

def reconhecer_voz():
    reconhecedor = sr.Recognizer()
    with sr.Microphone() as fonte:
        print("Aguarde... Estou ouvindo.")
        reconhecedor.adjust_for_ambient_noise(fonte)
        audio = reconhecedor.listen(fonte)
        
        try:
            frase = reconhecedor.recognize_google(audio, language="pt-BR")
            print(f"Você disse: {frase}")
            return frase
        except sr.UnknownValueError:
            print("Desculpe, não consegui entender.")
            return None
        except sr.RequestError:
            print("Erro ao conectar ao serviço de reconhecimento de voz.")
            return None

def reproduzir_resposta(resposta):
    arquivo_audio = "resposta.mp3"
    
    # Remover o arquivo se ele existir
    if os.path.exists(arquivo_audio):
        os.remove(arquivo_audio)

    # Criar o arquivo de áudio usando gTTS
    tts = gTTS(text=resposta, lang='pt')
    tts.save(arquivo_audio)
    
    # Transcrever o áudio usando Whisper
    resposta_transcrita = transcrever_audio(arquivo_audio)
    print(f"Transcrição do áudio: {resposta_transcrita}")
    
    # Reproduzir o áudio
    pygame.mixer.music.load(arquivo_audio)
    pygame.mixer.music.play()
    
    # Esperar até que a reprodução seja concluída
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    
    # Liberar o arquivo de áudio
    pygame.mixer.music.unload()
    
    # Remover o arquivo de áudio
    os.remove(arquivo_audio)


def transcrever_audio(arquivo_audio):
    try:
        resultado = modelo.transcribe(arquivo_audio)
        return resultado["text"]
    except Exception as e:
        print(f"Erro ao transcrever áudio: {e}")
        return None

def main():
    try:
        while True:
            print("Assistente iniciado...")
            ativacao = reconhecer_voz()
            
            if ativacao:
                if "sair" in ativacao.lower():
                    print("Encerrando o programa.")
                    break
                
                # Resposta do sistema
                reproduzir_resposta(ativacao)
    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário.")
    finally:
        pygame.mixer.quit()

if __name__ == "__main__":
    main()
