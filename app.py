from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    site_url = None
    if request.method == 'POST':
        site_url = request.form['url']
    return render_template('index.html', site_url=site_url)

if __name__ == '__main__':
    app.run(debug=True)
