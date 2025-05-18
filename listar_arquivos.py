from pathlib import Path
from datetime import datetime

pastas = list()
entrada = str(input('Digite o caminho da pasta que deseja ler: '))
print("Carregando...")
pasta_alvo = Path(entrada)

if not pasta_alvo.exists() or not pasta_alvo.is_dir():
    print('Caminho invalido ou Pasta inexistente!')
else:
    for arquivo in pasta_alvo.rglob("*"):
        if arquivo.is_file():
            nome = arquivo.name.lower()
            caminho = arquivo.resolve()
            tamanho = (arquivo.stat().st_size / 1024)
            criacao = datetime.fromtimestamp(arquivo.stat().st_ctime).date()

            dados = {
                "nome": nome,
                "caminho": caminho,
                "tamanho": tamanho,
                "criacao": criacao
            }

            pastas.append(dados)

    op = str(input("Deseja filtrar os arquivos? [S/N]: ")).upper().strip()
    while op not in 'SN':
        print('Opção invalida. Tente novamente.')
        op = str(input("Deseja filtrar os arquivos? [S/N]: ")).upper().strip()

    with open('saida.txt', 'w', encoding='utf-8') as f:
        if op == 'S':
            print('''Opções de filtragem:
    [1]Nome;
    [2]Data de criação;
    [3]Tamanho;
    [4]Cancelar;''')
            filtrar = str(input("Filtrar: ")).strip()
            while filtrar not in ['1', '2', '3','4']:
                print('Opção invalida. Tente novamente')
                filtrar = str(input("Filtrar: ")).strip()
            if filtrar == '1':
                fnome = str(input("Digite o nome que deseja filtrar: ")).strip().lower()
                for v in pastas:
                    if fnome in v["nome"]:
                        f.write(f'Nome: {v["nome"]}\n')
                        f.write(f'Caminho: {v["caminho"]}\n')
                        f.write(f'Tamanho: {v["tamanho"]:.2f} KB\n')
                        f.write(f'Data de criação: {v["criacao"].strftime("%d/%m/%Y")}\n')
                        f.write(f'{'=' * 60}\n')
            
            elif filtrar == '2':
                fdata = str(input('Digite a data de criação (dd/mm/aaaa): '))
                try:
                    data_alvo = datetime.strptime(fdata, "%d/%m/%Y").date()
                except ValueError:
                    print("Data invalida, Use o formato dd/mm/aaaa.")
                    exit()
                for v in pastas:
                    if v["criacao"] == data_alvo:
                        f.write(f'Nome: {v["nome"]}\n')
                        f.write(f'Caminho: {v["caminho"]}\n')
                        f.write(f'Tamanho: {v["tamanho"]:.2f} KB\n')
                        f.write(f'Data de criação: {v["criacao"].strftime("%d/%m/%Y")}\n')
                        f.write(f'{'=' * 60}\n')

            elif filtrar == '3':
                try:
                    min_size = int(input('Digite o tamanho minimo em bytes: '))
                    msKB = min_size / 1024
                except ValueError:
                    print("Valor invalido. Digite um valor inteiro.")
                    exit()
                for v in pastas:
                    if v["tamanho"] >= msKB:
                        f.write(f'Nome: {v["nome"]}\n')
                        f.write(f'Caminho: {v["caminho"]}\n')
                        f.write(f'Tamanho: {v["tamanho"]:.2f} KB\n')
                        f.write(f'Data de criação: {v["criacao"].strftime("%d/%m/%Y")}\n')
                        f.write(f'{'=' * 60}\n')

        if op == 'N' or filtrar == '4':
            for v in pastas:
                f.write(f'Nome: {v["nome"]}\n')
                f.write(f'Caminho: {v["caminho"]}\n')
                f.write(f'Tamanho: {v["tamanho"]:.2f} KB\n')
                f.write(f'Data de criação: {v["criacao"].strftime("%d/%m/%Y")}\n')
                f.write(f'{'=' * 60}\n')
