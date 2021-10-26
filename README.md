# Welcome to SocBot

Welcome to SocBot! The idea for the project came directly from a BSide Cape Town [talk](https://www.youtube.com/watch?v=lR79M3HwOuo&feature=youtu.be) in 2018 by Cailan. I looked for the project he detailed in the talk but it doesn't seem to have made it on to Github. I took the ideas that he described in his talk and decided to try make an open source project similar to what he envisioned. 

Now why would you want to use SocBot in the first place? That's a fair question. In my view, this will be useful for smaller security teams who don't have a proper CSIRT in place, or for teams who are looking to improve their capabilities using Open Source software. Everything is Open Source and I hope that companies that might not have a lot of money to spend on security will still be able to improve their overall security posture based on projects like this. Organisations with Security Operation Centers (SOCs) or Incident Response (IR) teams will receive alerts throughout the day. There could be several alerts which are received when the team is not at their computers and many of these alerts may be urgent. 

The main idea behind SocBot is to automate some of the tedious work through automation. This won't replace the current workflow, but it would make it easier on the employee since they will be able to perform initial checks and determine if it really is serious and they need to jump onto their PC in order to remediate the issue, or if it was just a false positive that can wait until they are back. 

I have written a series of posts on the topic of automation using TheHive and Telegram. If you would like to know my ideas on the workflows and possible future implementations for an organisation, I would recommend reading the final post: <URL>. 

## How does this work?
The basic ideas are listed below:
*  Upload file to server / telegram / slack
*  Automated file lookup / IoC checks
*  Create basic case management structure

Tooling used:
*  Automated Spin up: Using Vagrant + Ansible
*  Telegram bot - <https://github.com/python-telegram-bot/python-telegram-bot>
*  Case management - <https://thehive-project.org>
*  IP / IoC Reputation lookup - <https://github.com/TheHive-Project/Cortex>

### Interacting with the Setup
In order to access the web interfaces, you will need to have another machine with a GUI connected to the internal network adapter. In order to keep this as simple as possible, any VM should work and you merely need to change the adapter settings to be in the same range as the SocBot VMs. Once you have connected your VM to the network, you should be able to view the SocBot VMs and connect to the web applications. If you want an automated Kali machine, I have a Vagrant Kali script on my [Github](https://github.com/KyhleOhlinger/Vagrant_Kali).

# The Initial Setup Requirements
Now that you have an understnding of what the project does, I hope I've convinced at least one person to play around with it. In order to get this up and running, you (as an administrator / person running the project) will need to have access to the Telegram API keys - which are Open Source and free to get a hold of through the use of [BotFather](https://core.telegram.org/bots).

## Structure
The folder is divided into the following components:
* Main Project Folder - This contains the main `Vagrantfile` and associated `Ansible Playbooks`. 
* CaseManagement - This contains the files required to set up the CaseManagement host.
* TelegramBot - This contains the files required to create the Telegram Bot and link it to CaseManagement.

## Initial setup:
In order to run SocBot, you will need to have the following installed on your local machine:
* Vagrant
* Ansible
* VirtualBox
* Telegram

The first time you run the files, it will take quite a while to update and upgrade the hosts - all depending on your internet connection speed. The required Vagrant plugins are provided below and will need to be installed prior to running SocBot:
* `vagrant plugin install vagrant-disksize`
* `vagrant plugin install vagrant-vbguest`
* `vagrant plugin install vagrant-reload`

## Changing the Config Files
Before you run SocBot, you need to generate a Crypto Key using the following command:
```bash
play.crypto.secret="$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 64 | head -n 1)"
```

Once you have the Cyrpto Key, you should add the key to the top of following configuration files within the `CaseManagement` folder:
* cortex_application.conf
* thehive_application.conf

Additionally, if you want to add in any security controls to the configuration files, you should do so at this point. 

## How to Run SocBot
With the prerequisists installed, you can follow the steps below to install SocBot:
1. Download the files to your host.
2. Run `vagrant up` on the vagrant file.

This will then install the `CaseManagement` VM as well as the `SocBot` VM. The `CaseManagemnt` machine will install the following:
* ElasticSearch
* TheHive
* Cortex

The Cortex Configuration Analyzers do take quite a while to set up so don't worry if it appears to be hanging. If you prefer, you can remove the line from the Ansible file and run it manually once the VMs have been provisioned. Additionally, if anything fails during installation, you can make changes to the ansible scripts or VagrantFile and run the following command:
* `vagrant provision`

### Configuring the Case Management Server
Once the prerequisites have been installed, you need to edit the TheHive and Cortex profiles. The web applications will be available on ports 9000 and 9001, respectively. For detailed information about the steps below, you can refer to the Automation Series in my [blog](https://ohlinger.co).

#### TheHive
In order to generate API keys in TheHive, click on: settings &rarr; users:
* Create an API Key

#### Cortex
In order to generate API keys in Cortex:
* Create a new Organisation
* Create a new user and assign the user to the Organisation
* Click on: Users &rarr; Create an API Key

#### Configuring the Services
Both TheHive and Cortex run as services within the `CaseManagement` host. Using the Keys that you have generated, you need to edit the following files:
* /etc/thehive/application.conf - add in the Cortex Key: <KEY>

* Restart both services with the following commands:
    * `sudo service thehive restart`
    * `sudo service cortex restart`

You can now install any analyzers for your organisation by including the free ones or one's that require API keys. Remember to sign into the new user's account within the created Org in order to access the analyzers! If either one is inaccessible at any point, you can log into the CaseMangement host and determine whether the services are running through the use of the following commands, respectively:

* `service thehive status`
* `service cortex status`

If either one is not active, you can try restarting the service using: `sudo service <service> start`.

### Configuring the SocBot Server

Now that the Case Management server is up an running, you need to create a Telegram bot using `BotFather` and generate an API key. Within the `TelegramBot.py` file, edit the following lines:
* `Headers` - Insert the token you generated for thehive
* `Telegram_Key` - Insert the API token for your Telegram bot
* `Endpoint` - Insert the IP address of your Case Management host

If you haven't created a Telegram Bot yet, you should read the following [documentation](https://core.telegram.org/bots) on how to create a bot. Alternatively, you can read my [blog post](https://ohlinger.co/automation-series-part-2/) on creating the Bot used within this project. Everything should now be set up and you can run your first Telegram commands! Navigate to the SocBot host and then run `python3 telegrambot.py`. 

## Using SocBot

All interaction from a normal user's perspective will happen via Telegram. You can view all commands associated with the bot by sending it the following command: `/help`. A breakdown of all commands and usages are listed below for ease of access:
* `/start` - To initialize the bot during installation and for first use for each user.
* `/vt <ip>` - A VirusTotal lookup of an IoC.
* `/th` - Presents the user with the Case Management functionality that is currently available.
* `/help` - A list of commands that are available within SocBot.

The administrator will also be able to directly interact with the hosts which will give them access to TheHive. From here you are able to create as many users as required, each user will have access to the web interface shown below:

**Note:** The commands within Telegram bot are just a proof of concept (PoC) and do not contain a ton of functionality. Within the `/th` command palette, only the `Get` command works at this point and `/vt` is not linked to case management. It will be up to the user to add in additional commands to suit their needs. However, the direct API calls required to interact with TheHive are provided as template functions within the Python code. 

## Recommended Additions:
If you are going to be making use of this within your organisation, I highly recommend that you make use of an encrypted channel rather than the current cleartext channels. For both TheHive and Cortex, this can be accomplished through the use of reverse proxies. Additionally, I would recommend creating users and accounts while keeping the principal of least privilege in mind. My [blog post](https://ohlinger.co/automation-series-part-5) contains more ideas on how this can be improved and used by organisations. 

If you are looking for Open Source tooling to improve the efficiency of your SOC, automation is key. This project is a very simple demonstration of the power that is available, if your organisation is willing to put in some time and effort into Research & Development (R&D). I believe that with the number of alerts that a company sees on any given day, processes that make the work less tedious and allow the security team to reduce noise are essential in maintaining a confident and invigorated workforce.

## MIT License

Copyright (c) 2021 Kyhle Ohlinger

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
