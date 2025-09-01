# pyinstaller -F --onefile <filename>.py
import os
import sys
import traceback
import multiprocessing
import re

isDev = False

def run_command (command):
    import subprocess
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    sp = subprocess.Popen(command, startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = sp.communicate()
    stderr = stderr.decode("utf-8")


def processingTask(data):

    delete_lip_files = data[0]
    delete_wav_files = data[1]
    make_fuz_files = data[2]
    skip_existing = data[3]
    data = data[4]

    text = data[0]
    text = re.sub(r'[^a-zA-Z_\s]+', '', text)
    wav_path = data[1]
    fpath = "" if isDev else "/resources/app"

    resampled_path = wav_path.replace(".wav", "_r.wav")
    lip_output_path = wav_path.replace(".wav", ".lip")
    fuz_path = lip_output_path.replace(".lip", ".fuz")

    if skip_existing and (os.path.exists(lip_output_path) or (make_fuz_files and os.path.exists(fuz_path))):
        pass
    else:
        dir_path = os.path.dirname(os.path.realpath(__file__))

        # Run FaceFXWrapper to create the .lip file
        # run_command(f'{dir_path}/plugins/lip_fuz/FaceFXWrapper.exe USEnglish {dir_path}/plugins/lip_fuz/FonixData.cdf "{wav_path}" "{lip_output_path}" "{text}"')
        run_command(f'{dir_path}{fpath}/plugins/lip_fuz/FaceFXWrapper.exe USEnglish {dir_path}{fpath}/plugins/lip_fuz/FonixData.cdf "{wav_path}" "{resampled_path}" "{lip_output_path}" "{text}"')

    if skip_existing and make_fuz_files and os.path.exists(fuz_path):
        pass
    else:
        # Resample the .wav to 44100Hz
        # Create .xwm file
        # xwm_path = resampled_wav_path.replace(".wav", ".xwm")
        xwm_path = wav_path.replace(".wav", ".xwm")
        # run_command(f'{dir_path}/plugins/lip_fuz/xWMAEncode.exe "{resampled_wav_path}" "{xwm_path}"')
        run_command(f'{dir_path}{fpath}/plugins/lip_fuz/xWMAEncode.exe "{wav_path}" "{xwm_path}"')

        # Create the .fuz file
        run_command(f'{dir_path}{fpath}/plugins/lip_fuz/fuz_extractor.exe -c "{fuz_path}" "{lip_output_path}" "{xwm_path}"')

        # Clean up
        os.remove(xwm_path)


    # Clean up
    if os.path.exists(resampled_path):
        os.remove(resampled_path)

    if delete_lip_files:
        os.remove(lip_output_path)
    if delete_wav_files:
        os.remove(wav_path)


if __name__ == '__main__':
    # On Windows calling this function is necessary.
    multiprocessing.freeze_support()

    fpath = "" if isDev else "/resources/app"

    try:
        print("start")

        num_processes = int(sys.argv[1])
        delete_lip_files = int(sys.argv[2])
        delete_wav_files = int(sys.argv[3])
        make_fuz_files = int(sys.argv[4])
        skip_existing = int(sys.argv[5])

        dir_path = os.path.dirname(os.path.realpath(__file__))

        if os.path.exists(f'{dir_path}{fpath}/plugins/lip_fuz/input.txt'):
            with open(f'{dir_path}{fpath}/plugins/lip_fuz/input.txt') as f:
                lines = f.read().split("\n")
                lines = [[delete_lip_files, delete_wav_files, make_fuz_files, skip_existing, line.split("|")] for line in lines]

            workers = int(num_processes) if num_processes>0 else max(1, multiprocessing.cpu_count()-1)
            workers = min(len(lines), workers)

            pool = multiprocessing.Pool(workers)
            results = pool.map(processingTask, lines)
            pool.close()
            pool.join()
        else:
            with open("DEBUG.txt", "w+") as f:
                f.write(f'No: {dir_path}{fpath}/plugins/lip_fuz/input.txt')
    except:
        with open("ERROR.txt", "w+") as f:
            f.write(traceback.format_exc())

