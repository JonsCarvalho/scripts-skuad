import os, sys, csv

file_name = None
path = None
cnpjs = None
reports = []


def clear():
    return os.system('cls' if os.name == 'nt' else 'clear') or None


def main():
    global file_name
    global path
    global cnpjs
    global reports

    try:
        with open(path + '\\' + file_name + '.csv', "r") as file:
            read = csv.DictReader(file, delimiter=';')

            if not cnpjs:
                current_cnpj = None
                for column in read:
                    if not current_cnpj:
                        current_cnpj = column['CNPJ_FUNDO']
                        reports.append({
                            'cnpj': column['CNPJ_FUNDO'],
                            'variation_percentage': 0,
                            'cap': 0,
                            'resg_total': 0,
                            'vl_quota_previous': None
                        })
                    else:
                        if current_cnpj != column['CNPJ_FUNDO']:
                            current_cnpj = column['CNPJ_FUNDO']
                            reports.append({
                                'cnpj': column['CNPJ_FUNDO'],
                                'variation_percentage': 0,
                                'cap': 0,
                                'resg_total': 0,
                                'vl_quota_previous': None
                            })
                    for instance in reports:
                        if instance['cnpj'] == column['CNPJ_FUNDO']:
                            if not instance['vl_quota_previous']:
                                instance['vl_quota_previous'] = float(
                                    column['VL_QUOTA'])
                            else:
                                instance['variation_percentage'] = ((float(
                                    column['VL_QUOTA']) - instance['vl_quota_previous']) / instance['vl_quota_previous'])

                                instance['vl_quota_previous'] = float(
                                    column['VL_QUOTA'])
                            instance['resg_total'] += float(column['RESG_DIA'])
                            instance['cap'] += float(column['CAPTC_DIA'])

            else:
                for cnpj in cnpjs:
                    reports.append({
                        'cnpj': cnpj,
                        'variation_percentage': 0,
                        'cap': 0,
                        'resg_total': 0,
                        'vl_quota_previous': None
                    })
                for column in read:
                    for instance in reports:
                        if instance['cnpj'] == column['CNPJ_FUNDO']:
                            if not instance['vl_quota_previous']:
                                instance['vl_quota_previous'] = float(
                                    column['VL_QUOTA'])
                            else:
                                instance['variation_percentage'] = ((float(
                                    column['VL_QUOTA']) - instance['vl_quota_previous']) / instance['vl_quota_previous'])

                                instance['vl_quota_previous'] = float(
                                    column['VL_QUOTA'])
                            instance['resg_total'] += float(column['RESG_DIA'])
                            instance['cap'] += float(column['CAPTC_DIA'])

        for instance in reports:
            print('CNPJ: %s | Variação da Cota: %s%s |  Captação: %s | Resgate Total: %s' % (instance['cnpj'], round(
                instance['variation_percentage'], 4), '%', instance['cap'], instance['resg_total']))

    except:
        print('\n\nOcorreu algo de errado, não foi possível obter os relatórios.')


if __name__ == '__main__':
    if not sys.argv[1:]:
        print('É necessário colocar os parâmetros.')
    else:
        file_name = str(sys.argv[1])
        path = str(sys.argv[2])
        cnpjs = sys.argv[3:]

        main()
