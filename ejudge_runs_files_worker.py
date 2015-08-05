from walker import Walker
import os


class EjudgeRunsFilesWorker(Walker):
    def walk(self, start_dir):
        for dirname, _, filenames in os.walk(os.path.join(start_dir, 'var', 'archive', 'xmlreports')):
            for filename in filenames:
                file_full_name = os.path.join(dirname, filename)
                yield ('gzip' if filename.endswith('.gz') else 'xml', file_full_name)
