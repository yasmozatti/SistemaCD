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
        categoria: "Eletrônicos"
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

app = QtWidgets.QApplication([])
formulario =uic.loadUi("form.ui")
formulario.pushButton.clicked.connect(funcao_principal)

formulario.show()
app.exec()

