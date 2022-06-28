from flask import Flask, render_template, request
from selenium import webdriver
import parser

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route('/friends_groups', methods=['GET', 'POST'])
def friends_groups():
    if request.method == 'POST':
        url = request.form.get('url')
        driver = webdriver.Chrome(executable_path="chromedriver/chromedriver.exe")
        friends_groups_list = parser.parsing(driver, url)
        if friends_groups_list:
            fail_str = ""
        else:
            fail_str = "к сожалению, общие группы найти нельзя или их нет"
        return render_template("friends_groups.html", len=len(friends_groups_list),
                               friends_groups_list=friends_groups_list, fail=fail_str)


if __name__ == "__main__":
    app.run(debug=False)
