from flask import Flask, render_template, request, redirect
import os


app = Flask(__name__)



def template_list(file_list):
    list = '<ul>'
    for i in range(len(file_list)):
        list = list + f'<li><a href="/?id={file_list[i]}">{file_list[i]}</a></li>'

    list = list + '</ul>'
    return list


def template_html(title, list, body, control):
    return f'''
    <!doctype html>
    <html>
    <head>
    <title>WEB1 - {title}</title>
    <metacharset = "utf-8">
    </head>
    <body>
    <h1><a href = "/" >WEB</a></h1>
    {list}
    <a href = "/create">create</a>
    {control}
    {body}
</body>
</html>
'''


@app.route('/')
def index():
    file_list = os.listdir('./data')
    page_id = request.args.get('id')
    if page_id is None:
        title = 'Welcome'
        description = 'Hello, Flask'
        list = template_list(file_list)
        html = template_html(title, list, f"<h2>{title}</h2><p>{description}</p>", "")
        return html
    elif page_id is not None:
        title = page_id
        file = open('./data/{}'.format(page_id), "r", encoding="cp949")
        description = file.read()
        print(description)
        list = template_list(file_list)
        html = template_html(title, list, f"<h2>{title}</h2><p>{description}</p>", f'''
        <a href="/update?id={title}">update</a>
              <form action="delete_process" method="post">
                <input type="hidden" name="id" value="{title}"/>
                <input type="submit" value="delete"/>
              </form>
              ''')
        file.close()
        return html


@app.route('/create')
def create():
    file_list = os.listdir('./data')
    title = 'Welcome - create'
    list = template_list(file_list)
    html = template_html(title, list, f'''
    <form action="create_process" method="post">
          <p><input type="text" name="title" placeholder="title"/></p>
          <p>
            <textarea name="description" placeholder="description"></textarea>
          </p>
          <p>
            <input type="submit"/>
          </p>
        </form>
    ''', "")

    return html


@app.route('/create_process', methods=['POST'])
def create_process():
    post = request.form
    title = post.getlist('title')[0]
    description = post.getlist('description')[0]
    file = open(f'./data/{title}', 'w', encoding=" cp949")
    file.write(f"{description}")
    file.close()
    return redirect(f"/?id={title}")


@app.route('/update')
def update():
    file_list = os.listdir('./data')
    page_id = request.args.get('id')
    title = page_id
    file = open('./data/{}'.format(page_id), "r", encoding="cp949")
    description = file.read()
    list = template_list(file_list)
    html = template_html(title, list, f'''
    <form action="/update_process" method="post">
          <input type="hidden" name="id" value="{title}"/>
            <p><input type="text" name="title" placeholder="title" value="{title}"/></p>
            <p>
              <textarea name="description" placeholder="description">{description}</textarea>
            </p>
            <p>
              <input type="submit"/>
            </p>
          </form>
    ''', "")
    return html


@app.route('/update_process', methods=['POST'])
def update_process():
    post = request.form
    id = post.getlist('id')[0]
    title = post.getlist('title')[0]
    description = post.getlist('description')[0]
    os.rename(f"./data/{id}", f"./data/{title}")
    file = open(f'./data/{title}', 'w', encoding=" cp949")
    file.write(f"{description}")
    file.close()
    return redirect(f"/?id={title}")


@app.route('/delete_process', methods=['POST'])
def delete_process():
    post = request.form
    id = post.getlist('id')[0]
    os.remove(f'./data/{id}')
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
