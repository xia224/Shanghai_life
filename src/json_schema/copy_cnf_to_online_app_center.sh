#!/bin/bash
set -eux
#check configuration legal
python3 app_center_json_schema_verification.py -s app_center_config_schema.json -c new-app-center.json

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

copy_and_update_conf_func(){
  scp -P20220 -i ~/.ssh/devops.xiazhenya.pem new-app-center.json devops@$ip:/tmp

  ssh -p 20220 devops@$ip -i ~/.ssh/devops.xiazhenya.pem << EOF
   cd /etc/uap/mix_streaming_app_center_config/
   #copy config file
   sudo cp app-center.json app-center.json.old
   sudo cp /tmp/new-app-center.json app-center.json
   echo "***Old configuration file md5: "
   md5 app-center.json.old
   echo "***New configuration file md5: "
   md5 app-center.json
   grep -m 1 "DataCenter AppCenter vendor_region" <(tail -n 100 -f /data/uap/mix_streaming/log/app_center.exe.DEBUG) 
EOF
}

for ip in "${ip_try[@]}"
do
  echo -e "Begin to modify app_center configuration of ${RED}$ip${NC}"
  copy_and_update_conf_func &
  echo "Finish to modify app_center configuration of $ip"
  printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
done

wait
echo "ALL APPCENTER UPDATE DONE"

