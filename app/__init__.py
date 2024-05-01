from flask import Flask, render_template, request, flash, send_from_directory
from pytube import YouTube
from pydub import AudioSegment
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "euamoprogramar"

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/baixar_video", methods=["GET"])
def baixar_video():
    download_sucesso = False
    try:
        url = request.args.get("url")
        #seu caminho onde deseja salvar
        caminho_salvar = "/storage/emulated/0/Download"
        
        if request.args.get("download_iniciado"):
            if url:
                yt = YouTube(url)
                print(f"Iniciando download: {yt.title}")
                stream = yt.streams.get_highest_resolution()
                stream.download(caminho_salvar)
                download_sucesso = True
                flash(f"Download de {yt.title} feito com sucesso")
    except Exception as erro:
        flash("Houve um erro ao baixar")
        print("Houve um erro: ", erro)

    return render_template("baixar_video.html", download_sucesso=download_sucesso)


@app.route("/baixar_musica", methods=["GET"])
def baixar_musica():
    download_sucesso = False
    try:
        url = request.args.get("url")
        caminho_salvar = "/storage/emulated/0/Download"
        
        if url:
            yt = YouTube(url)
            print(f"Iniciando download: {yt.title}")
            
            stream_audio = yt.streams.filter(only_audio=True).first()
            caminho_video = stream_audio.download(output_path=caminho_salvar)
            
            # Converter o áudio para MP3
            caminho_audio = f"{caminho_salvar}/{yt.title}.mp3"
            clip_video = AudioSegment.from_file(caminho_video)
            clip_video.export(caminho_audio, format="mp3")
            
            os.remove(caminho_video)
            
            download_sucesso = True
            flash(f"Download de {yt.title} feito com sucesso")
    except Exception as erro:
        flash("Houve um erro ao baixar")
        print("Houve um erro:", erro)

    return render_template("baixar_musica.html", download_sucesso=download_sucesso)


@app.route("/ver_videos")
def ver_videos():
    caminho_video = "/storage/emulated/0/Download"
    videos = [f for f in os.listdir(caminho_video) if f.endswith('.mp4')]
    return render_template("ver_videos.html", videos=videos, caminho_video=caminho_video)

@app.route('/ver_videos/<video_nome>')
def reproduzir_video(video_nome):
    caminho_video = "/storage/emulated/0/Download"
    return send_from_directory(caminho_video, video_nome)


@app.route("/ver_musicas")
def ver_musicas():
    caminho_musica = "/storage/emulated/0/Download"
    musicas = [f for f in os.listdir(caminho_musica) if f.endswith('.mp3')]
    for musica in musicas:
        print("musica: ",musica)
    return render_template("ver_musicas.html", musicas=musicas, caminho_musica=caminho_musica)


@app.route("/ver_musicas/<musica_nome>")
def reproduzir_musica(musica_nome):
    caminho_musica = "/storage/emulated/0/Download"
    return send_from_directory(caminho_musica, musica_nome)


if __name__ == "__main__":
    app.run(debug=True)
