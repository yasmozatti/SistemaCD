from PyQt5 import uic,QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="cadastro_produtos"
)

numero_id = 0

def gerar_pdf():
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y=0
    pdf = canvas.Canvas("lista_produtos.pdf")
    pdf.setFont("Times-Bold", 22)
    pdf.drawString(200,800, "Produtos Cadastrados")
    pdf.setFont("Times-Bold", 15)

    pdf.drawString(10,750, "ID")
    pdf.drawString(40,750, "CÓDIGO")
    pdf.drawString(200, 750, "PRODUTO")
    pdf.drawString(410, 750, "PREÇO")
    pdf.drawString(480,750, "CATEGORIA")

    for i in range(0, len(dados_lidos)):
        y = y+ 50
        pdf.drawString(10,750 - y, str(dados_lidos[i][0]))
        pdf.drawString(40,750 - y, str(dados_lidos[i][1]))
        pdf.drawString(100,750 - y, str(dados_lidos[i][2]))
        pdf.drawString(410,750 - y, str(dados_lidos[i][3]))
        pdf.drawString(480,750 - y, str(dados_lidos[i][4]))
    pdf.save()
    print("PDF GERADO COM SUCESSO!")

def funcao_principal():
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()

    codigo = linha1
    descricao = linha2
    preco = linha3

    if formulario.radioButton.isChecked():
        categoria = "Informatica"
    elif formulario.radioButton_2.isChecked():
        categoria = "Alimentos"
    elif formulario.radioButton_3.isChecked():
        categoria = "Eletronicos"
    else:
        categoria = ""
    
    print("Código", linha1)
    print("Descrição", linha2)
    print("Preço", linha3)
    print("Categoria", categoria)

    cursor = banco.cursor()
    comando_SQL = "INSERT INTO produtos (codigo, descricao, preco, categoria) VALUES (%s, %s, %s, %s);"
    dados = (str(linha1), str(linha2), str(linha3), categoria)
    cursor.execute(comando_SQL, dados)
    banco.commit()

    formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")

def voltar_formulario():
    formulario.show()
    segunda_tela.close()

def chama_segunda_tela():
    segunda_tela.show()
    formulario.close()
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    segunda_tela.tableWidget.setRowCount(len(dados_lidos))
    segunda_tela.tableWidget.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0,5):
            segunda_tela.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

def tela_remove_elemento():
    linha = segunda_tela.tableWidget.currentRow()
    segunda_tela.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM produtos WHERE id=" + str(valor_id))

def editar_dados():
    global numero_id
    linha = segunda_tela.tableWidget.currentRow()

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM produtos WHERE id=" + str(valor_id))
    produto = cursor.fetchall()
    tela_editar.show()
    numero_id = valor_id
    tela_editar.lineEdit_10.setText(str(produto[0][0]))
    tela_editar.lineEdit_9.setText(str(produto[0][1]))
    tela_editar.lineEdit_7.setText(str(produto[0][2]))
    tela_editar.lineEdit_8.setText(str(produto[0][3]))
    tela_editar.lineEdit_6.setText(str(produto[0][4]))

def salvar_dados():
    global numero_id
    codigo = tela_editar.lineEdit_9.text()
    descricao = tela_editar.lineEdit_7.text()
    preco = tela_editar.lineEdit_8.text()
    categoria = tela_editar.lineEdit_6.text()
    cursor = banco.cursor()
    cursor.execute("UPDATE produtos SET codigo = '{}', descricao = '{}', preco = '{}', categoria = '{}' WHERE id = []".format(codigo, descricao,preco,categoria, numero_id))
    print("Dados salvos")



def voltar_lista():
    tela_editar.close()
    chama_segunda_tela()




app = QtWidgets.QApplication([])
formulario =uic.loadUi("form.ui")
segunda_tela =uic.loadUi("lista.ui")
tela_editar=uic.loadUi("editar.ui")
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(chama_segunda_tela)
segunda_tela.pushButton_3.clicked.connect(gerar_pdf)
segunda_tela.pushButton_2.clicked.connect(voltar_formulario)
segunda_tela.pushButton_4.clicked.connect(tela_remove_elemento)
segunda_tela.pushButton_5.clicked.connect(editar_dados)
tela_editar.pushButton_2.clicked.connect(voltar_lista)
tela_editar.pushBotton_5.clicked.connect(salvar_dados)

formulario.show()
app.exec()

