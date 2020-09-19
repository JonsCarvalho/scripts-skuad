import os, sys, requests

CSV_FILES_URL = 'http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_'
path = None
file_name = None


def clear():
    return os.system('cls' if os.name == 'nt' else 'clear') or None

def request_params():
    global path
    global file_name
    
    print('Precisamos do caminho de destino do arquivo:\n\n')
    path = input()
    clear()
        
    while not path:
        print('O formato informado está errado.\n')
        print('Caminho de destino do arquivo:\n\n')
        
        path = input()
        clear()
        continue
        
    
    print('Agora insira o ano seguido pelo mês específico, no formato YYYYMM:\n\n')
    file_name = input()
    clear()
    
    while len(file_name) != 6:
        print('O formato informado está errado.\n')
        print('Insira o ano seguido pelo mês específico, no formato YYYYMM:\n\n')
        
        file_name = input()
        clear()
        continue
    
    main()

def main():
    global path
    global file_name

    url = CSV_FILES_URL + file_name + '.csv'

    try:
        with open(path +'\\' + file_name + '.csv', "wb") as file:
            print ('\n\nDownloading ' +'inf_diario_fi_'+ file_name + '.csv')
        
            response = requests.get(url, stream=True)
            
            length = response.headers.get('content-length')
            
            if length is None:
                file.write(response.content)
            else:
                progress = 0
                total_length = int(length)
                for data in response.iter_content(chunk_size=4096):
                    progress += len(data)
                    file.write(data)
                    done = int(50 * progress / total_length)
                    sys.stdout.write(
                        '\r[%s%s]'
                        % 
                        ('#' * done, ' ' * (50-done))
                    )
                    sys.stdout.write(' %.2f' % ((progress/total_length)* 100))
                    sys.stdout.write('%')
                    sys.stdout.flush()
        
        print('\n\nO download do arquivo terminou.')
    except:
        print('\n\nOcorreu algo de errado, o download do arquivo não obteve sucesso.')
    
            
if __name__ == '__main__':
    if not sys.argv[1:]:
        request_params()
    else:
        path = str(sys.argv[1])
        file_name = str(sys.argv[2])
        
        main()



