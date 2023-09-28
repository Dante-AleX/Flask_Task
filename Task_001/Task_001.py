# Создать базовый шаблон для интернет-магазина, содержащий общие элементы дизайна 
# (шапка, меню, подвал), и дочерние шаблоны для страниц категорий товаров и отдельных 
# товаров. Например, создать страницы «Одежда», «Обувь» и «Куртка», используя базовый шаблон.

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/category/<category_name>')
def category(category_name):
    return render_template('category.html', category=category_name)

@app.route('/product/<product_name>')
def product(product_name):
    return render_template('product.html', product=product_name)

if __name__ == '__main__':
    app.run()