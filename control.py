from PyQt5 import uic,QtWidgets
import mysql.connector

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="cadastro_produtos"
)

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
        categoria: "Eletronicos" # type: ignore
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
    segunda_tela.pushButton_2.clicked.connect(voltar_formulario)

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    segunda_tela.tableWidget.setRowCount(len(dados_lidos))
    segunda_tela.tableWidget.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0,5):
            segunda_tela.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
            


app = QtWidgets.QApplication([])
formulario =uic.loadUi("form.ui")
segunda_tela =uic.loadUi("lista.ui")
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(chama_segunda_tela)

formulario.show()
app.exec()

