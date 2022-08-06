from waitress import serve
import main

serve(main.app, host='', port=913, _quiet=True)
