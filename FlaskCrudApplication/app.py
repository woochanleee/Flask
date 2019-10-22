from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    return "Hello Flask Application"


if __name__ == "__main__":
    app.run(debug=True)
# https://www.youtube.com/watch?v=Pu9XhFJduEw&list=PL1FgJUcJJ03vLZXbAFESDqGKBrDNgi-LG&index=1