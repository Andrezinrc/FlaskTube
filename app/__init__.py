from flask import Flask, render_template, request, flash, send_from_directory
from pydub import AudioSegment
import yt_dlp
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
        caminho_salvar = "/storage/emulated/0/Download"

        if request.args.get("download_iniciado"):
            if url:
                ydl_opts = {
                    'format': 'best',
                    'outtmpl': os.path.join(caminho_salvar, '%(title)s.%(ext)s'),
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                download_sucesso = True
                flash("Download feito com sucesso")
    except Exception as erro:
        flash("Houve um erro ao baixar")
        print("Houve um erro:", erro)

    return render_template("baixar_video.html", download_sucesso=download_sucesso)

@app.route("/baixar_musica", methods=["GET"])
def baixar_musica():
    download_sucesso = False
    try:
        url = request.args.get("url")
        caminho_salvar = "/storage/emulated/0/Download"

        if url:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(caminho_salvar, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            download_sucesso = True
            flash("Download feito com sucesso")
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
        print("musica: ", musica)
    return render_template("ver_musicas.html", musicas=musicas, caminho_musica=caminho_musica)

@app.route("/ver_musicas/<musica_nome>")
def reproduzir_musica(musica_nome):
    caminho_musica = "/storage/emulated/0/Download"
    return send_from_directory(caminho_musica, musica_nome)

if __name__ == "__main__":
    app.run(debug=True)
