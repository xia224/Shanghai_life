#!/bin/bash
set -eux

ip_list=(
"101.200.232.192"
"47.111.233.232"
"47.114.52.104"
"101.133.175.161"
"47.100.124.10"
"120.24.80.42"
"47.115.148.104"
)

ip_cana=("120.131.12.101"
)

ip_try=("110.43.42.109"
)

RED='\033[0;31m'
NC='\033[0m' # No Color
ip='110.43.42.109'

rollback_configuration_func(){
  echo "abc"
  ssh -p 20220 devops@$ip -i ~/.ssh/devops.xiazhenya.pem << EOF
   cd /etc/uap/mix_streaming_app_center_config/
   #recovery config file
   sudo cp app-center.json app-center.json.err
   sudo cp app-center.json.old app-center.json
   sudo rm -f app-center.json.old
EOF
}

for ip in "${ip_try[@]}"
do
  echo -e "Begin to restore app_center configuration of ${RED}$ip${NC}"
  #timeout is available on linux
  #export -f rollback_configuration_func
  #timeout 20s rollback_configuration_func
  rollback_configuration_func &
  echo "Finish to restore app_center configuration of $ip"
  printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
done
wait
echo "ALL APPCENTER ROLLBACK DONE"

