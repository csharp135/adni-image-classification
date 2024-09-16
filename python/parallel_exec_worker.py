import sys
import subprocess
import threading
import queue
import glob
import pandas as pd
import shutil

class MultithreadedProcessRunner:
    def __init__(self, num_workers):
        self.num_workers = num_workers
        self.queue = queue.Queue()
        self.threads = []

    def start(self):
        for _ in range(self.num_workers):
            thread = threading.Thread(target=self.worker)
            self.threads.append(thread)
            thread.start()

    def submit(self, command):
        self.queue.put(command)

    def worker(self):
        while True:
            command = self.queue.get()
            print(self, '::got command', command)
            if command is None:
                self.queue.task_done()
                self.queue.put(None)  # Signal workers to stop
                break
            try:
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
                #for line in process.stdout:
                #    print(line.decode().rstrip())
                process.wait()
            except Exception as e:
                print(f"Error executing command: {command}")
                print(e)

            self.queue.task_done()
        print(self, '::DONE')

    def join(self):
        print('threads', len(self.threads))
        for thread in self.threads:
            self.queue.put(None)  # Signal workers to stop
            for thread in self.threads:
                thread.join()

def load_classifications(kaggle_dataset_csv):
    main_csv_data = pd.read_csv(kaggle_dataset_csv)
    df = pd.DataFrame(main_csv_data)

    return df

if __name__ == "__main__":
    num_workers = int(sys.argv[1])
    mri_dir = sys.argv[2]
    kaggle_dataset_csv = sys.argv[3]
    class_ids = load_classifications(kaggle_dataset_csv)
    to_ignore_images = {
        'I45213', 'I39028', 'I34226', 'I134505', 'I64907', 'I63147',
        'I62943', 'I63111', 'I63897', 'I66310', 'I35911', 'I92669'
    }

    pexec = "fsl_script/fsl_exec.sh "
    runner = MultithreadedProcessRunner(num_workers)
    runner.start()
    print('Searchin for files to load in ', mri_dir)
    files = glob.glob(mri_dir+'/**/*.nii', recursive=True)
    print('Found', len(files)' to process')

    for file in files:
        i = file.find('_I')

        image_id = file[i+1:].replace('.nii', '')
        if image_id in to_ignore_images:
            continue

        dfx = class_ids.query('`Image Data ID` == @image_id')
        group = list(dfx['Group'])[0]

        to_exec = pexec+" " + file + " " + group
        print(to_exec)
        runner.submit(to_exec)

    runner.join()

