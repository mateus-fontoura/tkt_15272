import json
import pyperclip

# Caminho para o arquivo data.json
file_path = r'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\data.json' #Editar aqui para o path do seu json

# Lendo o arquivo JSON
with open(file_path, 'r') as file:
    json_data = json.load(file)

# Processando o JSON para agrupar os tempos de resposta por URI, serverAddr e upstreamCacheStatus
uri_server_cache_times = {}
max_time = 0
max_time_details = {"uri": "", "server": "", "cache_status": ""}

for event in json_data["data"]["httpEvents"]:
    uri = event["requestUri"]
    server = event["serverAddr"]
    cache_status = event["upstreamCacheStatus"]
    time = float(event["requestTime"])

    if uri not in uri_server_cache_times:
        uri_server_cache_times[uri] = {}

    if server not in uri_server_cache_times[uri]:
        uri_server_cache_times[uri][server] = {}

    if cache_status not in uri_server_cache_times[uri][server]:
        uri_server_cache_times[uri][server][cache_status] = []

    uri_server_cache_times[uri][server][cache_status].append(time)

    # Verificando se este é o tempo máximo
    if time > max_time:
        max_time = time
        max_time_details = {"uri": uri, "server": server, "cache_status": cache_status}

# Preparando a string de saída
output_str = ""
for uri, servers in uri_server_cache_times.items():
    output_str += f"URI: {uri}\n"
    for server, cache_statuses in servers.items():
        output_str += f"  Server: {server}\n"
        for cache_status, times in cache_statuses.items():
            formatted_times = ", ".join(map(str, times))
            output_str += f"    Cache Status: {cache_status}\n      Tempos: {formatted_times}\n\n"

# Análise dos maiores tempos
analysis_str = (f"A maior resposta de tempo foi {max_time} segundos, "
                f"ocorrendo na URI '{max_time_details['uri']}', "
                f"no servidor '{max_time_details['server']}', "
                f"com status de cache '{max_time_details['cache_status']}'.\n\n")

# Adicionando a análise ao final da string de saída
output_str += analysis_str

# Copiando para o clipboard
pyperclip.copy(output_str)
print("Os dados foram copiados para o clipboard.")
