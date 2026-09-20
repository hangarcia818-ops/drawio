#!/usr/bin/env python3
"""Topología lógica PNETLab. Python 3.8+, biblioteca estándar, sin Internet.

Uso: python3 generar_topologia.py [--salida diagramas] [--sobrescribir]
No se conecta a equipos ni modifica configuraciones de red.
Edite NODOS y ENLACES para mantener una única fuente de información.
Los datos son el último estado compartido, no una comprobación en vivo.
"""
import argparse
from pathlib import Path
import xml.etree.ElementTree as ET

NODOS = []
ENLACES = []

def nodo(id, texto, x, y, tipo='router', w=300, h=130):
    NODOS.append(dict(id=id, texto=texto, x=x, y=y, tipo=tipo, w=w, h=h))

def enlace(a, b, texto, puntos=()):
    ENLACES.append(dict(a=a, b=b, texto=texto, puntos=puntos))

# Coordenadas compartidas por SVG y draw.io; GraphML conserva atributos.
nodo('bog', 'BOG_R1 | Bogotá\nOSPF ID: 1.1.1.1\nV10: 192.168.6.2/25\nV20: 192.168.4.2/24\nV30: 192.168.0.2/23', 620, 220)
nodo('bkp', 'BACKUP_BOG | Bogotá\nOSPF ID: 2.2.2.2\nV10: 192.168.6.3/25\nV20: 192.168.4.3/24\nV30: 192.168.0.3/23', 1130, 220)
nodo('cali', 'CALI_R2 | Cali\nOSPF ID: 4.4.4.4\nV10: 192.168.7.65/27\nV20: 192.168.5.1/24\nV30: 192.168.2.1/23', 100, 540)
nodo('med', 'MED_R4 | Medellín\nOSPF ID: 3.3.3.3\nV10: 192.168.7.97/28\nV20: 192.168.7.1/26\nV30: 192.168.6.129/25', 1130, 540)
nodo('swbog', 'SW_BOG | Capa 2\nGestión: VLAN 10\nIP de gestión: por confirmar', 620, 540, 'switch')
nodo('swcali', 'SW_CALI | Capa 2\nSVI: 192.168.7.66/27\nGateway: 192.168.7.65', 100, 850, 'switch')
nodo('swmed', 'SW_MED | Capa 2\nSVI: 192.168.7.98/28\nGateway: 192.168.7.97', 1130, 850, 'switch')
nodo('srv', 'Servidor Ubuntu | VLAN 10\nens37: 192.168.6.10/25\nens33: DHCP / NAT VMware\nNagios, Prometheus, Grafana\nNode/SNMP Exporter, GLPI', 620, 850, 'server')
nodo('nat', 'NAT VMware / Internet\nAcceso por ens33\nGateway registrado: 172.16.154.2', 620, 1110, 'cloud')

for id, x, texto in [
    ('vbog', 620, 'BOGOTÁ | VLAN y puertas de enlace\n10 ADMIN: 192.168.6.0/25 | VIP .6.1\n20 SOPORTE: 192.168.4.0/24 | VIP .4.1\n30 VENTAS: 192.168.0.0/23 | VIP .0.1\nDHCP: BOG_R1 | Clientes por validar'),
    ('vcali', 100, 'CALI | VLAN y puertas de enlace\n10 ADMIN: 192.168.7.64/27 | GW .7.65\n20 SOPORTE: 192.168.5.0/24 | GW .5.1\n30 VENTAS: 192.168.2.0/23 | GW .2.1\nDHCP: CALI_R2 | Clientes por validar'),
    ('vmed', 1130, 'MEDELLÍN | VLAN y puertas de enlace\n10 ADMIN: 192.168.7.96/28 | GW .7.97\n20 SOPORTE: 192.168.7.0/26 | GW .7.1\n30 VENTAS: 192.168.6.128/25 | GW .6.129\nDHCP: MED_R4 | Clientes por validar')]:
    nodo(id, texto, x-25, 1370, 'vlan', 350, 150)

