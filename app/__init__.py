from flask import Flask, render_template, request, flash
from pytube import YouTube
from pydub import AudioSegment
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "euamoprogramar"

caminho = "/storage/emulated/0"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/baixar_video", methods=["GET"])
def baixar_video():
    download_sucesso = False
    try:
        pasta = request.args.get("pasta")
        url = request.args.get("url")

        caminho_salvar = caminho + ("/" + pasta if pasta else "")
        if url:
            yt = YouTube(url)
            print(f"Iniciando download: {yt.title}")
            stream = yt.streams.get_highest_resolution()
            stream.download(caminho_salvar)
            download_sucesso = True
            flash("Download feito com sucesso")
            flash(yt.title)
    except Exception as erro:
        flash("Houve um erro ao baixar")
        print("Houve um erro: ", erro)

    return render_template("baixar_video.html", download_sucesso=download_sucesso)


@app.route("/baixar_musica", methods=["GET"])
def baixar_musica():
    download_sucesso = False
    try:
        pasta = request.args.get("pasta")
        url = request.args.get("url")

        caminho_salvar = caminho + ("/" + pasta if pasta else "/meu_pytube_musica")

        if url:
            yt = YouTube(url)
            print(f"Iniciando download: {yt.title}")
            flash(yt.title)
            stream_video = yt.streams.get_highest_resolution()
            caminho_video = stream_video.download(output_path=caminho_salvar)
            titulo_video = yt.title
            caminho_audio = f"{caminho_salvar}/{titulo_video}.mp3"
            clip_video = AudioSegment.from_file(caminho_video)
            clip_video.export(caminho_audio, format="mp3")
            download_sucesso = True
            flash("Download feito com sucesso")
    except Exception as erro:
        flash("Houve um erro ao baixar")
        print("Houve um erro: ", erro)

    return render_template("baixar_musica.html", download_sucesso=download_sucesso)

@app.route("/ver_videos")
def ver_videos():
    caminho_video = caminho + "/Download/meu_pytube_video"
    videos = os.listdir(caminho_video)
    for video in videos:
        print("video: ", video)
    return render_template("ver_videos.html", videos=videos, caminho_video=caminho_video)

caminho_video = caminho + "/Download/meu_pytube_video"
@app.route('/ver_videos/<video_nome>')
def reproduzir_video(video_nome):
    return send_from_directory(caminho_video, video_nome)

@app.route("/ver_musicas")
def ver_musicas():
    caminho_musica = caminho + "/Download/meu_pytube_musica"
    musicas = os.listdir(caminho_musica)
    for musica in musicas:
        print("musica: ",musica)
    return render_template("ver_musicas.html", musicas=musicas, caminho_musica=caminho_musica)

caminho_video = caminho + "/Download/meu_pytube_musica"
@app.route("/ver_musicas/<musica_nome>")
def reproduzir_musica(musica_nome):
    return send_from_directory(caminho_video, video_nome)
if __name__ == "__main__":
    app.run(debug=True)
