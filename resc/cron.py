from enum import Enum
import re
import subprocess


class CronScale(Enum):
    MIN = {"name": "minute", "min": 0, "max": 59}
    HOU = {"name": "hour", "min": 0, "max": 23}
    DAY = {"name": "day", "min": 1, "max": 31}
    MON = {"name": "month", "min": 1, "max": 12}
    WEE = {"name": "week", "min": 0, "max": 6}


class CronMode(Enum):
    INTERVAL = "interval"
    SCHEDULE = "schedule"


class CronTypeError(TypeError):
    pass


class CronAttributeError(AttributeError):
    pass


class CronValueError(ValueError):
    pass


class CronRegularExpressionError(ValueError):
    pass


class CronCommandError(Exception):
    pass


class Cron:
    """
    """
    _CRON_RE = (
        r'(([0-6]?[0-9]-[0-6]?[0-9])'
        r'|((,?[0-6]?[0-9])+)'
        r'|(\*))(/[0-6]?[0-9])?'
    )

    _CRON_WHICH = "command which crontab"

    def __new__(
        cls,
        command,
        interval_str,
    ):
        return super().__new__(
            cls)

    def __init__(
        self,
        command,
        interval_str,
    ):
        if not isinstance(command, str):
            raise CronTypeError(
                "command must be str type."
            )
        self._command = command
        self._command = self._quote_replace()

        if interval_str is None:
            raise CronValueError("interval_str must be not None.")
        if not isinstance(interval_str, str):
            raise CronTypeError("interval_str must be str type.")

        self._interval_str = interval_str
#        self._str_to_lists()
        self._totalline = f"{self._interval_str} {self._command}\n"

        if not Cron.available():
            raise CronCommandError(
                "not found crontab command. you must have crontab command."
            )

    @property
    def interval_str(self):
        return self._interval_str

    @property
    def totalline(self):
        return self._totalline

    def _quote_replace(self):
        return self._command.replace('"', '\\"')

    @staticmethod
    def _listcommand():
        result = subprocess.Popen(
            "command crontab -l",
            encoding="utf-8",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )
        comm = result.communicate()
        errout = comm[1]
        stdout = comm[0]
        if re.match(r'^no crontab', errout) is not None:
            return None
        else:
            return stdout

    @property
    def _list(self):
        return self._listcommand()

    @staticmethod
    def cronlist():
        return Cron._listcommand()

    def register(self):
        if self._list is None or len(self.list) == 0:
            input = self._totalline
        else:
            iter = re.finditer(r'.*\n', self._list)
            cronlists = [x.group() for x in iter]
            # delete duplication
            cronlists = list(set(cronlists))
            if self._totalline not in cronlists:
                cronlists.append(self._totalline)
            input = "".join(list(set(cronlists)))
        res = subprocess.run(
            self._crontab_path(),
            input=input,
            encoding='utf-8',
            shell=True,
        )
        return res.returncode

    @property
    def list(self):
        lists = self._list
        if lists is None:
            return None

        iter = re.finditer(r'.*\n', lists)
        cronlists = [x.group() for x in iter]
        return cronlists

    @property
    def count(self):
        return len(self.list
                   if self.list is not None
                   else list()
                   )

    def delete(self):
        if self._list is None:
            return None
        else:
            iters = re.finditer(r'.*\n', self._list)
            cronlists = [x.group() for x in iters]
            # delete duplication
            cronlists = list(set(cronlists))
            if self._totalline in cronlists:
                cronlists.remove(self._totalline)
            if len(cronlists) == 0:
                res = subprocess.run(
                    f"{self._crontab_path()} -r",
                    shell=True
                )
                return res.returncode
            else:
                input = "".join(list(set(cronlists)))
                res = subprocess.run(
                    self._crontab_path(),
                    input=input,
                    encoding='utf-8',
                    shell=True
                )
                return res.returncode
    
    @staticmethod
    def cronlist():
        if Cron._listcommand() is None:
            return
        else:
            iters = re.finditer(r'.*\n', Cron._listcommand())
            cronlists = [x.group() for x in iters]
            # delete duplication
            cronlists = list(set(cronlists))
            return cronlists

    @staticmethod
    def crondelete(totalline):
        crons = Cron.cronlist()
        if crons is None:
            return
        else:
            if totalline in crons:
                crons.remove(totalline)
            if len(crons) == 0:
                res = subprocess.run(
                    f"{Cron._crontab_path()} -r",
                    shell=True
                )
                return res.returncode
            else:
                input = "".join(list(set(crons)))
                res = subprocess.run(
                    Cron._crontab_path(),
                    input=input,
                    encoding='utf-8',
                    shell=True
                )
                return res.returncode

    @classmethod
    def available(self):
        exists = subprocess.run(
            self._CRON_WHICH,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if exists.returncode == 0:
            return True
        else:
            return False

    @staticmethod
    def _path():
        result = subprocess.Popen(
            Cron._CRON_WHICH,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = result.communicate()
        if len(stderr) > 0:
            raise CronCommandError(
                "An error occurred in \"command which crontab\"."
            )
        if len(stdout) == 0:
            raise CronCommandError("not found crontab command.")

        # "/usr/bin/crontab\n"
        path = stdout.decode()
        delete_empty = re.sub(r'(\n|\s)+$', '', path)

        return delete_empty

    @staticmethod
    def _crontab_path():
        return f"command {Cron._path()}"
