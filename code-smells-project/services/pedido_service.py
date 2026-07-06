import logging

logger = logging.getLogger(__name__)

def notificar_pedido_criado(pedido_id, usuario_id):
    logger.info("Pedido %s criado para usuario %s", pedido_id, usuario_id)

def notificar_status_alterado(pedido_id, novo_status):
    logger.info("Pedido %s status alterado para %s", pedido_id, novo_status)
