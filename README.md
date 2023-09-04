# OPC DA web service for schneider web client

This application is an API that reads all nodes from an OPC DA server until it reaches an item. It then reads and saves the item's tag with its description in an XML file, along with the item's value. Please note that if the item does not have a description, the item's ID is used instead.

## Requirements for Operation

1. Download the DLL file for OPC operation on Windows from [this link](http://gray-box.net/daawrapper.php?lang=en).
2. Paste the downloaded DLL file into the `system32` folder.
3. Open CMD and run the following command to register the service: `regsvr32 gbda_aut.dll`.

By following these steps, the OPC service should operate correctly.

4. You need Python version 2.7.8 to 3.7.0.

5. You will need to install the `pywin32`, `OpenOPC-Python3x` and `flask` packages. You can do this using pip in Python with the following commands:
```python
pip install pywin32
```

```python
pip install OpenOPC-Python3x
```

```python
pip install flask
```

6. The application will return an XML with all the information from the OPC server at the `/get_xml` endpoint.
