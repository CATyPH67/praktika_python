from flask import Flask, render_template, redirect, url_for, request
from selenium import webdriver
import parser
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route('/friends_groups', methods=['GET', 'POST'])
def friends_groups():
    if request.method == 'POST':
        url = request.form.get('url')
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--no-sandbox")
        # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        driver = webdriver.Chrome(executable_path="chromedriver/chromedriver.exe")
        friends_groups_list = parser.parsing(driver, url)
        if friends_groups_list:
            return render_template("friends_groups.html", len=len(friends_groups_list),
                                   friends_groups_list=friends_groups_list, fail="")
        else:
            return render_template("friends_groups.html", len=0,
                                   friends_groups_list=friends_groups_list,
                                   fail="к сожалению, общие группы найти нельзя или их нет")


if __name__ == "__main__":
    app.run(debug=False)
