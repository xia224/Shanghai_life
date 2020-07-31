#include <iostream>
#include "cpp/src/AccessToken2.h"

using namespace agora::tools;

int main(int argc, char* argv[]) {
  if (argc != 3) {
    std::cout << "You should run like: ./access_token <appid> <app_certificate>"
              << std::endl;
    return -1;
  }
  std::string appid = argv[1];
  std::string app_certificate = "5CFd2fd1755d40ecb72977518be15d3b";
  std::string cname = argv[2];

  uint32_t expire = 600;
  uint32_t ts = static_cast<uint32_t>(time(NULL));
  uint32_t uid = 28823;

  std::cout << "current time stamp: " << ts << std::endl;
  AccessToken2 accessToken(appid, app_certificate, ts, expire);
  accessToken.salt_ = 1;

  std::unique_ptr<Service> service_streaming(new ServiceStreaming(cname, uid));
  service_streaming->AddPrivilege(ServiceStreaming::kPrivilegePublishMixStream, expire);
  accessToken.AddService(std::move(service_streaming));

  std::string token;
  token = accessToken.Build();
  std::cout << "Token: " << token << std::endl;

  return 0;
}
