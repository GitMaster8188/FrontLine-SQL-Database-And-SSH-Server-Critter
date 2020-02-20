# FrontLine
<b>FrontLine - SSH and SQL Database Critter</b> is written in a <b>Python Script</b>, with the support of <b>Shell Scripting</b>, capable of brute forcing a specific selected server with a bunch of passphrases and be able to load commands, access directories, data, tables from a databases, schemas and table structures and more..<br/>
![alt text](https://www.imperva.com/learn/wp-content/uploads/sites/13/2018/01/hydra-brute-force-attack.png)<br/>
<b>What is a Brute Force ?</b><br/>
In cryptography, a brute-force attack consists of an attacker submitting many passwords or passphrases with the hope of eventually guessing correctly. The attacker systematically checks all possible passwords and passphrases until the correct one is found.

# SSH Server
![alt text](https://user-images.githubusercontent.com/45601866/74913855-69cb0c00-53fc-11ea-9513-763c70206107.png)

The script can access any <b>SSH Servers</b> once the correct passphrase is found during the loads of brute forcing. When the script finally accessed the SSH Server, the user can now navigate to different directories stored in the server, also can <b>create, read, update, and delete</b> different files and execute some critical commands such as <b>rm or rmdir</b> to delete files or directories, run jobs and processes saved in the server and many more. The user can also upload shell scripts that can quickly and easily manipulate files. 
This is very helpful when an attacker wants to gain some information from a specific company, or even delete their back ups and permanent files the companies is using in a daily basis.<br/>

<b>Below are the special commands that you can run for alternatives.</b><br/>
<ul>
  <li><b>--upload-local-file</b>: type and press the enter key to execute this type of command to start uploading a local file/s from your computer to the <b>SSH Server</b>. Once executed, the script will going to ask for two inputs, <b>Remote File Path</b> (<i>asking the user to enter the specific path in where the uploaded file will be stored</i>), <b>Local File Path</b> (<i>there will be a prompt window for the user to choose a single or multiple files he/she wants to upload to the server</i>). If all things are okay, the script will now going to upload the selected file/s to the <b>SSH Server</b></li>
  <li><b>--download-remote-file</b>: type and press te enter key to execute. This type of command do the vice versa of the above command, it download file/s from the <b>SSH Server</b> and save it to the local directories. There's also two inputs the script will gonna ask, <b>Remote File Path</b> (<i>asking the user to enter the compelete path of the file the user wants to download</i>), <b>Local Path</b> (<i>asking to enter the path or the directory where the downloaded remote file will be stored</i>).</li>
</ul><br/>
<b>Using --upload-local-file</b><br/>

![alt text](https://user-images.githubusercontent.com/45601866/74913166-14dac600-53fb-11ea-91e1-3c1a96f2d80c.png)

<b>Using --download-remote-file</b><br/>
![alt text](https://user-images.githubusercontent.com/45601866/74913162-13110280-53fb-11ea-8dfc-cee3d3507e44.png)

You can check if the file was successfully uploaded by executing <b>ls -lrt</b> command in the FrontLine Terminal, just type <i>cd /some/directory/; ls -lrt</i>...

Also the same thing when checking if you have successfully downloaded the file from the remote server, just browse in the selected directory in where you have enter the directory of the downloaded file.
