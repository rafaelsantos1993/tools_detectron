'''
A função para renomear aruivos sequencialmente com o mesmo comprimento de string 
Recebe como argumento: img_dir: nome da pasta onde estão aos arquivos; size: tamanho da string (número, e.g 3 = img_001) dos arquivos;
file_name_to_remove: opicional, nome de arquivos que não devem ser renomeados 
'''
import os 
import argparse

#recebe os arguemntos 
parser=argparse.ArgumentParser()
parser.add_argument("image_dir", type = str)
parser.add_argument("name_size", type = int)
parser.add_argument("number_to_start", type = int)
parser.add_argument("file_to_exclude", type=str, nargs="?")
args = parser.parse_args()

#função para renomear
def rename_files(img_dir,size, file_count, *file_name_remove):
    os.chdir(img_dir)    # muda para o diretório onde estão os arquivos 
    files_list=sorted(os.listdir(img_dir))  #recebe a lista com os nomes

    #Remove os itens da lista, caso haja algum 
    if file_name_remove:
        for item in file_name_remove:
            files_list.remove(item)
    
    for item in list(files_list):         #loop sobre toda a lista    
        order=len(str(file_count))
        number_of_zeros=size-order
        old_names=item.split('.')   #divide o arqui em uma lista, em  ['nome', 'extensão']
        os.rename(item,'image_'+number_of_zeros*'0'+str(file_count)+'.'+old_names[-1])    # renomeia o item com a extesão antiga 
        file_count+=1
    return os.listdir(img_dir)              #rentorna os novos nomes 

if __name__ == '__main__':
    image_dir = args.image_dir
    name_size = args.name_size
    number_to_start = args.number_to_start
    if args.file_to_exclude:
        file_to_exclude = args.file_to_exclude
        print(rename_files(image_dir, name_size, number_to_start, file_to_exclude))
    else:
        print(rename_files(image_dir, name_size, number_to_start))
