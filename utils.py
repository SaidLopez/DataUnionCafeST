import streamlit_authenticator as stauth
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def codify_password(password):
    return stauth.Hasher([password]).generate()


sns.set(style="ticks", context="talk")
plt.style.use("dark_background")
tesco_data = pd.read_csv('tesco_data.csv')
product_data = pd.read_csv('products_data.csv')


def most_consumed_items(product_data=product_data):

    top_products = product_data.groupby('name')[["quantity", "price"]].agg(
        {'quantity': "sum", "price": "median"}).sort_values('quantity', ascending=False)
    fig,  ax = plt.subplots(figsize=(15, 10))
    ax = sns.barplot(
        data=top_products[:20], x=top_products[:20].index, y="quantity", palette='pastel', hue=top_products[:20].index)
    plt.title('Top 20 consumed products')
    plt.xticks(rotation=90)
    plt.xlabel("Product name")
    plt.ylabel("Quantity bought")
    return fig


def most_money_spent(product_data=product_data):
    top_products = product_data.groupby('name')[["quantity", "price"]].agg(
        {'quantity': "sum", "price": "median"}).sort_values('quantity', ascending=False)
    fig,  ax = plt.subplots(figsize=(15, 10))
    top_products["total_spent"] = top_products['quantity'] * \
        top_products['price']
    top_products = top_products.sort_values('total_spent', ascending=False)
    ax = sns.barplot(data=top_products[:20], x=top_products[:20].index,
                     y="total_spent", palette='pastel', hue=top_products[:20].index)
    plt.title('Top 20 total spend on products')
    plt.xticks(rotation=90)
    plt.xlabel("Product name")
    plt.ylabel("£GBP")
    return fig


def basket_price(data=tesco_data):
    data['timeStamp'] = pd.to_datetime(data['timeStamp'], format='ISO8601')
    fig,  ax = plt.subplots(figsize=(15, 10))
    ax = sns.lineplot(data=tesco_data, x='timeStamp',
                      y='basketValueGross')
    plt.title('Top 20 total spend on products')
    # plt.xticks(rotation=90)
    plt.xlabel("Years")
    plt.ylabel("£GBP")
    plt.show()
    return fig


def your_tesco_data(data=tesco_data):
    return tesco_data
