import threading
from django.core.mail.backends.smtp import EmailBackend

class AsyncEmailBackend(EmailBackend):
    """
    Motor de correo asíncrono que envía emails en un hilo separado
    para no bloquear el renderizado de la página.
    """
    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        
        # Iniciamos el envío en un hilo separado
        thread = threading.Thread(target=self._send_messages_sync, args=(email_messages,))
        thread.daemon = True
        thread.start()
        
        # Retornamos el número de mensajes que intentamos enviar
        return len(email_messages)

    def _send_messages_sync(self, email_messages):
        # Llamamos al método original de forma síncrona dentro del hilo
        super().send_messages(email_messages)
