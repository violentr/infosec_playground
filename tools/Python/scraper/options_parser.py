import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-H", "--headers", help="send request headers '{\"Cookie\": \"CookieValue\"'}", dest="headers")
parser.add_argument("-U", "--url", help="syply url to scrap", dest="url")
args = parser.parse_args()
