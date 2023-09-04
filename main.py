import OpenOPC
import xml.etree.ElementTree as ET
from flask import Flask, Response
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    return Response('OK', status=200)

@app.route('/get_xml', methods=['GET'])

def get_xml():

    try:

        host = '192.168.10.252'

        resultado = subprocess.run(["ping", host], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)        
        print(resultado)
        if resultado.returncode == 0:
            print(f"Ping exitoso a {host}:\n{resultado.stdout}")
            opc = OpenOPC.client()

            opc.connect('Bosch.FPA5000OpcServer.1')

            # Create an XML root element
            root = ET.Element("Properties")

            def retrieve_properties_recursive(node):
                try:
                    
                    properties = opc.properties(node)
                    
                    # Conditional variable assignment
                            # Get the values you need from the properties list
                    detector_short_text = node if properties[7][2] in (' ', '') or len(str(properties[7][2])) <= 2 else properties[7][2].replace('CAN int.: ', '')
                    item_value = properties[2][2]

                    # Replace spaces with underscores in detector_short_name
                    detector_short_name = detector_short_text.replace(' ', '_')
                    print(detector_short_name)

                    # Create an XML element for this property
                    property_elem = ET.SubElement(root, detector_short_name)
                    property_elem.text = item_value
                    # Increment the counter
                except Exception as e:
                    print(f'Error while retrieving properties for {node}')
                    # Handle the error here if needed
                    # Optionally, you can add a delay before retrying
                    # import time
                    # time.sleep(1)  # Add a 1-second delay before retrying
                    items = opc.list(node)
                    for sub_item in items:
                        retrieve_properties_recursive(sub_item)

            fatherNode = 'Central de incendios 1-1'
            items = opc.list(fatherNode)

            for item in items:
                nodes = opc.list(fatherNode + '.' + item)
                for n in nodes:
                    newnode = fatherNode + '.' + item + '.' + n if len(str(n)) == 1 else n
                    #print(newnode)
                    
                    retrieve_properties_recursive(newnode)

            # Create an XML string from the root element
            xml_string = ET.tostring(root, encoding='utf-8').decode()

            #print(xml_string)  # Print the XML string


            opc.close()

            return Response(xml_string, content_type='application/xml')
        else:
            print(f"Fallo el ping a {host}:\n{resultado.stderr}")
            xml_content = '<error>panel sin conexion</error>'
            return Response(xml_content, content_type='application/xml', status=200)

    except Exception as e:
        return str(e)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


