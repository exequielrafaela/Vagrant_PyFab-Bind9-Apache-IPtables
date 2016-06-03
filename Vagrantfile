# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.define "fw_nat_dns", primary: true do |fw_nat_dns|
    fw_nat_dns.vm.box = "hashicorp/precise64"
    fw_nat_dns.vm.hostname = "bind9"
    fw_nat_dns.vm.network "public_network", bridge: "wlan0", auto_config: false
    #fw_nat_dns.vm.network "private_network", ip: "10.0.0.1", netmask: "255.255.255.252"
    #fw_nat_dns.vm.network "public_network", bridge: "wlan0"#, auto_config: false
    #fw_nat_dns.vm.network "private_network", ip: "10.0.0.1", netmask: "255.255.255.252"
    fw_nat_dns.vm.provider :virtualbox do |vb|
      vb.memory = 512
      vb.cpus = 1
    end
    fw_nat_dns.vm.provision :shell ,path: "bootstrap_fw_nat_dns.sh"
  end
 
  config.vm.define "router2" do |router2|
    router2.vm.box = "hashicorp/precise64"
    router2.vm.hostname = "router2"
    router2.vm.network "public_network", bridge: "wlan0", auto_config: false
    router2.vm.network "public_network", bridge: "wlan0", auto_config: false
    router2.vm.network "public_network", bridge: "wlan0", auto_config: false
    #router2.vm.network "private_network", ip: "10.0.0.2", auto_config: false
    #router2.vm.network "private_network", ip: "20.0.0.2", auto_config: false
    #router2.vm.network "private_network", ip: "30.0.0.1", auto_config: false
    router2.vm.provider :virtualbox do |vb|
      vb.memory = 512
      vb.cpus = 1
    end
    router2.vm.provision :shell ,path: "bootstrap_router2.sh"
  end
  config.vm.define "router3" do |router3|
    router3.vm.box = "hashicorp/precise64"
    router3.vm.hostname = "router3"  
    router3.vm.network "public_network", bridge: "wlan0", auto_config: false
    router3.vm.network "public_network", bridge: "wlan0", auto_config: false
    #router3.vm.network "private_network", ip: "30.0.0.2", auto_config: false
    #router3.vm.network "private_network", ip: "172.16.0.254", auto_config: false
    router3.vm.provider :virtualbox do |vb|
      vb.memory = 512
      vb.cpus = 1
    end
    router3.vm.provision :shell ,path: "bootstrap_router3.sh"
  end
  config.vm.define "router4" do |router4|
    router4.vm.box = "hashicorp/precise64"
    router4.vm.hostname = "router4"
    router4.vm.network "private_network", ip: "20.0.0.1", auto_config: false
    router4.vm.network "private_network", ip: "192.168.1.254", auto_config: false
    router4.vm.provider :virtualbox do |vb|
      vb.memory = 512
      vb.cpus = 1
    end
    router4.vm.provision :shell ,path: "bootstrap_router4.sh"
  end
  config.vm.define "web" do |web|
    web.vm.box = "hashicorp/precise64"
    web.vm.hostname = "apache"
    web.vm.network "private_network", ip: "172.16.0.1", auto_config: false
    # accessing "localhost:8080" will access port 80 on the guest machine.
    web.vm.network :forwarded_port, guest: 80, host: 8080
    web.vm.provider :virtualbox do |vb|
      vb.memory = 512
      vb.cpus = 1
    end
    web.vm.provision :shell ,path: "bootstrap_web.sh"
  end
  config.vm.define "linux" do |linux|
    linux.vm.box = "hashicorp/precise64"
    linux.vm.hostname = "client"
    linux.vm.network "private_network", ip: "172.16.0.1", auto_config: false
    linux.vm.provider :virtualbox do |vb|
      vb.memory = 512
      vb.cpus = 1
    end
    linux.vm.provision :shell ,path: "bootstrap_client.sh"
  end
end

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network :private_network, ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network :public_network

  # If true, then any SSH connections made will enable agent forwarding.
  # Default value: false
  # config.ssh.forward_agent = true

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

   # The url from where the 'config.vm.box' box will be fetched if it
   # doesn't already exist on the user's system.
   # config.vm.box_url = "http://domain.com/path/to/above.box"