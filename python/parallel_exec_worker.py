import sys
import subprocess
import threading
import queue
import glob

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

if __name__ == "__main__":
    num_workers = int(sys.argv[1])
    jobs_dir = sys.argv[2]
    runner = MultithreadedProcessRunner(num_workers)
    runner.start()
    files = glob.glob(jobs_dir+'/*', recursive=False)

    for pexec in files:
        print(pexec)
        runner.submit(pexec)

    runner.join()

