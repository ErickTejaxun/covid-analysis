from fpdf import FPDF, HTMLMixin
from datetime import datetime
import os
 
class PDF(FPDF, HTMLMixin):
    pass


def generarPDF(nombre, titulo, algoritmo):
    now = datetime.now()
    fechahora = now.strftime("%d/%m/%Y %H:%M:%S")
    pdf = PDF()    
    texto_abstract = ("El siguiente reporte tiene como objetivo reportar los resultados del "  + titulo+
                    "Luego de la aplicación del análisis a través de" + algoritmo+
                    "se han obtenido los resultados siguientes"
                    )
    
    contenidoHTML =("<table>"
    '<tr><th width="50%">1. Abstract <p>'+ texto_abstract+' </p></th><th width="50%">2. Resultados</th></tr>'
    "</table>")


    pdf.add_page()
    pdf.write_html(f"""  
    <h1>{titulo}</h1>
    <section>
        <h2 align="center">Erick R. Tejaxún Xicón</h2>        
        <p><a href="https://github.com/ErickTejaxun/covid-analysis">Github repositorio</a></p>
        <!--<p align="right">right aligned text</p>
        
        <font color="#00ff00"><p>hello in green</p></font>
        <font size="7"><p>hello small</p></font>
        <font face="helvetica"><p>hello helvetica</p></font>
        <font face="times"><p>hello times</p></font>-->
    </section>
    <section>
        <table width="100%">
        <thead>
            <tr>
            <th width="50%" ><b>1. Abstract</b></th>
            <th width="50%" ><b>2. Resultados</b></th>
            </tr>
        </thead>
        <tbody>
            <tr>
            <td width="50%" >{texto_abstract}</td>
            <td width="50%" >{texto_abstract}</td>
            </tr>            
        </tbody>
        </table>
    </section>
    """)

    dir = './pdfs/'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    pdf.output(dir+nombre)