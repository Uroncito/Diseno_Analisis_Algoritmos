class Nodo:
    def __init__(self,datos,hijos=None):
        self.datos=datos
        self.hijos=hijos
        self.padre=None
    def set_hijos(self,hijos):
        self.hijos=hijos
        if(self.hijos!=None):
            for hij in self.hijos:
                hij.padre=self
    def get_hijos(self):
        return self.hijos
    def get_padre(self):
        return self.padre
    def set_padre(self,padre):
        self.padre=padre
    def set_datos(self,datos):
        self.datos=datos
    def get_datos(self):
        return self.datos
    def igual(self,nodo):
        if(self.get_datos()==nodo.get_datos()):
            return True
        else:
            return False
    def en_lista(self,lista_nodos):
        esta_en_lista=False
        for n in lista_nodos:
            if self.igual(n):
                esta_en_lista=True
        return esta_en_lista
    def __str__(self):
        return str(self.get_datos())

def busqueda_amplitud(estado_inicial,solucion):
    solucionado=False
    nodos_visitados=[]
    nodos_pendientes=[]
    nodoInicial=Nodo(estado_inicial)
    nodos_pendientes.append(nodoInicial)
    while((not solucionado) and (len(nodos_pendientes)!=0)):
        nodo=nodos_pendientes.pop(0)
        #estraer el nodo y se agrega a visitando
        nodos_visitados.append(nodo)
        if(nodo.get_datos()==solucion):
            solucionado=True
            return nodo
        else:
            dato_nodo=nodo.get_datos()
            #operacion izquierda {x,x,1,4}
            hijo=[dato_nodo[1],dato_nodo[0],dato_nodo[2],dato_nodo[3]]
            hijo_izq=Nodo(hijo)
            if((not hijo_izq.en_lista(nodos_pendientes)) and
               (not hijo_izq.en_lista(nodos_visitados))):
                nodos_pendientes.append(hijo_izq)
            #operacion centro {3,x,x,4}
            hijo=[dato_nodo[0],dato_nodo[2],dato_nodo[1],dato_nodo[3]]
            hijo_centro=Nodo(hijo)
            if((not hijo_centro.en_lista(nodos_pendientes)) and
               (not hijo_centro.en_lista(nodos_visitados))):
                nodos_pendientes.append(hijo_centro)
            #operacion derecho {3,2,x,x}
            hijo=[dato_nodo[0],dato_nodo[1],dato_nodo[3],dato_nodo[2]]
            hijo_der=Nodo(hijo)
            if((not hijo_der.en_lista(nodos_pendientes)) and
               (not hijo_der.en_lista(nodos_visitados))):
                nodos_pendientes.append(hijo_der)
            nodo.set_hijos([hijo_izq,hijo_centro,hijo_der])

if __name__=="__main__":
    estado_inicial=[3,2,1,4]
    solucion=[1,2,3,4]
    nodo_solucion=busqueda_amplitud(estado_inicial,solucion)
    #resultados
    resultado=[]
    nodo=nodo_solucion
    while(nodo.get_padre()!=None):
        resultado.append(nodo.get_datos())
        nodo=nodo.get_padre()
    resultado.append(estado_inicial)
    resultado.reverse()
    print(resultado)
    
            
    