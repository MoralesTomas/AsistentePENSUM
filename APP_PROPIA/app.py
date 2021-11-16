from curso import curso
import pickle
import sys
from PyQt5 import uic
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication,QMessageBox,QTableWidgetItem
import sys
cursos = []
creditos = 0

def arreglar():
    global cursos
    for i in cursos:
        esLista = False
        if isinstance(i.pre, list):
            print(f"el curso con codigo = {i.codigo} si tiene una lista")
            esLista = True
        if esLista is False:
            if i.pre != "" and i.pre != "SIN CURSOS PRE-REQUISITO":
                print(f"-----------------------------\n{i.pre}\n------------------------")
                i.pre = i.pre.replace("[","")
                i.pre = i.pre.replace("]","")
                i.pre = i.pre.replace(",","\n")
                arreglo = i.pre.split("\n")
                for a in arreglo:
                    a = int(a.strip())
                i.pre = arreglo
    for i in cursos:
        if isinstance(i.pre, list):
            arreglo = []
            for a in i.pre:
                arreglo.append(int(a))
            i.pre = arreglo

def crear(codigo,creditos,nombre,pre,obligatorio):
    global cursos

    tmp = curso(codigo,creditos,nombre,pre,obligatorio)
    cursos.append(tmp)

def guardar():
    global cursos

    try:
        archivo = open("APP_PROPIA//datos", "wb")
        pickle.dump(cursos, archivo)
        archivo.close()
        print("ARCHIVOS GUARDADOS")
    except:
        print("No se pudo guardar")

def recuperarDatos():
    global cursos
    
    # noObli = [5,39,40,8,9,11,10,368,650,28,122,120,200,652,335,734,656,654,700,966,788,738,288,702,1,968,974]
    aprov = [17,39,69,101,5,19,147,103,107,150,795,114,348,10,112,152,960,118,732,116,770,736]
    try:
        archivo = open("APP_PROPIA//datos", "rb")
        listado = pickle.load(archivo)
        archivo.close()
        cursos = listado
        for i in cursos:
            for a in aprov:
                if i.codigo == a:
                    i.aprobado = True
        # arreglar()
    except:
        print("NO SE PUDO OBTENER DATOS ANTERIORES")
    for i in cursos:
        i.pasarALista()
        
