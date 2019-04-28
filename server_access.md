# Server Access Instructions

> <h3 style="color: red; font-style: italic; font-weight: 700; margin-top: 0;">Important!</h3> With great power, comes great responsibility. **_DO NOT_** post usernames, passwords, hostnames, API keys, or other secret information on GitHub. Once it is on the Internet, it is impossible to recall. Sanitize all code, documentation, and issues before committing/posting, and store any necessary secret information in gitignored files to reduce accidental disclosure. **_You have been warned!_**

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
