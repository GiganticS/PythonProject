#importing python package
from website import create_app

app = create_app()

#starting web server, everytime when we will edit code it will reload website
if __name__=='__main__':
    app.run(debug=True)