import json


class JudgeResult():
    def __init__(self, result: str, error_message: str = None):
        self.result = result
        self.error_message = error_message if error_message is not None else ""

    def export_json(self):
        return json.dumps({
            "result": self.result,
            "error_message": self.error_message
        })


def test():
    res = JudgeResult("AC", "")
    print(res.export_json())


if __name__ == '__main__':
    test()
