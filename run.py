from app import app

context = ('server.crt', 'server.key')
app.run(debug=True, ssl_context=context,threaded=True)