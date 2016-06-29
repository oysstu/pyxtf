#### pyxtf
A library for reading and visualizing the eXtended Triton Format (XTF) (revision 40)

Current limitations:
 - Only supports python 3
 - Only read functionality is implemented, not write
 - Limited support for vendor-specific extensions

##### Installation
Clone or download the repository and run the following command. This requires setuptools to be installed.

```bash
python setup.py install
```

###### Dependencies
The project depends on setuptools and numpy. Matplotlib is used for plotting, but is not required for basic functionality.

##### Usage
Some example XTF-files can be downloaded from the [Triton Imaging Inc.](http://www.tritonimaginginc.com/site/content/public/downloads/DemoFiles/DemoFiles.zip) website.

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

##### Scope
There already exists a python2 project called [pyxtf](https://github.com/shamrin/pyxtf), but was more limited in scope than my needs. A better name might've been pyxtf3 to differentiate, but seeing as that project seems abandonded this project will most likely supersede that project in time. A reason for creating a completely new project, is that this project is based on ctypes - while the other pyxtf uses the struct parsing module. The motivation was not performance, but personal preference.


##### Contribution
XTF files are not a golden bullet, there are large differences between file versions and vendors. If you find an XTF-file that does not work, either submit a patch or new packet type, or be prepared to send an example XTF-file when submitting the bug-report.


