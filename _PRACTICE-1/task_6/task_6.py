import requests

get_ip_response = requests.get('https://icanhazip.com/')
if get_ip_response.status_code == 200:
  ip_address = get_ip_response.text[:-2]
  ip_info_response = requests.get(f'https://ipinfo.io/{ip_address}/geo')
  if ip_info_response.status_code == 200:
    ip_info = ip_info_response.json()

    HTML_TEMPLATE = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8" />
<title></title>
<link rel="stylesheet" href="style.css" />
</head>
<body>
<p>IP address: {ip_info['ip']}</p>
<p>City: {ip_info['city']}</p>
<p>Region: {ip_info['region']}</p>
<p>Country: {ip_info['country']}</p>
<p>Location: {ip_info['loc']}</p>
<p>Internet service provider: {ip_info['org']}</p>
<p>Postal Code: {ip_info['postal']}</p>
<p>Time Zone: {ip_info['timezone']}</p>
</body>
</html>
""" 

    with open('result.html', 'w', encoding='utf-8') as file:
      file.write(HTML_TEMPLATE)

  else:
    print('Ошибка при получении информации о IP Address')

else:
  print('Ошибка при получении собственного IP Address')