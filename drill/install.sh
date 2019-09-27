echo "Downloading Apache-Drill."
install_path="/usr/local/drill"
sudo rm -rf ${install_path}
sudo mkdir -p ${install_path}
sudo chmod 770 ${install_path}
sudo chown -R jbondurant: ${install_path}
tar_path=${install_path}"/apache-drill.tar.gz"
curl https://www-us.apache.org/dist/drill/drill-1.16.0/apache-drill-1.16.0.tar.gz > ${tar_path}
tar -xzvf ${tar_path} -C ${install_path}
rm -f ${tar_path}
echo "Apache-Drill installed."
