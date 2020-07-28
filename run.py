from app import server
from app.config import config_manager as cfg


server_host = cfg.get_server_host()
server_port = cfg.get_server_port()


server.run(threaded=True, host=server_host, port=server_port)
