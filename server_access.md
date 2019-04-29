# Server Access Instructions

>### Important!
>With great power, comes great responsibility. __DO NOT__ post usernames, passwords, hostnames, API keys, or other secret information on GitHub. Once it is on the Internet, it is impossible to recall. Sanitize all code, documentation, and issues before committing/posting, and store any necessary secret information in gitignored files to reduce accidental disclosure. *__You have been warned!__*

## SSH
Every modern operating system has an SSH client available in its command line tools.
- __Windows__
  - Launch Command Prompt or PowerShell by seaching in the Start Menu
  - Enter the command `ssh username@host`
    - If `ssh` is 'not recognized...' follow the [steps here](https://www.liquidweb.com/kb/using-ssh-client-windows-10/) to activate the SSH client on Windows 10
  - Accept any certificates and provide your password when prompted
- __macOS__
  - Launch terminal by searching in Spotlight
  - Enter the command `ssh username@host`
  - Accept any certificates and provide your password when prompted
- __Linux__
  - Press `ctrl` + `alt` + `t` to launch terminal
  - Launch terminal by searching in Spotlight
  - Enter the command `ssh username@host`
  - Accept any certificates and provide your password when prompted
- __ChromeOS__
  - Install the [SSH Chrome App](https://chrome.google.com/webstore/detail/secure-shell-app/pnhechapfaindjhompbnflcldabbghjo?hl=en) from the Chrome Web Store and launch the app
  - Enter the command `ssh username@host`
  - Accept any certificates and provide your password when prompted

Using SSH we can access all the usual command-line tools (like Python) in the expected manner.

>### Useful tips
> - Use `ssh -M username@host` to activate multitasking superpowers. We can open the second terminal window and then use `ssh username@host` as usual to piggyback off the existing SSH connection in a second terminal window.
- In this second terminal window use `top -o %MEM` to view the current system resource usage sorted by RAM usage.

## RStudio Server
RStudio Server runs as a web app accessible from the browser. To access this remotely we must setup an SSH tunnel to map the RStudio Server port to a port on our computer.

- Run the command `ssh -L 8787:localhost:8787 username@host`
- Launch your favorite browser and navigate to `http://localhost:8787`
- Login with your server credentials

## Transferring files
The Secure Copy client, included with the SSH client on our computer, allows us to copy files to and from the remote server.

- To copy the file "output.txt" from a path on the remote host to a path on the local host
  - `scp username@host:/remote/path/output.txt /local/path/`
- To copy the file "script.py" from a path on the local host to a path on the remote host
  - `scp /local/path/script.py username@host:/remote/path/`
- To copy a directory, use the `-r` option
  -  `scp -r username@host:/remote/path/ /local/path/`

## PyCharm Remote Debugging
PyCharm will do the hard work for us, if we [set up remote debugging](https://www.jetbrains.com/help/pycharm/remote-debugging-with-product.html) with the server. PyCharm automatically will copy scripts to the remote server and run them when we go to debug, taking care of what we would normally have to do on our own.
