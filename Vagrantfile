Vagrant.configure("2") do |config|
    config.vbguest.auto_update = false
    vagrant_root = File.dirname(__FILE__)
    
    # ======================== CASEMANAGEMENT Settings ==========================
    config.vm.define "casemanagement" do |casemanagement|
        casemanagement.vm.box = "ubuntu/focal64"
        casemanagement.vm.network "public_network", bridge: 'wlp2s0'
        casemanagement.vm.network "private_network", ip: "192.168.50.3", virtualbox__intnet: true
        casemanagement.disksize.size = "25GB"
        casemanagement.vm.hostname = "casemanagement"
        
        # Set size and memory for the VM
        casemanagement.vm.provider :virtualbox do |v, override|
            v.name = "CaseManagement"
            v.gui = true
            v.cpus = 2
            v.memory = 4096
            v.customize ["modifyvm", :id, "--vram", 64]
        end
        #casemanagement.vm.provision "shell", reboot: true
        casemanagement.vm.provision "file", source: vagrant_root + "/CaseManagement/", destination: "/home/vagrant/CaseManagement"

        # ======================== CASEMANAGEMENT Provisioning ==========================
        casemanagement.vm.provision  "setup_playbook", type:'ansible' do |ansible|
            ansible.verbose = "vvv"
            ansible.playbook = "setup_playbook.yml"
            ansible.become = true
        end 

        casemanagement.vm.provision :reload

        # Adding Basic Ansible Playbook - Initialisation for CaseManagement
        casemanagement.vm.provision  "casemanagement_playbook", type:'ansible' do |ansible|
            ansible.verbose = "vvv"
            ansible.playbook = "casemanagement_playbook.yml"
            ansible.become = true
        end 
    end

    # ======================== SOCBOT Settings ==========================
    config.vm.define "socbot" do |socbot|
        socbot.vm.box = "ubuntu/focal64"
        socbot.vm.network "public_network", bridge: 'wlp2s0'
        socbot.vm.network "private_network", ip: "192.168.50.2", virtualbox__intnet: true
        socbot.disksize.size = "15GB"
        socbot.vm.hostname = "socbot"
        # Pull Required files onto the VM
        socbot.vm.provision "file", source: vagrant_root + "/TelegramBot/", destination: "/home/vagrant/TelegramBot"
        
        # Set size and memory for the VM
        socbot.vm.provider :virtualbox do |v, override|
            v.name = "SocBot"
            v.gui = true
            v.cpus = 2
            v.memory = 2048
            v.customize ["modifyvm", :id, "--vram", 64]
        end

        socbot.vm.provision :reload

        #======================== SOCBOT Provisioning ==========================
        #Adding Basic Ansible Playbook - Initialisation for SocBot
        socbot.vm.provision  "setup_playbook", type:'ansible' do |ansible|
            ansible.verbose = "vvv"
            ansible.playbook = "setup_playbook.yml"
            ansible.become = true
        end 

        # Adding in Telegram Bot Ansible Playbook
        socbot.vm.provision  "telegram_playbook", type:'ansible' do |ansible|
        ansible.verbose = "vvv"
            ansible.playbook = "telegram_playbook.yml"
            ansible.become = true
        end
        socbot.vm.provision "file", source: vagrant_root + "/tmux.conf", destination:  "~/.tmux.conf"
    end
end