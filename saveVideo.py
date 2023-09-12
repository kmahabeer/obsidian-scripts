import subprocess
import uuid
import os
import pyperclip

current_dir = os.getcwd()
save_dir = "References/Videos/attachments"
os.chdir("..")
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
else:
    os.chdir(save_dir)

# Ask user for video URL
video_url = input("Enter the URL of the video: ")

print("\n---Media Type---")
print("0 - 1080p video + audio")
print("1 - audio only")
option = input("Select an option for media type: ")

if option == "1":
    isGifCompress = "0"
else:
    print("\n---Compression---")
    print("0 - do NOT compress")
    print("1 - compression")
    isGifCompress = input("Select an option for compression: ")

# Generate a UUID
uuid_str = str(uuid.uuid4())

if option == "0":
    # Download the video using yt-dlp
    download_cmd = f'yt-dlp -f "bv[height<=1080]+ba/b" --add-metadata --embed-thumbnail -o "ref-{uuid_str}.%(ext)s" {video_url}'
    subprocess.run(download_cmd, shell=True)
elif option == "1":
    # Download audio only from the video using yt-dlp
    download_audio_cmd = (
        f'yt-dlp -f "ba[ext=m4a]" -o "ref-{uuid_str}.%(ext)s" {video_url}'
    )
    subprocess.run(download_audio_cmd, shell=True)
output_string = "Video download complete."

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

            # Convert the downloaded video to a GIF
            vid2gif_cmd = f'ffmpeg -i "ref-{uuid_str}.{ext}" -filter:v "fps={fps},setpts={1/speed}*PTS,scale={scaleWidth}:-1" -y "ref-{uuid_str}-speed_{speed}x-FPS_{fps}-w{scaleWidth}.gif"'
            subprocess.run(vid2gif_cmd, shell=True)
            output_string += "\nVideo to GIF conversion complete."

            if isGifCompress == "1":
                for lossy in lossy_values:
                    for color in color_values:
                        # Compress the video
                        compress_cmd = f'gifsicle -O3 --lossy={lossy} --colors {color} "ref-{uuid_str}-speed_{speed}x-FPS_{fps}-w{scaleWidth}.gif" -o "ref-{uuid_str}-speed_{speed}x-FPS_{fps}-w{scaleWidth}-compressed-lossy_{lossy}-colors_{color}.gif"'
                        subprocess.run(compress_cmd, shell=True)
                        output_string += "\nGIF compression complete."

os.chdir(current_dir)
print(output_string)
print(f"Video file: ref-{uuid_str}.{ext}s")
print(f"Gif file: ref-{uuid_str}-speed_{speed}x-FPS_{fps}-w{scaleWidth}.gif")
pyperclip.copy(f"ref-{uuid_str}-speed_{speed}x-FPS_{fps}-w{scaleWidth}.gif")
