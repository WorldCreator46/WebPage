from waitress import serve
import main

serve(main.app, host='0.0.0.0', port=913, _quiet=True)
