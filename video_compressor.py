import os
import subprocess


input_folder = r"C:\Users\oguzh\Desktop\ilayda\takeout-20240525T183809Z-001\Takeout\Google Fotoğraflar\BİTİŞİK\videolar"
output_folder = r"C:\Users\oguzh\Desktop\ilayda\takeout-20240525T183809Z-001\Takeout\Google Fotoğraflar\DONUSUM\videolar"


def get_resolution(input_path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=s=x:p=0", input_path],
        stdout=subprocess.PIPE,
        text=True
    )
    res = result.stdout.strip().split('x')
    width, height = res[0], res[1]
    return int(width), int(height)


def convert_video(input_path, output_path, scale_command):
    command = [
        "ffmpeg",
        '-hwaccel', 'cuda',
        "-i", input_path,
        "-c:v", "hevc_nvenc",
        "-cq", '37',
        "-profile:v", 'main10',
        '-preset', 'slow',
        '-aq-strength', '10',
        '-rc-lookahead', '100',
        '-bf', '4',
        '-b_ref_mode', 'middle',
        '-temporal-aq', '1',
        '-spatial-aq', '1',
        '-c:a', 'copy',
        # "-c:v", "libx265",
        # "-crf", '35',
        *scale_command,
        # '-c:a', 'aac',
        # '-b:a', '128k',
        output_path
    ]
    subprocess.run(command, text=True)


def main():
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Çevrilmiş videoları tekrar çevirmemek için -->
    compressed_videos = os.listdir(output_folder)
    for file in os.listdir(input_folder):
        if any(file in compressed_video for compressed_video in compressed_videos):
            continue
        else:
            input_path = os.path.join(input_folder, file)
            output_path = os.path.join(output_folder, file)
            # Video çözünürlüğünü al
            width, height = get_resolution(input_path)
            scale_command = []
            # Çözünürlüğe göre genişlik ve yükseklik değerlerini belirle
            # if width > 1920 or height > 1920:
            #     scale_command = ["-vf", "scale=iw*0.5:ih*0.5"]

            # Videoyu dönüştür
            convert_video(input_path, output_path, scale_command)
            print(f"{file} dönüştürüldü.")


if __name__ == "__main__":
    main()
