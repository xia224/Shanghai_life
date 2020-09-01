# -*- coding: utf-8 -*-
__author__ = "xiazhenya@agora.io"
__copyright__ = "Copyright (c) 2020-2025 Agora.io, Inc."

import os
import json
import ipdb
import logging
import time
import subprocess
from flask import Flask, request, jsonify, Response

app = Flask("app_center_tool")
app.logger.setLevel(logging.INFO)
PORT = 54545
HOST = "0.0.0.0"


def exec_query_cmd(files, keywords):
  cmdStr = "grep -10 -r"
  cmdStr += " \"" + keywords + "\""
  cmdStr += " %s"%(files)
  app.logger.info("query cmd: %s" % cmdStr)
  
  popen = subprocess.Popen(cmdStr, shell=True,
          stdout = subprocess.PIPE, stderr=subprocess.STDOUT)
  sout, serr = popen.communicate()
  return popen.returncode, sout, serr


@app.route('/app_center/v1/query_log')
def app_query_log():
  app.logger.info(request.path)
  keywords = request.args.get('query_keyword')
  if keywords == None or keywords == '':
    return "Error: query_keyword must be specified"
  app.logger.info("Query keywords: %s" % keywords)

  files = request.args.get('log_file')
  if files == None or files == '':
    return "Error: log_file must be specified"
  app.logger.info("Query files: %s" % files)

  
  ret = exec_query_cmd(files, keywords)
  if ret[0] != 0:
    app.logger.info("After grep query, get errcode: %d" % ret[0]) 
  return ret[1]

@app.route('/app_center/v1/get_config')
def get_config():
  app.logger.info(request.path)
  #config_file = 'app_center.json'
  config_file = request.args.get('config_file')
  if config_file == None or config_file == '':
    app.logger.info("config_file is not specified")
    return {'Error': 'config_file must be specified'}
  if os.path.isfile(config_file):
    with open(config_file) as configs:
      cnf = json.load(configs)
  else:
    app.logger.error("config file %s not existed"%config_file)
    return "Config file not existed!"

  key = request.args.get('config_key')
  app.logger.info("Query key: %s" % key)

  if (key and cnf.get(key)):
    return json.dumps(cnf[key])

  return cnf

@app.route('/app_center/v1/update_config', methods=['POST'])
def update_config():
  config_file = request.args.get('config_file')
  if config_file == None or config_file == '':
    app.logger.info('config_file is not specified') 
    rt = {'Error': 'config_file must be specified'}
    return Response(json.dumps(rt), mimetype='application/json') 

  with open(config_file, 'r') as infile:
    old_obj = json.load(infile)
  app.logger.info('old json data: %s'%old_obj)

  app.logger.info(request.path)
  #app.logger.info("Post data: %s" % request.stream.read())

  req_data = request.json
  print(req_data)
  #user = request.form['name']
  configs=""
  if req_data.get('strategy'):
    strategy = req_data['strategy']
    app.logger.info('strategy: %s'%strategy)
    old_obj['strategy'] = strategy 
    configs += 'strategy,'
  if req_data.get('vendor_region'):
    vendor_region = req_data['vendor_region']
    app.logger.info('vendor_region: %s'%vendor_region)
    old_obj['vendor_region'] = vendor_region 
    configs += 'vendor_region,'
  if req_data.get('worker_role'):
    role = req_data['worker_role']
    app.logger.info('worker_role: %s'%role)
    old_obj['worker_role'] = role
    configs += 'worker_role,'
  if req_data.get('random_distance'):
    rd = req_data['random_distance']
    app.logger.info('random_distance: %s'%rd)
    old_obj['random_distance'] = rd
    configs += 'random_distance,'
  if req_data.get('converge_key_list'):
    ckl = req_data['converge_key_list']
    app.logger.info('converge_key_list: %s'%ckl)
    old_obj['converge_key_list'] = ckl
    configs += 'converge_key_list,'
  if req_data.get('converge_strategy'):
    cs = req_data['converge_strategy']
    app.logger.info('converge_strategy: %s'%cs)
    old_obj['converge_strategy'] = cs
    configs += 'converge_strategy,'
  if req_data.get('service_name'):
    sn = req_data['service_name']
    app.logger.info('service_name: %s'%sn)
    old_obj['service_name'] = sn
    configs += 'service_name,'
  if req_data.get('env_conf'):
    ec = req_data['env_conf']
    app.logger.info('env_conf: %s'%ec)
    old_obj['env_conf'] = ec
    configs += 'env_conf,'
  if req_data.get('serve_sdk_port'):
    ssp = req_data['serve_sdk_port']
    app.logger.info('serve_sdk_port: %s'%ssp)
    old_obj['serve_sdk_port'] = ssp
    configs += 'serve_sdk_port,'
  if req_data.get('serve_edge_port'):
    sep = req_data['serve_edge_port']
    app.logger.info('serve_edge_port: %s'%sep)
    old_obj['serve_edge_port'] = sep
    configs += 'serve_edge_port,'
  if req_data.get('audio_expire_time'):
    aet = req_data['audio_expire_time']
    app.logger.info('audio_expire_time: %s'%aet)
    old_obj['audio_expire_time'] = aet
    configs += 'audio_expire_time,'
  if req_data.get('video_expire_time'):
    vet = req_data['video_expire_time']
    app.logger.info('video_expire_time: %s'%vet)
    old_obj['video_expire_time'] = vet
    configs += 'video_expire_time,'
  if req_data.get('lbs_key'):
    lbskey = req_data['lbs_key']
    app.logger.info('lbs_key: %s'%lbskey)
    old_obj['lbs_key'] = lbskey
    configs += 'lbs_key,'

  with open(config_file, 'w') as outfile:
    json.dump(old_obj, outfile)
  rt = {'info': 'Get config: ' + configs}
  
  return Response(json.dumps(rt), mimetype='application/json') 


if __name__ == '__main__':
  app.logger.info('Support the below 3 restful api:')
  app.logger.info("1./app_center/v1/query_log <must:log_file> <optional:query_keyword>")
  app.logger.info('2./app_center/v1/get_config <must:config_file> <optional:config_key>')
  app.logger.info('3./app_center/v1/update_config <must:config_file>')
  app.run(host=HOST, port=PORT)