enlace('bog', 'bkp', '10.10.10.24/30')
enlace('bog', 'cali', '10.10.10.0/30')
enlace('bog', 'med', '10.10.10.4/30')
enlace('cali', 'med', '10.10.10.8/30 | OSPF área 0', [(250, 420), (1280, 420)])
enlace('bog', 'swbog', 'e0/3 ↔ e0/0 | trunk')
enlace('bkp', 'swbog', 'e0/3 ↔ e0/1 | trunk', [(1540, 285), (1540, 730), (770, 730)])
enlace('cali', 'swcali', 'e0/2 ↔ e0/0 | trunk')
enlace('med', 'swmed', 'e0/2 ↔ e0/0 | trunk')
enlace('swbog', 'srv', 'LAB / ens37 | VLAN 10')
enlace('srv', 'nat', 'ens33 | Internet')
enlace('swbog', 'vbog', 'VLAN 10,20,30', [(540, 605), (540, 1445)])
enlace('swcali', 'vcali', 'VLAN 10,20,30')
enlace('swmed', 'vmed', 'VLAN 10,20,30')

COLORES = dict(router='#dbeafe', switch='#d1fae5', server='#fef3c7', cloud='#e2e8f0', vlan='#ede9fe')
TITULO = 'Laboratorio PNETLab | Bogotá · Cali · Medellín'
NOTAS = [
    'Topología lógica basada en el estado compartido; no representa disponibilidad en tiempo real.',
    'HSRP en Bogotá: principal y respaldo comparten SW_BOG. No hay salida WAN independiente del respaldo.',
    'Monitoreo SNMP/ICMP por la red existente; no se dibujan enlaces físicos adicionales de monitoreo.',
    'Un switch por sede. VLAN 99 eliminada. Troncales 802.1Q: VLAN 10, 20 y 30.',
    'Los bloques VLAN son agrupaciones lógicas, no equipos. GW/VIP abreviadas conservan el prefijo 192.168.',
]

def xml_bytes(root):
    return ET.tostring(root, encoding='utf-8', xml_declaration=True)

def drawio():
    root = ET.Element('mxfile', host='app.diagrams.net')
    diagram = ET.SubElement(root, 'diagram', id='laboratorio', name='Topología lógica')
    model = ET.SubElement(diagram, 'mxGraphModel', page='1', pageWidth='1650', pageHeight='1850')
    cells = ET.SubElement(model, 'root')
    ET.SubElement(cells, 'mxCell', id='0')
    ET.SubElement(cells, 'mxCell', id='1', parent='0')
    for n in NODOS + [dict(id='titulo', texto=TITULO, x=80, y=50, w=1450, h=70, tipo='text'), dict(id='notas', texto='\n'.join(NOTAS), x=80, y=1590, w=1450, h=170, tipo='text')]:
        style = 'rounded=1;whiteSpace=wrap;html=0;fontSize=14;spacing=12;strokeColor=#64748b;fillColor=' + COLORES.get(n['tipo'], '#ffffff') + ';'
        c = ET.SubElement(cells, 'mxCell', id=n['id'], value=n['texto'], style=style, vertex='1', parent='1')
        ET.SubElement(c, 'mxGeometry', {'x':str(n['x']), 'y':str(n['y']), 'width':str(n['w']), 'height':str(n['h']), 'as':'geometry'})
    for i, e in enumerate(ENLACES):
        c = ET.SubElement(cells, 'mxCell', id=f'e{i}', value=e['texto'], source=e['a'], target=e['b'], edge='1', parent='1', style='endArrow=none;html=0;fontSize=13;strokeWidth=2;labelBackgroundColor=#ffffff;')
        g = ET.SubElement(c, 'mxGeometry', {'relative':'1', 'as':'geometry'})
        if e['puntos']:
            arr = ET.SubElement(g, 'Array', {'as':'points'})
            for x,y in e['puntos']:
                ET.SubElement(arr, 'mxPoint', x=str(x), y=str(y))
    return xml_bytes(root)

