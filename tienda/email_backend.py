import threading
import logging
from django.core.mail.backends.smtp import EmailBackend

# Configuramos un logger para ver errores en los logs de despliegue (Render/Heroku)
logger = logging.getLogger(__name__)

class AsyncEmailBackend(EmailBackend):
    """
    Motor de correo asíncrono que envía emails en un hilo separado
    para no bloquear el renderizado de la página, con logging para depuración.
    """
    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        
        # Iniciamos el envío en un hilo separado para que el usuario no espere
        thread = threading.Thread(target=self._send_messages_sync, args=(email_messages,))
        thread.daemon = True
        thread.start()
        
        # Retornamos el número de mensajes que intentamos enviar para que Django no falle
        return len(email_messages)

    def _send_messages_sync(self, email_messages):
        try:
            # Llamamos al método original de forma síncrona dentro del hilo
            sent_count = super().send_messages(email_messages)
            if sent_count:
                print(f"✅ [AsyncEmail] {sent_count} emails enviados exitosamente.")
        except Exception as e:
            # Si falla, lo imprimimos para que aparezca en los logs del servidor
            print(f"❌ [AsyncEmail Error] Fallo al enviar emails: {str(e)}")
            logger.error(f"Error en AsyncEmailBackend: {e}", exc_info=True)
