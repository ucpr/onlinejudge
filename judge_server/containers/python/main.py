import filecmp
import glob
import json
import os
import sys
import subprocess
from typing import List
from subprocess import TimeoutExpired
from judge_result import JudgeResult


def run_process(input_):
    p = None
    try:
        p = subprocess.run(
            ["python", "/problem/code.py"],
            input=input_.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=2
        )
    except TimeoutExpired:
        return {
            "isError": True,
            "reason": "TLE",
            "stdout": "",
            "stderr": ""
        }
    
    return {
        "isError": False,
        "reason": "",
        "stdout": p.stdout,
        "stderr": p.stderr
    }


def get_test_filenames():
    return {
        "input_files": glob.glob('/problem/testcases/in/*'),
        "output_files": glob.glob('/problem/testcases/out/*')
    }


def diff():
    filenames = get_test_filenames()
    input_file_paths = filenames["input_files"]
    output_file_paths = filenames["output_files"]

    judge_results: List[JudgeResult] = []

    for i, input_file_path in enumerate(input_file_paths):
        input_: str = ""
        output_: str = ""
        with open(input_file_path) as input_file:
            input_ = input_file.read()
            
        run_result = run_process(input_)
        if run_result["isError"]:
            judge_results.append(
                JudgeResult(
                    status=run_result["reason"],
                    error=run_result["stdout"]
                ).export_dict()
            )
        else:
            with open('./tmp.txt', 'w') as tmp_file:
                tmp_file.write(run_result["stdout"].decode())
            import filecmp
            res = filecmp.cmp('tmp.txt', output_file_paths[i])
            judge_results.append(
                JudgeResult(
                    status="AC" if res else "WA",
                ).export_dict()
            )
        
    return judge_results


def check_status(statuses):
    if "WA" in statuses:
        return "WA"
    elif "TLE" in statuses:
        return "TLE"
    else:
        return "AC"


def main():
    judge_results = diff()

    statuses = [judge_result["status"] for judge_result in judge_results]
    res = {
        "status": check_status(statuses),
        "ac_count": statuses.count("AC"),
        "output": ""
    }

    print(json.dumps(res))


if __name__ == '__main__':
    main()