def graphml():
    ns = 'http://graphml.graphdrawing.org/xmlns'
    root = ET.Element('graphml', xmlns=ns)
    for key in ('label','tipo','x','y','width','height'):
        ET.SubElement(root, 'key', {'id':key, 'for':'all' if key=='label' else 'node', 'attr.name':key, 'attr.type':'string'})
    graph = ET.SubElement(root, 'graph', id='laboratorio', edgedefault='undirected')
    for n in NODOS:
        node = ET.SubElement(graph, 'node', id=n['id'])
        for k,v in dict(label=n['texto'],tipo=n['tipo'],x=n['x'],y=n['y'],width=n['w'],height=n['h']).items():
            ET.SubElement(node, 'data', key=k).text=str(v)
    for i,e in enumerate(ENLACES):
        edge=ET.SubElement(graph,'edge',id=f'e{i}',source=e['a'],target=e['b'])
        ET.SubElement(edge,'data',key='label').text=e['texto']
    return xml_bytes(root)

def svg():
    root=ET.Element('svg',xmlns='http://www.w3.org/2000/svg',viewBox='0 0 1650 1850',width='1650',height='1850')
    ET.SubElement(root,'title').text=TITULO
    ET.SubElement(root,'rect',width='1650',height='1850',fill='white')
    def texto(x,y,lines,size=14):
        t=ET.SubElement(root,'text',x=str(x),y=str(y),fill='#172033', attrib={'text-anchor':'middle','font-family':'Arial, sans-serif','font-size':str(size)})
        for i,line in enumerate(lines):
            ET.SubElement(t,'tspan',x=str(x),dy='0' if i==0 else '22').text=line
    texto(825,90,[TITULO],28)
    index={n['id']:n for n in NODOS}
    def centro(n): return (n['x']+n['w']/2,n['y']+n['h']/2)
    for e in ENLACES:
        pts=[centro(index[e['a']]),*e['puntos'],centro(index[e['b']])]
        ET.SubElement(root,'polyline',points=' '.join(f'{x},{y}' for x,y in pts),fill='none',stroke='#64748b',attrib={'stroke-width':'2'})
        j=(len(pts)-1)//2
        x=(pts[j][0]+pts[j+1][0])/2; y=(pts[j][1]+pts[j+1][1])/2
        t=ET.SubElement(root,'text',x=str(x),y=str(y-8),attrib={'text-anchor':'middle','font-family':'Arial, sans-serif','font-size':'13','paint-order':'stroke','stroke':'white','stroke-width':'5','stroke-linejoin':'round','fill':'#334155'})
        t.text=e['texto']
    for n in NODOS:
        ET.SubElement(root,'rect',x=str(n['x']),y=str(n['y']),width=str(n['w']),height=str(n['h']),rx='12',fill=COLORES[n['tipo']],stroke='#64748b')
        lines=n['texto'].splitlines()
        texto(n['x']+n['w']/2,n['y']+n['h']/2-(len(lines)-1)*11+5,lines)
    texto(825,1610,NOTAS,15)
    return xml_bytes(root)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--salida',default='diagramas',help='Carpeta de salida')
    p.add_argument('--sobrescribir',action='store_true',help='Permitir reemplazar los tres archivos generados')
    args=p.parse_args()
    ids=[n['id'] for n in NODOS]
    assert len(ids)==len(set(ids)), 'Identificadores duplicados'
    assert all(e['a'] in ids and e['b'] in ids for e in ENLACES), 'Enlace con nodo inexistente'
    out=Path(args.salida)
    outputs={out/'laboratorio.drawio':drawio(),out/'laboratorio.svg':svg(),out/'laboratorio.graphml':graphml()}
    if not args.sobrescribir and any(f.exists() for f in outputs):
        p.error('Ya existen diagramas. Use otra carpeta o --sobrescribir (reemplaza las ediciones manuales).')
    out.mkdir(parents=True,exist_ok=True)
    for path,data in outputs.items():
        ET.fromstring(data)
        path.write_bytes(data)
        print('Generado:',path.resolve())

if __name__=='__main__':
    main()
