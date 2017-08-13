
<p align="center">
<img src="images/header.jpg" alt="NIT-Trichy SonicWall Login Utility" />  
</p>
<br>

<table>
    <tr> 
        <td width="80%" ><img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat" alt="Contributions Open"/> </td>
        <td width="50%" align="right"><img src="http://forthebadge.com/images/badges/built-with-love.svg" alt="Built with Love" /> </td>
    </tr>
</table>


A command-line utility that logs in a user in the DELL SonicWall infrastructure at NIT-Trichy, to allow access to the Internet. It will maintain a persistent internet connection, and when the time limit of a session is about to expire, it will refresh your session, thus resetting your timer.

### Requires
- Python 2.6+ (or) Python 3.3+
- **requests** python package

### Installation
Make sure that you have the required dependencies before proceeding further. To install the **requests** python package, execute 
```sh
pip install requests
```
Once you have successfully installed the dependencies, you need to get a copy of this repository.  
You can do it in two ways, either *download* the *zip file format* of this github repository, or if you have **git** installed in your system, *clone* this repository into your system.
- If you have downloaded a *zip format* of the repository, extract it to the location of your choice.
- If you are using **git**, here's how to *clone* this repository. In your terminal, execute
```sh
git clone https://github.com/digaru19/NITT-SonicWall-Login.git
```

### Usage

Navigate to the directory where you have *cloned* or *extracted* this repository, and rename the file `credentials.txt.example` to `credentials.txt`. Now, open the file `credentials.txt` in a text editor, and fill in the correct credentials, i.e. your *NITT Roll Number* and *Password*.  
Say, if your *roll number* is `106115096`, and your *password* is `SuperStrongPassword`, your `credentials.txt` file may look something like this, 
```json
{
"USERNAME": "106115096",
"PASSWORD": "SuperStrongPassword"
}
```

Now, open up a terminal, or a command prompt, and navigate to the above directory location, and execute 
```python
python SonicWall_Login.py 
```
If all goes well, you should be logged into the Sonicwall, with a persistent session, and it will be refreshed everytime your session time limit is about to expire.  
You can check your login status by opening `http://192.168.20.1/loginStatusTop(eng).html` in your browser (Do not try to *Update* or *Logout* from this status page).  

#### Demo 
<p align="center">
<img src="images/demo.gif" alt="Usage Demo" />  
</p>
<br>

### Disclaimer
This program is free software. It comes without any warranty, to the extent permitted by applicable law. You shall not use this utility for any illegal purposes. In no event shall the author be liable to any party for direct, indirect, special, incidental, or consequential damages, arising out of the use of this software.

License
----
MIT

