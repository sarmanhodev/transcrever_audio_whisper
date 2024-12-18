# transcrever_audio_whisper

🎙️ Assistente Virtual com Whisper e gTTS
Este é um projeto de uma assistente virtual em Python que utiliza o modelo Whisper para transcrição de áudio, reconhecimento de voz do Google, e o gTTS para geração e reprodução de respostas em áudio.


✨ Funcionalidades
🎤 Reconhecimento de voz: Ouvindo comandos de voz em português utilizando a biblioteca speech_recognition.
🧠 Transcrição de áudio: Utiliza o modelo Whisper para transcrever as respostas geradas.
🔊 Respostas em voz: Geração e reprodução de áudio com a biblioteca gTTS integrada ao pygame.
⚙️ Comando de saída: O sistema reconhece o comando "sair" para encerrar o programa.



🛠️ Tecnologias e Dependências
Dependência	e Descrição
whisper -	Modelo Whisper para transcrição de áudio.
speech_recognition -	Reconhecimento de voz para capturar comandos.
gTTS -	Geração de áudio a partir de texto.
pygame -	Reprodução de áudio.
os, time, warnings -	Ferramentas auxiliares nativas do Python.

🔧 Instalação
1. Clone o repositório:
  git clone https://github.com/sarmanhodev/transcrever_audio_whisper.git
  cd transcrever_audio_whisper

2. Crie um ambiente virtual (recomendado):
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows

3. Instale as dependências:
   pip install -r requirements.txt

   Nota: O arquivo requirements.txt deve conter:
   openai-whisper
   SpeechRecognition
   gTTS
   pygame


4. Baixe o modelo Whisper: O modelo base será baixado automaticamente ao iniciar o script pela primeira vez.


🚀 Como usar
1. Execute o script principal:
   python main.py

2. Aguarde o início do assistente e fale um comando no microfone.
3. Para encerrar o programa, aperte as teclas CTRL+C

📝 Exemplo de Uso
Fluxo básico do assistente:
1. Ouvindo Comando:

    "Aguarde... Estou ouvindo."

2. Reconhecimento de Fala:

    "Você disse: Qual é a previsão do tempo hoje?"

3.  Geração e Reprodução de Resposta:

      -A resposta é convertida em áudio com gTTS.
      -O áudio é reproduzido usando pygame.
      -A resposta gerada é transcrita utilizando Whisper:
      -"Transcrição do áudio: Qual é a previsão do tempo hoje?"

4. Comando de saída:
   Para encerrar o programa, aperte as teclas CTRL+C
   
    
⚠️ Observações
   Avisos do Whisper: O script desabilita os avisos relacionados ao uso de FP16 no CPU, garantindo uma execução mais limpa.
   Arquivos temporários: O arquivo de áudio gerado (resposta.mp3) é removido automaticamente após a reprodução.

🙌 Agradecimentos
Whisper - Modelo de transcrição de áudio. (https://github.com/openai/whisper)
Google Text-to-Speech (gTTS) (https://gtts.readthedocs.io/en/latest/)
SpeechRecognition (https://pypi.org/project/SpeechRecognition/)
Pygame (https://pypi.org/project/pygame/)



  Desenvolvido por Diego Sarmanho
