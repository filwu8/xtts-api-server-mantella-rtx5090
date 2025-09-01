import os
import re
import queue
import threading
import subprocess
import multiprocessing as mp

logger = setupData["logger"]
isDev = setupData["isDev"]


def run_command (command):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    sp = subprocess.Popen(command, startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = sp.communicate()
    stderr = stderr.decode("utf-8")
    # logger.log(f'Running command: {command}')
    # if len(stderr):
    #     logger.log(f'Error running command: {command}')
    #     logger.log(f'Error: {stderr}')
    # else:
    #     logger.log(f'Command: {command}')
    #     logger.log(f'Output: {stdout}')


def run_lip_fuz(text, game, wav_path, delete_lip_files=False, delete_wav_files=False, make_fuz_files=True, skip_existing=True):
    resampled_path = wav_path.replace(".wav", "_r.wav")
    lip_output_path = wav_path.replace(".wav", ".lip")
    fuz_path = lip_output_path.replace(".lip", ".fuz")
    root_path = f'.' if isDev else f'./resources/app' # The root directories are different in dev/prod

    if skip_existing and (os.path.exists(lip_output_path) or (make_fuz_files and os.path.exists(fuz_path))):
        pass
    else:
        # Run FaceFXWrapper to create the .lip file
        run_command(f'{root_path}/plugins/lip_fuz/FaceFXWrapper.exe {game} USEnglish {root_path}/plugins/lip_fuz/FonixData.cdf "{wav_path}" "{resampled_path}" "{lip_output_path}" "{text}"')

    if not make_fuz_files or skip_existing and os.path.exists(fuz_path):
        pass
    else:
        # Create .xwm file
        xwm_path = wav_path.replace(".wav", ".xwm")
        run_command(f'{root_path}/plugins/lip_fuz/xWMAEncode.exe -b 160000 "{wav_path}" "{xwm_path}"')

        # Create the .fuz file
        run_command(f'{root_path}/plugins/lip_fuz/fuz_extractor.exe -c "{fuz_path}" "{lip_output_path}" "{xwm_path}"')

        # Clean up
        if os.path.exists(xwm_path):
            os.remove(xwm_path)


    # Clean up
    if os.path.exists(resampled_path):
        os.remove(resampled_path)

    if delete_wav_files:
        if "output" not in wav_path and "_ffmpeg" not in wav_path: # Attempt to fix case where the preview audio file in the main app is deleted
            os.remove(wav_path)
    if delete_lip_files:
        os.remove(lip_output_path)


def create_lip_fuz_files(data=None):
    global os, re, subprocess, logger, isDev, run_command, run_lip_fuz


    plugin_settings = data["pluginsContext"]["lip_fuz_settings"]
    game = plugin_settings["game"]
    make_fuz_files = 1 if (plugin_settings["make_fuz_files"]=="true" or plugin_settings["make_fuz_files"]==True) else 0
    delete_lip_files = 1 if (plugin_settings["delete_lip_files"]=="true" or plugin_settings["delete_lip_files"]==True) else 0
    delete_wav_files = 1 if (plugin_settings["delete_wav_files"]=="true" or plugin_settings["delete_wav_files"]==True) else 0
    skip_existing = 1 if plugin_settings["skip_existing"]=="true" else 0

    text = "".join(data["letters"]) # Use the post-processed letters rather than the raw input text
    text = text.replace("_", " ")
    text = re.sub(r'[^a-zA-Z\s]+', '', text)
    output_path = data["output_path"] # The output path of the audio file


    run_lip_fuz(text, game, output_path, delete_lip_files=delete_lip_files, delete_wav_files=delete_wav_files, make_fuz_files=make_fuz_files, skip_existing=skip_existing)

def mp_create_lip_fuz_files(data=None):
    global os, subprocess, logger, isDev, run_command, run_lip_fuz

    plugin_settings = data["pluginsContext"]["lip_fuz_settings"]
    game = plugin_settings["game"]
    use_multiprocessing = (plugin_settings["use_multiprocessing"]=="true" or plugin_settings["use_multiprocessing"]==True)
    make_fuz_files = 1 if (plugin_settings["make_fuz_files"]=="true" or plugin_settings["make_fuz_files"]==True) else 0
    delete_lip_files = 1 if (plugin_settings["delete_lip_files"]=="true" or plugin_settings["delete_lip_files"]==True) else 0
    delete_wav_files = 1 if (plugin_settings["delete_wav_files"]=="true" or plugin_settings["delete_wav_files"]==True) else 0
    skip_existing = 1 if (plugin_settings["skip_existing"]=="true" or plugin_settings["skip_existing"]==True) else 0
    num_processes = plugin_settings["num_processes"]

    if use_multiprocessing:
        # ================== External file start
        output_paths = data["output_paths"]
        input_sequences = data["inputSequence"]

        txt_contents = []
        for data_i in range(len(output_paths)):
            text = input_sequences[data_i]
            text = text.replace("_", " ")
            text = re.sub(r'[^a-zA-Z\s]+', '', text)
            txt_contents.append(f'{text}|{output_paths[data_i]}')

        root_path = f'.' if isDev else f'./resources/app' # The root directories are different in dev/prod
        if os.path.exists(f'{root_path}/plugins/lip_fuz/input.txt'):
            os.remove(f'{root_path}/plugins/lip_fuz/input.txt')
        with open(f'{root_path}/plugins/lip_fuz/input.txt', "w+", encoding="utf8") as f:
            f.write("\n".join(txt_contents))

        # run_command(f'{root_path}/plugins/lip_fuz/run_lipfuz_gen.exe {root_path}/plugins/lip_fuz/input.txt {num_processes} {delete_lip_files} {delete_wav_files}')
        run_command(f'{root_path}/plugins/lip_fuz/run_lipfuz_gen.exe {num_processes} {game} {delete_lip_files} {delete_wav_files} {make_fuz_files} {skip_existing}')
        # ================== External file end
    else:
        # ================== Simple sequential start
        output_paths = data["output_paths"]
        input_sequences = data["inputSequence"]

        for data_i in range(len(output_paths)):
            run_lip_fuz(input_sequences[data_i], game, output_paths[data_i], delete_lip_files=delete_lip_files, delete_wav_files=delete_wav_files, make_fuz_files=make_fuz_files, skip_existing=skip_existing)
        # ================== Simple sequential end




# ================== Multi-threaded start                   Multi-THREADED doesn't make things faster, but I left this in, as it's a decent example for how to do threads in plugins
# exitFlag = 0
# queueLock = None
# workQueue = None

# def run_lip_fuz_wrapper(wQueue):
#     while True:
#         data = wQueue.get()
#         run_lip_fuz(data[0], data[1])
#         wQueue.task_done()

# def mp_create_lip_fuz_files(data=None):
#     global os, subprocess, logger, isDev, run_command, run_lip_fuz, queue, exitFlag, queueLock, workQueue, threading, run_lip_fuz_wrapper, mp

#     # input_paths = data["input_paths"]
#     output_paths = data["output_paths"]
#     input_sequences = data["inputSequence"]
#     num_threads  = int(data["processes"])
#     num_threads = num_threads if num_threads>0 else max(1, mp.cpu_count()-1)

#     logger.log(f'num_threads: {num_threads}')

#     threads = []
#     queueLock = threading.Lock()
#     workQueue = queue.Queue(32)
#     exitFlag = 0

#     # Create new threads
#     for ti in range(num_threads):
#         # thread = LipFuzThread(input_sequences[ti], output_paths[ti], workQueue)
#         thread = threading.Thread(target=run_lip_fuz_wrapper, args=(workQueue,) )
#         thread.setDaemon(True)
#         thread.start()
#         threads.append(thread)

#     # Fill the queue
#     for data_i in range(len(output_paths)):
#        workQueue.put([input_sequences[data_i], output_paths[data_i]])

#     workQueue.join()
#     logger.log("Done with threads")
# ================== Multi-threaded end

