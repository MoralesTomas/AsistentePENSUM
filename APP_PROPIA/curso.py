class curso():
    def __init__(self,codigo,creditos,nombre,pre,obligatorio,apro):
        self.codigo = int(codigo)
        self.creditos = int(creditos)
        self.nombre = nombre
        self.pre = pre
        self.obligatorio = obligatorio
        self.aprobado = apro
        self.cursable = False
        self.analizado = False
        self.cr = 0
        self.llenarPre()

    def llenarPre(self):
        try:
            if self.obligatorio == "si":
                self.obligatorio = True
            elif self.obligatorio == 'no':
                self.obligatorio = False
            if self.aprobado == "si" or self.aprobado is True:
                self.aprobado = True
                self.cursable = False
            elif self.aprobado == 'no':
                self.aprobado = False
        except:
            pass
        

    def revision(self,listado):
        try:
            if self.pre != "SIN CURSOS PRE-REQUISITO":
                validacion = True
                print(f"Los pre son: {self.pre}")
               
                print(len(self.pre),"evaluando curso con codigo",self.codigo)
                for i in self.pre:
                    print("en este caso i es :",i)
                    cursoPre = self.buscarcurso(listado,i)
                    print(f"El curso con codigo {cursoPre.codigo} aprobado = {cursoPre.aprobado}")
                    if cursoPre.aprobado is False:
                        validacion = False
                if validacion:
                    self.cursable = True
                else:
                    self.cursable = False
        except:
            print("Error en la revision del curso con codigo",self.codigo)

    def buscarcurso(self,listado,codigo):
        for i in listado:
            if i.codigo == codigo:
                # retorna el curso en si
                return i

    def pasarALista(self):
        # si desde primera instancia no es una lista lo pasaremos a una lista
        if isinstance(self.pre, list) is False and self.pre != "" and self.pre !="SIN CURSOS PRE-REQUISITO" :
            if self.pre[0] == "[":
                #[11,12] = 11\n12
                self.pre = self.pre.replace("[","")
                self.pre = self.pre.replace("]","")
                self.pre = self.pre.replace(",","\n")
                self.pre = self.pre.split("\n")
                # print(f"=========={self.codigo}=========\n")
                # print({self.pre})
                # print("END")
            else:
                arreglo = self.pre.split("\n")
                self.pre = arreglo
                # print(f"=========={self.codigo}=========\n")
                # print({self.pre})
                # print("END")
            # ahora ya es una lista ahora a volver los valores a enteros.
            arr = []
            for i in self.pre:
                if i.isdigit():
                    arr.append(int(i))
            self.pre = arr
        else:
            # ahora que pasa si ya es una lista pero de tipo str?
            if isinstance(self.pre,list):
                if isinstance(self.pre[0],str):
                    arr = []
                    for i in self.pre:
                        if i.isdigit():
                            arr.append(int(i))
        print("QUEDA PARA",self.codigo,type(self.pre))
        print(self.pre)            