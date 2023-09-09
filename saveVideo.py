import subprocess
import uuid
import os.path

# Ask user for video URL
video_url = input("Enter the URL of the video: ")

# Generate a UUID
uuid_str = str(uuid.uuid4())

# # Download the video using yt-dlp
download_cmd = f'yt-dlp -f "bv[height<=1080]+ba/b" --add-metadata --embed-thumbnail -o "ref-{uuid_str}.%(ext)s" {video_url}'
subprocess.run(download_cmd, shell=True)

# GIF parameters
fps_values = [12]
speed_values = [2]
scale_values = [480]

# Compression parameters
lossy_values = [90]
color_values = [128]

for fps in fps_values:
    for speed in speed_values:
        for scaleWidth in scale_values:
            if os.path.exists(f"ref-{uuid_str}.mkv"):
                ext = "mkv"
            if os.path.exists(f"ref-{uuid_str}.mp4"):
                ext = "mp4"
            else:
                print(f"Neither ref-{uuid_str}.mp4 nor ref-{uuid_str}.mkv exists.")
                continue

            # Convert the downloaded video to a GIF
            vid2gif_cmd = f'ffmpeg -i "ref-{uuid_str}.{ext}" -filter:v "fps={fps},setpts={1/speed}*PTS,scale={scaleWidth}:-1" -y "ref-{uuid_str}-speed_{speed}x-FPS_{fps}-w{scaleWidth}.gif"'
            subprocess.run(vid2gif_cmd, shell=True)

            for lossy in lossy_values:
                for color in color_values:
                    # Compress the video
                    compress_cmd = f'gifsicle -O3 --lossy={lossy} --colors {color} "ref-{uuid_str}-speed_{speed}x-FPS_{fps}-w{scaleWidth}.gif" -o "ref-{uuid_str}-speed_{speed}x-FPS_{fps}-w{scaleWidth}-compressed-lossy_{lossy}-colors_{color}.gif"'
                    subprocess.run(compress_cmd, shell=True)

print("\nVideo downloaded, converted to GIF, and compressed.")
