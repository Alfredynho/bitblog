# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "warpp"
  config.vm.hostname = "jvacx"
  config.vm.box_check_update = true

  config.vm.network "private_network", ip: "192.168.33.110"

  config.vm.synced_folder "./", "/code", disabled: false, :nfs => true
  # config.vm.network "public_network", ip: "192.168.1.100"
  # config.vm.network "public_network", ip: "192.168.43.200"



  config.vm.provider "virtualbox" do |vb|
     vb.gui = false
     vb.memory = "1024"
     vb.name = "jvacx"
  end

  config.push.define "atlas" do |push|
    push.app = "jvacx/warpp"
  end

end
