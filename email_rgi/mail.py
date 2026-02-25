import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders

CONTA_PADRAO = 'cartoriorgirj@gmail.com'


def envia_email(email_dest, nome_documento, numero_doc, data_hora_tabela, usuario_logado, usuario_digitalizacao):
    status = ''
    message = MIMEMultipart()
    message["To"] = email_dest
    message["From"] = CONTA_PADRAO
    message["Subject"] = f'Divergência de Imagem Digitalizada: {nome_documento}: {numero_doc}'

    body = f'''
    <font size=3>
    <b> Divergência na digitalização de {nome_documento}, com número: {numero_doc} </b>
    </font>
    <br>
    <br>
    Ao setor de TI,<br>
    Segue abaixo todos os dados referentes à divergência na digitalização:
    <br>
    <br>
    <b>Tipo do documento:</b> {nome_documento}<br>
    <b>Número do documento:</b> {numero_doc}<br>
    <b>Digitalizado por:</b> {usuario_digitalizacao}<br>
    <b>Data e hora da digitalização:</b> {data_hora_tabela}<br>
    <br>
    <b>Usuário Conferente:</b> {usuario_logado}
   
    <br>
    <br>
    Favor verificar a divergência e, em seguida, prosseguir com a resolução da questão.'''

    messageText = MIMEText(body,'html')
    message.attach(messageText)

    ###### Desativado pois não iremos enviar anexo inicialmente #####
    # binary_pdf = open(anexo, 'rb')
    # payload = MIMEBase('application', 'octate-stream', Name='dados para pagamento.pdf')
    # payload.set_payload((binary_pdf).read())

    # # enconding the binary into base64
    # encoders.encode_base64(payload)

    # # add header with pdf name
    # payload.add_header('Content-Decomposition', 'attachment', filename='dados para pagamento.pdf')
    # message.attach(payload)

    # pdf = MIMEApplication(open(anexo, 'rb').read())
    # pdf.add_header('Content-Disposition', 'attachment;filename=')
    # message.attach(pdf)

    email = CONTA_PADRAO
    #password incorreto para testes = 'trxnykgianxboom'
    password = 'lrukoabdjvlkmhlw'

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo('Gmail')
    server.starttls()
    try:
        server.login(email,password)
    except Exception as error:
        print(f'Erro ao enviar e-mail: {error}')
        server.quit()
        return error
    else:
        status = 'sucesso'

    fromaddr = CONTA_PADRAO
    toaddrs  = email_dest
    try:
        server.sendmail(fromaddr,toaddrs,message.as_string())
    except Exception as error:
        print(f'Erro ao enviar e-mail: {error}')
        server.quit()
        return error
    else:
        status = 'sucesso'
    
    server.quit()
    return status
if __name__ == "__main__":
    try:
        envia_email(    
        email_dest="cartorio@2rgi-rj.com.br",
        nome_documento="Matrícula",
        numero_doc='145200',
        data_hora_tabela="14/05/2025 09:18",
        usuario_logado='edu',
        usuario_digitalizacao='crd'
        )
    except Exception as err:
        print(err)
    finally:
        print('E-mail funcionando, e enviado com sucesso!')