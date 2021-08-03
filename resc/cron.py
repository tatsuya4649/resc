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

    def __init__(
        self,
        command,
        interval_str,
        register_file=None,
    ):
        if not isinstance(command, str):
            raise CronTypeError(
                "command must be str type."
            )
        self._command = command
        self._command = self._quote_replace()

        if interval_str is None:
            raise CronValueError("interval_str must be not None.")

        self._interval_str = interval_str
        self._str_to_lists()
        self._totalline = f"{self._interval_str} {self._command}\n"
        self._register_file = register_file

        if not Cron.available():
            raise CronCommandError(
                "not found crontab command. you must have crontab command."
            )
        self._crontab_path = f"command {self._path}"

    @property
    def interval_str(self):
        return self._interval_str

    @property
    def totalline(self):
        return self._totalline

    def _str_to_lists(self):
        self._intervals = list()
        template = self._CRON_RE
        results = re.finditer(template, self._interval_str)
        results = [i for i in results]
        if len(results) != 5:
            raise CronRegularExpressionError("invalid cron string")
        for res in results:
            # */10
            deleteblank = re.match(r"^\S+", res.group())
            if deleteblank is None:
                raise CronRegularExpressionError(
                    "invalid cron string"
                )
            # *
            before_slash = deleteblank.group().split('/')[0]

            index = results.index(res)
            if len(before_slash.split('-')) > 1:
                self._intervals.append({
                    "interval": -1,
                    "scale": CronMode.SCHEDULE,
                    "mode": list(CronScale)[index],
                    "from": before_slash.split('-')[0],
                    "to": before_slash.split('-')[1],
                })
            else:
                self._intervals.append({
                    "interval": int(before_slash)
                    if before_slash != '*' else "*",
                    "scale": CronMode.SCHEDULE,
                    "mode": list(CronScale)[index],
                })

            # 10
            if len(deleteblank.group().split('/')) > 1:
                after_slash = deleteblank.group().split('/')[1]
                self._intervals.append({
                    "interval": int(after_slash),
                    "scale": CronMode.INTERVAL,
                    "mode": list(CronScale)[index],
                })

    def _quote_replace(self):
        return self._command.replace('"', '\\"')

    @property
    def _list(self):
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

    def _register_append(self):
        if self._register_file is not None:
            with open(self._register_file, "a") as rf:
                rf.write(self._totalline)

    def register(self):
        if self._list is None or len(self.list) == 0:
            input = self._totalline
            self._register_append()
        else:
            iter = re.finditer(r'.*\n', self._list)
            cronlists = [x.group() for x in iter]
            # delete duplication
            cronlists = list(set(cronlists))
            if self._totalline not in cronlists:
                self._register_append()
                cronlists.append(self._totalline)
            input = "".join(list(set(cronlists)))
        res = subprocess.run(
            self._crontab_path,
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
            iter = re.finditer(r'.*\n', self._list)
            cronlists = [x.group() for x in iter]
            # delete duplication
            cronlists = list(set(cronlists))
            if self._totalline in cronlists:
                cronlists.remove(self._totalline)
            if len(cronlists) == 0:
                res = subprocess.run(
                    f"{self._crontab_path} -r",
                    shell=True
                )
                return res.returncode
            else:
                input = "".join(list(set(cronlists)))
                res = subprocess.run(
                    self._crontab_path,
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

    @property
    def _path(self):
        result = subprocess.Popen(
            self._CRON_WHICH,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stderr = result.stderr.read()
        if len(stderr) > 0:
            raise CronCommandError(
                "An error occurred in \"command which crontab\"."
            )
        stdout = result.stdout.read()
        if len(stdout) == 0:
            raise CronCommandError("not found crontab command.")

        # "/usr/bin/crontab\n"
        path = stdout.decode()
        delete_empty = re.sub(r'(\n|\s)+$', '', path)

        return delete_empty