class interfaz(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("APP_PROPIA//vnt.ui", self)

        # QMessageBox.information(self, "Nota:","Esta app no toma en cuenta la cantida de creditos necesarios para cada curso\npor lo que se recomienda revisar el estatus de creditos en el portal de ingenieria")
        self.llenarCombo()
        self.btn_crear.clicked.connect(self.crear)
        self.btn_serializar.clicked.connect(self.guardado)
        self.btn_buscar.clicked.connect(self.busqueda)
        self.btn_busqueda_codigo.clicked.connect(self.bsecu)
        self.btn_editar.clicked.connect(self.editar)
        self.btn_eliminar.clicked.connect(self.eliminar)
        self.btn_actualizar.clicked.connect(self.buscarCursos)
        

    def bsecu(self):
        try:
            global cursos
            tmp = None

            try:
                    codigo = int(self.txt_ingresarCod.text().strip())
            except:
                    QMessageBox.warning(self, "Error","El codigo debe ser un valor numerico")
            for i in cursos:
                if i.codigo == codigo:
                    tmp = i
                    break
            self.txt_codigo.setText(str(tmp.codigo))
            self.txt_creditos.setText(str(tmp.creditos))
            self.txt_nombre.setText(str(tmp.nombre))
            self.txt_cr.setText(str(tmp.cr))
            print(tmp.obligatorio)
            if tmp.obligatorio == "si" or tmp.obligatorio is True:
                tmp.obligatorio = True
                self.txt_obligatorio.setCurrentIndex(0)
            else:
                self.txt_obligatorio.setCurrentIndex(1)
            tmp.llenarPre()
            if tmp.aprobado == "si" or tmp.aprobado is True:
                self.txt_aprobado.setCurrentIndex(1)
                tmp.aprobado = True
            else:
                self.txt_aprobado.setCurrentIndex(0)
            contenido = ""
            arreglo = tmp.pre
            for i in arreglo:
                contenido += str(i)+"\n"
            doc = self.areaPre
            doc.clear()
            if contenido == "":
                doc.appendPlainText("SIN CURSOS PRE-REQUISITO")
            else:
                doc.appendPlainText(str(tmp.pre))
            # codigo,creditos,nombre,pre,obligatorio,apro
        except:
            print("ERROR, al realizar la busqueda")

    def buscarCursos(self):
        # try:
            global cursos,creditos
            creditos = 0
            contenido = ""
            for i in cursos:
                try:
                    if i.aprobado:
                        creditos += i.creditos
                except:
                    print(f"ERROR al evaluar el curso con codigo : {i.codigo}")
            print(creditos)
            self.lb_creditos.setText(f"CREDITOS ACTUALES: {creditos}")

            for i in cursos:
                try:
                    i.revision(cursos)
                    if i.cursable is True and i.aprobado is False and i.obligatorio:
                        contenido += f"{i.codigo},{i.nombre},{i.creditos},{i.obligatorio},{i.cr}\n"
                except:
                    print("error primera")
            for i in cursos:
                try:
                    if i.cursable is True and i.aprobado is False and i.obligatorio is False:
                        contenido += f"{i.codigo},{i.nombre},{i.creditos},{i.obligatorio},{i.cr}\n"
                except:
                    print("error segunda")
            # print("los cursos encontrados son:",contenido)
            #primero limpiarla
            self.areaCursos.clearContents()
            self.areaCursos.setRowCount(0)
            # luego colocar el contenido

            listado = contenido.split("\n")
            for i in range(len(listado)):
                self.areaCursos.insertRow(i)
                sub = listado[i].split(",")
                for a in range(len(sub)):
                    celda = QTableWidgetItem(str(sub[a]))
                    self.areaCursos.setItem(i,a,celda)

            self.areaCursos.resizeColumnsToContents()  



        # except:
        #     print("Error en buscar cursos")

    def mostrarDatos(self):
        global cursos
        for i in cursos:
            try:
                print(f"nombre = {i.nombre} // codigo = {i.codigo} // aprobado = {i.aprobado} // obligatorio = {i.obligatorio} // pre = {i.pre} // tipo = {type(i.pre)}")
            except:
                print("error con el curso de codigo",i.codigo)

    def eliminar(self):
        try:
            # global cursos

            # indice = self.obtenerIndice()
            # if indice is not None:
            #     cursos.pop(indice)
            #     QMessageBox.information(self, "Exito","Curso eliminado con exito!")
            # else:
            #     QMessageBox.warning(self, "Error","No se pudo eliminar este curso.")
            # self.txt_codigo.clear()
            # self.txt_creditos.clear()
            # self.txt_nombre.clear()
            # doc = self.areaPre
            # doc.clear()
            # self.llenarCombo()

            QMessageBox.information(self, "Error","Comunicate con el desarrollador\npara realizar consultas sobre la\neliminacion de cursos.")

        except:
            print("Error en la instruccion eliminar")

    def obtenerIndice(self):
        try:
            global cursos
            contador = 0
            codigo = int(self.txt_codigo.text())
            for i in cursos:
                if i.codigo == codigo:
                    return contador
                contador += 1
            return None
                
        except:
            return None

    def editar(self):

        try:
            codigo = int(self.txt_codigo.text())
            creditos = int(self.txt_creditos.text())
            nombre = self.txt_nombre.text()
            obligatorio = self.txt_obligatorio.currentText().strip()
            aprobado = self.txt_aprobado.currentText().strip()
            pre = self.areaPre.toPlainText()
            tmp = self.buscarIndividual(codigo)
            cr = self.txt_cr.text().strip()
            if tmp != None:
                if obligatorio == 'si':
                    obligatorio = True
                elif obligatorio == 'no':
                    obligatorio = False
                if aprobado == 'si':
                    aprobado = True
                elif aprobado == 'no':
                    aprobado = False
                tmp.codigo = codigo
                tmp.creditos = creditos
                tmp.nombre = nombre
                tmp.obligatorio = obligatorio
                tmp.aprobado = aprobado
                tmp.pre = pre
                if cr != "" and cr.isdigit():
                    tmp.cr = cr
                if pre[0] == "[":
                    tmp.analizado = True
                else:
                    tmp.analizado = False
                QMessageBox.information(self, "Guardado","Se modificaron los datos del curso con exito!")
            else:
                QMessageBox.warning(self, "Error","No se pudieron actualizar los datos")
            self.txt_codigo.clear()
            self.txt_creditos.clear()
            self.txt_nombre.clear()
            doc = self.areaPre
            doc.clear()
            self.llenarCombo()
        except:
            print("Ocurrio un error")
        self.llenarCombo()
        self.mostrarDatos()
    
    def buscarIndividual(self,codigo):
        global cursos
        try:
            codigo = int(codigo)
            for i in cursos:
                if i.codigo == codigo:
                    return i
            return None
        except:
            print("Error al realizar la busqueda individual del codigo",codigo)

    def busqueda(self):
        try:
            global cursos
            tmp = None
            
            codigo = (self.comboBox.currentText())
            codigo = codigo.split("//")
            codigo = int(codigo[0].strip())
            
            for i in cursos:
                if i.codigo == codigo:
                    tmp = i
                    break
            self.txt_codigo.setText(str(tmp.codigo))
            self.txt_creditos.setText(str(tmp.creditos))
            self.txt_nombre.setText(str(tmp.nombre))
            self.txt_cr.setText(str(tmp.cr))
            print(tmp.obligatorio)
            if tmp.obligatorio == "si" or tmp.obligatorio is True:
                tmp.obligatorio = True
                self.txt_obligatorio.setCurrentIndex(0)
            else:
                self.txt_obligatorio.setCurrentIndex(1)
            tmp.llenarPre()
            if tmp.aprobado == "si" or tmp.aprobado is True:
                self.txt_aprobado.setCurrentIndex(1)
                tmp.aprobado = True
            else:
                self.txt_aprobado.setCurrentIndex(0)
            contenido = ""
            arreglo = tmp.pre
            for i in arreglo:
                contenido += str(i)+"\n"
            doc = self.areaPre
            doc.clear()
            if contenido == "":
                doc.appendPlainText("SIN CURSOS PRE-REQUISITO")
            else:
                doc.appendPlainText(str(tmp.pre))
            # codigo,creditos,nombre,pre,obligatorio,apro
        except:
            print("ERROR, al realizar la busqueda")

    def aceptar(self,codigo):
        global cursos
        
        try:
            codigo = int(codigo)
            for i in cursos:
                if i.codigo == codigo:
                    return False
            return True
        except:
            return False

    def mostrar(self):
        global cursos
        print(cursos)

    def guardado(self):
        guardar()
        QMessageBox.information(self, "Guardado","Datos guardados con exito!")

    def llenarCombo(self):
        global cursos
        # vaciar el combo
        self.comboBox.clear()
        self.comboBox.addItem(str("Lista_Cursos"))
        for i in cursos:
            try:
                cadena = f"{i.codigo} // {i.nombre}"
                self.comboBox.addItem(cadena)
            except:
                pass
            

    def crear(self):
        global cursos
        # codigo,creditos,nombre,pre,obligatorio
        # 
        try:
            codigo = int(self.txt_codigo.text().strip())
            creditos = int(self.txt_creditos.text().strip())
            nombre = self.txt_nombre.text()
            obligatorio = self.txt_obligatorio.currentText()
            aprobado = self.txt_aprobado.currentText()
            pre = self.areaPre.toPlainText()
            tmp = curso(codigo,creditos,nombre,pre,obligatorio,aprobado)
            if self.aceptar(codigo):
                cursos.append(tmp)
                guardar()
                print("Se guardo el curso")
                self.txt_codigo.clear()
                self.txt_creditos.clear()
                self.txt_nombre.clear()
                doc = self.areaPre
                doc.clear()
                self.llenarCombo()
                QMessageBox.information(self, "Guardado","Curso guardado con exito!")
            else:
                QMessageBox.warning(self, "Error","No se pudo guardar este curso pues ya existe un curso con este codigo.")
        except:
            print("OCURRIO UN ERROR")
            QMessageBox.warning(self, "Error","Error, no se pudo registrar el curso")

if __name__ == '__main__':
    recuperarDatos()
    app = QApplication(sys.argv)
    GUI = interfaz()
    GUI.show()
    sys.exit(app.exec_())