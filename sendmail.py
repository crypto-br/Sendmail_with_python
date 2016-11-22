import smtplib
import os
import mimetypes

from email import encoders
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

def adiciona_anexo(msg, filename):
        if not os.path.isfile(filename):
                return
        ctype, encoding = mimetypes.guess_type(filename)

        if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'

        maintype, subtype = ctype.split('/', 1)

        if maintype == 'text':
                with open(filename) as f:
                        mime = MIMEText(f.read(), _subtype=subtype)
        elif maintype == 'image':
                with open(filename, 'rb') as f:
                        mime = MIMEImage(f.read(), _subtype=subtype)
        elif maintype == 'audio':
                with open(filename, 'rb') as f:
                        mime = MIMEAudio(f.read(), _subtype=subtype)
        else:
                with open(filename, 'rb') as f:
                        mime = MIMEBase(maintype, subtype)
                        mime.set_payload(f.read())

                encoders.encode_base64(mime)

        mime.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(mime)


de = 'seuemail@gmai.com'
para = ['fulano@fulano.com.br']

msg = MIMEMultipart()
msg['From'] = de
msg['To'] = ', '.join(para)
msg['Subject'] = 'BACKUP FIREWALL'


# Corpo da mensagem
msg.attach(MIMEText('YOU MESSAGE', 'html', 'utf-8'))

# Arquivos anexos.
adiciona_anexo(msg, 'log-backup.txt')
#adiciona_anexo(msg, 'imagem.jpg')

raw = msg.as_string()

smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.login('youremail@gmail.com', 'yourpassword')
smtp.sendmail(de, para, raw)
smtp.quit()
