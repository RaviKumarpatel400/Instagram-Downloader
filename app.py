from flask import Flask, render_template, request, send_file, redirect, url_for
import yt_dlp
import os

app = Flask(__name__)

# Directory to save the downloaded video
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form['url']
    
    try:
        # Options for yt_dlp to download the video
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'format': 'mp4',  # Download the video in mp4 format
        }

        # Download the video from Instagram using yt_dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_title = info_dict.get('title', None)
            video_filename = ydl.prepare_filename(info_dict)

        # Redirect the user to download the file
        return send_file(video_filename, as_attachment=True)
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
