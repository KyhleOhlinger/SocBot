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
* Click on: Users &rarr; 
* Create an API Key

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

## License / Terms of Use (https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-license-to-a-repository)

MIT License

Copyright (c) 2021 Kyhle Ohlinger

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


Blog Intro:
=====================

Information Security (InfoSec) is generally very red team focused and one of the main reasons is that in the red team space, people tend to share ideas. There is a ton of collaboration, people open source tooling and communities get involved in order to solve a challenge. On the blue team side, most people tend to stick to themselves. Very few Open Source projects are created, and even fewer are actually useful. If you want to have something for security defense, it generally costs a lot of money and you are then tied to a vendor who attempts to sell you more products over the years.

The goal of SocBot is to show that Open Source automation can be used within the blue team space in order to improve an organisations security posture at no cost other than time and hardware requirements. This project makes use of TheHive and a Telegram bot in order to show you that it is possible to automate processes within the Security Operations Center (SOC) within smaller organisations who are not able to afford the most high-end Case Management platforms.

The [Github project](URL) that I created contains a starting point -- an idea -- that can be expanded upon by organsations who are looking to improve their security posture. This blog post will cover the current implementation, ideas to make it useful within an organisation, and how to run the project on your local machine. Information on how to configure the project is detailed within the Github Project.

## Why is this Useful?
Organisations with SOC's or Incident Response (IR) personel will receive alerts throughout the day. There could be several alerts when you are not at your computer and these alerts may be urgent. The main idea behind SocBot is to automate some of the tedious work through the use of Telegram API calls. 

This won't replace the current workflow, but it would make it easier on the employee since they will be able to perform initial checks and determine if it really is serious and they need to jump onto their PC in order to remediate the issue, or if it was just a low fidelity / false alert that can wait until they are back at work. 

## Current Implementation
Due to a ton of other things that have been going on in my life, this project came to a bit of a standstill since the last blogpost and I realised that if I don't release it now, it will just sit and gather dust. Therefore, this is nowhere near what this project could be, but I hope that many of you will take the time to add to the project and improve on the areas that I have not been able to dedicate time to. The current implementation provides an automated Case Management platform which has been integrated with Telegram in order to provide smaller organisations with a starting point which they can use to improve their SOC's capabilities and simultaneously reduce their workload. 

SocBot makes use of the following open source stack:
* ElasticSearch - Part of ELKStack
* Telegram
* TheHive
* Cortex

The basic workflow for this interaction is shown below:

ngrok -> telegram bot
            -> Send requests
                    -> Create case
                        -> Filter by the above, Vt etc
                            

### Current Functionality
This is the culmanation of the Automation Series and as such, the fuctionality is inline with the previous blog post. After installation, you will be able to create a Telegram bot, link it to the service and have access to the following:

* Hash Checker
* IP / Domain Checker
* File Upload - Responds with a hash
    -> Needs a DB? (File as Blob + hash)
* Case Management - TheHive

The current implementation of the Telegram bot is not context aware, rather you can interact with it using the following commands:
* /help
* /vt <hash> / <ip or domain>
* /cuckoo <hash> - create sandbox functionality for files
* /disassemble <hash> - Radare?
* /threatlookup <ip or domain> - hippocamp
* /thehive <Name>

TheHive creates a new case with the provided Indicators of Compromise (IoC). I'm not going to dive into the functionality behind TheHive -- if you are interested in it as case management software, I would recommend looking at their website which contains a ton of information on how it is used: <https://thehive-project.org>.

## Ideas to make it Useful
As described above, this project is currently very bare bones, but it can be expanded upon with relative ease in order to be useful for an organisation. 

### Encryption and Principal of Least Privilege
If you are going to be making use of this within your organisation, I highly recommend that you make use of an encrypted channel rather than the current cleartext channels. For both TheHive and Cortex, this can be accomplished through the use of reverse proxies. Additionally, I would recommend creating users and accounts while keeping the principal of least privilege in mind.

### Separation of Current Functionality
The Telegram Bot currently creates new cases within TheHive and from there a user is able to insert new Indicators of Compromise (IoCs) which will perform reputation checks. It may be useful to include more calls within the Python script to perform individual requests before creating a new case. This way, the analyst would be able to perform basic checks on the file / IP / hash and create a new case if necessary.

### Improving the Telegram Bot
The Telegram Bot's functionality at this point is rudementary. There are a ton of improvements that can (and should) be made if you are planning on using this within you organisation. The code includes the base templates for; new functions, keyboard creation, and user prompts. The first major change that I would suggest is to include various prompts whereby the user is asked for different information when performing case management. TheHive has a lot of functionality and I believe that there is a lot more that you can do with the bot.

### File Upload Functionality
Currently, the implementation does not include file upload and I believe that if a SOC is going to make use of a project like this, file upload functionality would be essential. A possible workflow could follow this process:

Upload file to Telegram Bot
    -> Store in DB (MongoDB, etc) and generate hash

Once this has been implemented, it would be useful to have integration with a Sandbox environment, such as [Cuckoo](https://cuckoosandbox.org/) and a dissassembler such as [Radare](https://rada.re/n/). In this example, the process flow could look as follows:

Upload file to Telegram Bot
    -> Store in DB and generate hash
    -> Disassemble file with Radare (e.g. /radare <hash>)
    -> Call cuckoo with Telegram bot (e.g. /cuckoo <hash>)

### Integration with Internal Tooling
If your organisation has the ability to block hosts or IP addresses from a central location, it would be beneficial to include API calls within the Telegram Bot to be able to either add the file hashes to a Allow/Block list depending on the severity of the information retrieved from SocBot. Depending on the systems in use, API calls could be made to block IP addresses and domains, or even isolate machines if deemed to be a significant enough. The process flow could look as follows:

Retrieve File / Hash -> Send to SocBot
                            -> Check on different Sources
                                -> VirusTotal
                                -> Sandbox
                                -> etc.
                            -> Depending on Severity
                                -> Allow / Block hash
                                -> Allow / Block IP or domain
                                -> Isolate Machine

-> Integration with AV and SIEM?                        
-> Integration with ticketing systems such as Compass / Jira


## Conclusion
If you are looking for open source tooling to improve the efficiency of your SOC, automation is key. This project is a very simple demonstration of the power that is possible if your organisation is willing to put in some time and effort into R&D. I believe that with the number of alerts that a company sees on any given day, processes that make the work less tedious and allow the security team to reduce noise are essential in maintaining a confident and invigorated workforce.

If you have any questions regarding the implementation of the Github project, please feel free to reach out to me!