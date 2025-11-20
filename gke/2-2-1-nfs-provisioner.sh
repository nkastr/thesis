# This file adds the nfs-provisioner to the cluster
# Required to create iXen application

# Variable definitions 
# nfs_ip is the ip of the machine the nfs files are stored
# nfs_host is the ip of the host to which the export is being shared

nfs_ip=127.0.0.1 # localhost
cluster=gke_thesis-413009_europe-west1-b_thesis
# nfs_host=


# Configure exports file and export
# sudo head -n -1 /etc/exports > temp && sudo mv temp /etc/exports
# sudo echo '/mnt/sharedfolder *(rw,sync,no_subtree_check,insecure)' | sudo tee -a /etc/exports
sudo exportfs -a

# Deploy nfs provisioner on the cluster
helm repo add nfs-subdir-external-provisioner https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner

helm --kube-context $cluster install nfs-subdir-external-provisioner nfs-subdir-external-provisioner/nfs-subdir-external-provisioner \
    --set nfs.server=${nfs_ip} --set nfs.path=/mnt/sharedfolder


