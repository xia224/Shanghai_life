#!/bin/bash


usage="$(basename "$0") [-h] [-t st] [-s ms] [-p op] -- program to search matched logs from app_center log files 

where:
    -h  show this help text
    -t  date of log files(default: current time)
    -s  matched string(default: Strategy response)
    -p  options for grep(default: -m 1)"

timest=`date +'%Y%m%d'`
matched_str="Strategy response"
options="-m 1"
while getopts ':hs:t:p:' option; do
  case "$option" in
    h) echo "$usage"
       exit
       ;;
    t) timest=$OPTARG
       ;;
    s) matched_str=$OPTARG
       ;;
    p) options=$OPTARG
       ;;
    :) printf "missing argument for -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
   \?) printf "illegal option: -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
  esac
done

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

RED='\033[0;31m'
NC='\033[0m' # No Color

find_logs_func(){
  ssh -p 20220 devops@$ip -i ~/.ssh/devops.xiazhenya.pem << EOF
   cd /data/uap/mix_streaming/log/
   #Search matched logs
   grep $options -r "$matched_str" app_center.exe.log.DEBUG.$timest-*
EOF
}

for ip in "${ip_cana[@]}"
do
  echo -e "Begin to find matched logs from ${RED}$ip${NC}"
   find_logs_func&
  echo "Finish finding matched logs from ${RED}$ip${NC}"
  printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
done
wait
echo "ALL APPCENTER SEARCH DONE"

