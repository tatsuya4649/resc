import re

class RescCompileIndentationError(IndentationError):
    pass


class RescCompileTypeError(TypeError):
    pass


class RescCompile:
    def __new__(
        cls,
        source
    ):
        return super().__new__(cls)
    def __init__(
        self,
        source
    ):
        if not isinstance(source, str):
            raise RescCompileTypeError(
                "source must be str type."
            )
        self._source = source

    @staticmethod
    def exndef():
        return re.compile(r"\n(\t| )*def")

    @staticmethod
    def exind():
        return re.compile(r"\n(\t| )*")

    @staticmethod
    def space():
        return re.compile(r"(\t| )*")

    @staticmethod
    def _noneline():
        return ""

    @staticmethod
    def compile(source):
        if not isinstance(source, str):
            raise RescCompileTypeError(
                "source must be str type."
            )
        exnotdef = RescCompile.exnotdef(source)
        exindent = RescCompile.exindent(exnotdef)
        try:
            compile(
                source=exindent,
                filename="<string>",
                mode="exec"
            )
            return exindent + '\n'
        except IndentationError as e:
            raise RescCompileIndentationError(
                e
            )

    @staticmethod
    def exnotdef(source):
        exnotdef = re.search(RescCompile.exndef(), source)
        if exnotdef is None:
            return source
        return source[exnotdef.start():]

    @staticmethod
    def exindent(source):
        result = re.match(
            RescCompile.exind(),
            source
        )
        if result is not None:
            exclude_newline = re.sub(
                r"^\n",
                "",
                result.group()
            )
            onlyspace = re.compile(f"^{exclude_newline}")
        else:
            result = re.match(RescCompile.space(), source)
            if result is None:
                return source
            onlyspace = result.group()
        lines = source.splitlines()
        if RescCompile._noneline() in lines:
            lines.remove(RescCompile._noneline())
        results = list()
        for line in lines:
            result = re.sub(
                onlyspace,
                "",
                line,
            )
            results.append(result)
        return "\n".join(results)

