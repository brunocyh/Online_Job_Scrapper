class Logger:
    def __init__(self):
        pass

    """
    This method pings the server and returns all the online service name.

    Return: ["Seek", "Indeed", ...]
    """
    def log(self):

        if not self._logfile_exist():
            self._create_logfile("c:/whatever/location")

        pass

    def _logfile_exist(self):
        pass

    def _create_logfile(self, file_path):
        pass