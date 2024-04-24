### pyxtf
A python library for reading eXtended Triton Format (XTF) files ([revision 42](https://www.ecagroup.com/en/xtf-file-format)]

##### Installation from pypi

```bash
pip3 install pyxtf
```

##### Installation from source
Clone or download the repository and run the following command. This requires setuptools to be installed.

```bash
python3 setup.py install
```

###### Dependencies
The project depends on setuptools and numpy. Matplotlib is used for plotting, but is not required for basic functionality.

##### Usage

```python
import pyxtf

input_file = 'yourfile.xtf'
(file_header, packets) = pyxtf.xtf_read(input_file, verbose=True)
```

The file_header is of type XTFFileHeader, which is a c-structure that starts off every XTF file. The packets object is a dictionary of the packets that follow the file header. The key is of type XTFHeaderType, which is an enumerated class. The value is a list of objects that belong to that type of header type. E.g usage might look as the following.

```python
...
# Retrieve a list of all sonar packets
sonar_packets = packets[pyxtf.XTFHeaderType.sonar]

# Print the first sonar packet (ping)
print(sonar_packets[0])
```

Examples can be found in the [examples directory](https://github.com/oysstu/pyxtf/tree/master/examples) on github.

##### Contribution
 If you find an XTF-file that does not work, either submit a patch or new packet type, or be prepared to send an example XTF-file when submitting the bug-report.


