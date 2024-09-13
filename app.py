# Chatgpt - 100% funcional.

import os
import zipfile

def split_m3u8(file_path, max_size_mb=5):
    max_size_bytes = max_size_mb * 1024 * 1024  # Convertendo MB para bytes
    part_number = 1
    current_size = 0
    current_part_lines = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            current_part_lines.append(line)
            current_size += len(line.encode('utf-8'))  # Calculando o tamanho da linha em bytes
            
            # Se o tamanho atual exceder o limite, salva a parte e reinicia
            if current_size >= max_size_bytes:
                part_file_name = f'parte{part_number}.m3u8'
                with open(part_file_name, 'w', encoding='utf-8') as part_file:
                    part_file.writelines(current_part_lines)
                print(f'Criado: {part_file_name} com tamanho {current_size / (1024 * 1024):.2f} MB')
                
                part_number += 1
                current_size = 0
                current_part_lines = []
    
    # Salva a última parte se houver linhas restantes
    if current_part_lines:
        part_file_name = f'parte{part_number}.m3u8'
        with open(part_file_name, 'w', encoding='utf-8') as part_file:
            part_file.writelines(current_part_lines)
        print(f'Criado: {part_file_name} com tamanho {current_size / (1024 * 1024):.2f} MB')

    # Compacta os arquivos divididos em um arquivo ZIP com máxima compressão
    zip_file_name = 'arquivos_divididos.zip'
    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zip_file:
        for i in range(1, part_number + 1):
            part_file_name = f'parte{i}.m3u8'
            zip_file.write(part_file_name)
            print(f'Adicionado ao ZIP: {part_file_name}')
    
    print(f'Arquivo ZIP criado: {zip_file_name}')

# Exemplo de uso
split_m3u8('arquivo.m3u8')
