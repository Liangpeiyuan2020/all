# -*- codeing=utf-8-*-
# @Time: 2021/8/11 15:54
# @AUthor: BaBa
# @File: demon.py
# @software: PyCharm
import test1
import json
from flask import Flask, jsonify
def accept():
    try:
        import test1
        return jsonify(test1.main())
        print("ttttttttttttttttttt")
    except Exception as e:
        pass
        print("rrrrrrrrrrrrrr")
    return 'OH NO!\n'
if __name__ == "__main__":
    # str=accept();
    print(str)
    import test1,json
    strrr=test1.main()
    print(strrr)
    print(json.dumps(strrr))
    dict1 = {"name": "monkey", "age": 23}
    jsonify(dict1)
