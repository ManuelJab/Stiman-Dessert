import threading
import logging
from django.core.mail.backends.smtp import EmailBackend

# Logger para depuración en producción (Render/Heroku)
logger = logging.getLogger(__name__)

class AsyncEmailBackend(EmailBackend):
    """
    Motor de correo asíncrono robusto para evitar bloqueos en la interfaz.
    """
    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        
        # Enviamos en un hilo NO-daemon para asegurar que se complete el envío
        # incluso si la respuesta HTTP ya se envió.
        thread = threading.Thread(target=self._send_messages_sync, args=(email_messages,))
        thread.start()
        
        return len(email_messages)

    def _send_messages_sync(self, email_messages):
        try:
            # Aseguramos que la conexión se abra y cierre explícitamente en el hilo
            self.open()
            sent_count = super().send_messages(email_messages)
            self.close()
            
            if sent_count:
                print(f"✅ [AsyncEmail] {sent_count} correos enviados exitosamente.")
        except Exception as e:
            # Imprimir el error para que sea visible en los logs del servidor
            print(f"❌ [AsyncEmail Error] Fallo al enviar emails: {str(e)}")
            logger.error(f"Error en AsyncEmailBackend: {e}", exc_info=True)
