import unittest
import os


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover(os.getcwd())

    with open("./report/result.txt", "w", encoding="utf-8") as f:
        runner = unittest.TextTestRunner(stream=f, descriptions=True, verbosity=2)
        runner.run(suite)

