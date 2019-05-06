import json


class JudgeResult():
    def __init__(
            self,
            status: str,
            error: str = "",
            warning: str = "",
            time: int = 0,
            memory: int = 0):
        self.status = status
        self.time = time
        self.memory = memory
        self.error = error
        self.warning = warning

    def export_json(self):
        return json.dumps({
            "status": self.status,
            "error": self.error,
            "warning": self.warning,
            "time": self.time,
            "memory": self.memory
        })


def test():
    res = JudgeResult("AC", "")
    print(res.export_json())


if __name__ == '__main__':
    test()
