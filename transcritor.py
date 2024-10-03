import PySimpleGUI as sg
import whisper
import os
from googletrans import Translator
from time import sleep

# Inicializando o modelo Whisper e o tradutor
model = whisper.load_model("base")
translator = Translator()

# Lista de idiomas disponíveis (lista mais extensa)
languages = {
    "Português": "pt",
    "Inglês": "en",
    "Espanhol": "es",
    "Francês": "fr",
    "Alemão": "de",
    "Italiano": "it",
    "Russo": "ru",
    "Chinês (Simplificado)": "zh-CN",
    "Japonês": "ja"
}

# Layout da interface
layout = [
    [sg.Text("Selecione um arquivo de áudio para transcrever:")],
    [sg.Input(key="-FILE-", enable_events=True), sg.FileBrowse("Procurar", file_types=(("Audio Files", "*.mp3;*.wav;*.m4a"),))],
    [sg.Text("Idioma de tradução:"), sg.Combo(list(languages.keys()), key="-LANG-", default_value="Português")],
    [sg.Button("Transcrever"), sg.Button("Traduzir"), sg.Button("Salvar como texto"), sg.Button("Sair")],
    [sg.ProgressBar(100, orientation='h', size=(30, 20), key="-PROGRESS-", visible=False)],
    [sg.Multiline(key="-OUTPUT-", size=(60, 15), disabled=True)]
]

# Criando a janela
window = sg.Window("Transcritor e Tradutor de Áudio", layout)

# Variável para armazenar o texto transcrito
transcribed_text = ""

# Função para salvar o texto em um arquivo
def save_text(text):
    save_path = sg.popup_get_file("Salvar como", save_as=True, no_window=True, file_types=(("Text Files", "*.txt"),))
    if save_path:
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(text)
        sg.popup("Arquivo salvo com sucesso!")

# Loop de eventos
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "Sair":
        break

    if event == "Transcrever":
        audio_path = values["-FILE-"]
        if os.path.exists(audio_path):
            window["-PROGRESS-"].update(visible=True)
            window["-OUTPUT-"].update("Transcrevendo o áudio, aguarde...")
            window.refresh()

            # Simulação de barra de progresso (não reflete o tempo real de processamento)
            for i in range(0, 101, 20):
                window["-PROGRESS-"].update(i)
                sleep(0.5)

            # Transcrição usando Whisper
            result = model.transcribe(audio_path)
            transcribed_text = result['text']

            # Exibir o texto transcrito
            window["-OUTPUT-"].update(transcribed_text)
            window["-PROGRESS-"].update(100)

        else:
            sg.popup_error("Arquivo não encontrado! Por favor, selecione um arquivo válido.")
        window["-PROGRESS-"].update(visible=False)

    if event == "Traduzir":
        if transcribed_text:
            window["-PROGRESS-"].update(visible=True)
            window["-OUTPUT-"].update("Traduzindo o texto, aguarde...")
            window.refresh()

            # Simulação de barra de progresso para tradução
            for i in range(0, 101, 20):
                window["-PROGRESS-"].update(i)
                sleep(0.5)

            # Pega o idioma selecionado
            target_language = languages[values["-LANG-"]]
            # Traduz o texto
            translated_text = translator.translate(transcribed_text, dest=target_language).text

            # Exibe o texto traduzido
            window["-OUTPUT-"].update(translated_text)
            transcribed_text = translated_text  # Atualiza o texto transcrito para permitir salvar o traduzido
            window["-PROGRESS-"].update(100)

        else:
            sg.popup_error("Primeiro, transcreva o áudio antes de traduzir.")
        window["-PROGRESS-"].update(visible=False)

    if event == "Salvar como texto":
        if transcribed_text:
            save_text(transcribed_text)
        else:
            sg.popup_error("Nenhum texto disponível para salvar.")

window.close()