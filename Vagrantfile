# -*- mode: ruby -*-
# vi: set ft=ruby :


Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu/xenial64"
  config.vm.box_check_update = true
  config.vm.hostname = "beamblog"

  config.vm.network "private_network", ip: "192.168.33.111"
  # config.vm.network "public_network", ip: "192.168.0.17", bridge: "en0: Wi-Fi (AirPort)"
  # config.vm.synced_folder "./", "/code", disabled: false, :nfs => true
  config.vm.synced_folder "./", "/code", disabled: false

  config.vm.provider "virtualbox" do |vb|
     vb.gui = false
     vb.memory = "1024"
     vb.name = "beamblog"
  end

end
