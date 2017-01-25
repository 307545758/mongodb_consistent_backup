import logging

from Tar import Tar
from Zbackup import Zbackup
from mongodb_consistent_backup.Common import config_to_string, parse_submodule


class Archive:
    def __init__(self, config, backup_dir):
        self.config     = config
        self.backup_dir = backup_dir

        self.method    = None
        self._archiver = None
        self.init()

    def init(self):
        archive_method = self.config.archive.method
        if not archive_method or parse_submodule(archive_method) == "none":
            logging.info("Archiving disabled, skipping")
        else:
            self.method = parse_submodule(archive_method)
            logging.info("Using archiving method: %s" % self.method)
            try:
                self._archiver = globals()[self.method.capitalize()](
                    self.config,
                    self.backup_dir
                )
            except LookupError, e:
                raise Exception, 'No archiving method: %s' % self.method, None
            except Exception, e:
                raise e

    def compression(self, method=None):
        if self._archiver:
            return self._archiver.compression(method)

    def threads(self, threads=None):
        if self._archiver:
            return self._archiver.threads(threads)

    def archive(self):
        if self._archiver:
            config_string = config_to_string(self.config.archive[self.method])
            logging.info("Archiving with method: %s (options: %s)" % (self.method, config_string))
            return self._archiver.run()

    def close(self):
        if self._archiver:
            return self._archiver.close()
