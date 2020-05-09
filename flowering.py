import csv
from pprint import pprint
from make_table import encoding_gene, fun_parents_children


flower_names = ['Roses', 'Carnations', 'Cosmos',
'Hyacinths', 'Lilies', 'Mums', 'Pansies', 'Roses',
'Tulips', 'Violets', 'Windflowers',]

def get_flower_genetype(flower):
    if flower.lower() == 'roses':
        file = 'csv/ACNH_ACNL Flower Genes - Roses.csv'
        m = list(csv.reader(open(file)))[1:]
        genetypes_flower= ['']*(4**4)
        for  _,_,_,_,a,b,c,d,color in m:
            idx = int(encoding_gene(a+b+c+d),16)
            genetypes_flower[idx] = color
        return genetypes_flower
    else:
        files = ['csv/ACNH_ACNL Flower Genes - Carnations.csv',
                'csv/ACNH_ACNL Flower Genes - Cosmos.csv',
                'csv/ACNH_ACNL Flower Genes - Hyacinths.csv',
                'csv/ACNH_ACNL Flower Genes - Lilies.csv',
                'csv/ACNH_ACNL Flower Genes - Mums.csv',
                'csv/ACNH_ACNL Flower Genes - Pansies.csv',
                'csv/ACNH_ACNL Flower Genes - Roses.csv',
                'csv/ACNH_ACNL Flower Genes - Tulips.csv',
                'csv/ACNH_ACNL Flower Genes - Violets.csv',
                'csv/ACNH_ACNL Flower Genes - Windflowers.csv',]
        for file in files:
            if flower.lower() in file.lower():
                m = list(csv.reader(open(file)))[1:]
                genetypes_flower = ['-'] * (4**3)
                for _,_,_,_,a,b,c,color in m:
                    idx = int(encoding_gene(a+b+c),16)
                    genetypes_flower[idx] = color
                return genetypes_flower
        raise "no such flower"



def bfs_crossing(flower,gene_num):
    gene_types = get_flower_genetype(flower)
    gene_fun = fun_parents_children(gene_num)

    gene_crossing_methods = {}
    for gene, color in enumerate(gene_types):
        if color != '':
            if 'seed' in color:
                gene_crossing_methods[gene] = [(gene,gene,8,0)]
            else:
                gene_crossing_methods[gene] = []
    gene_count =  len(gene_types)
    duplicate_check = [[False for _ in range(gene_count)] for _ in range(gene_count)]
    exist_gene = [gene for gene in gene_crossing_methods if len(gene_crossing_methods[gene])>0 ]

    for generation in [1,2,3,4]:
        exist_gene = [gene for gene in gene_crossing_methods if len(gene_crossing_methods[gene])>0 ]
        print('generation' ,generation-1 , 'exists',len(exist_gene))
        print('crossing gen', generation)

        for genei in exist_gene:
            for genej in exist_gene:
                # skip half methods
                if genei>genej: continue
                if duplicate_check[genei][genej]:
                    continue
                duplicate_check[genei][genej] = True

                children = gene_fun(genei,genej)
                for gene,p in children:
                    if gene not in [genei, genej]:
                        gene_crossing_methods[gene].append((genei,genej,p,generation))


    return gene_crossing_methods,gene_types
                
def find_parents(target_gene, methods,genes, generation):
    prob =5
    parents = [ v for v in methods[target_gene] if v[3]<generation and  v[2]>=prob ]
    return sorted(parents, key = lambda x:x[2])

def print_parents(prefix, gene, methods, genes, generation=999):
    if generation<=4:return
    parents = find_parents(gene,methods, genes, generation)
    for pa,pb,prob,gen in parents[:20]:
        eprob = 2**(prob-8)
        print(prefix+'-', genes[gene]+"(%d)="%gene, genes[pa]+"(%d)"%pa,genes[pb]+"(%d)"%pb,gen, '%.1f%%'%(eprob*100))
        if "seed" not in genes[pa]:
            print_parents(prefix+"| ", pa,methods,genes, gen)
        if pa!=pb:
            if "seed" not in genes[pb]:
                print_parents(prefix+"| ", pb,methods,genes, gen)



if __name__ == "__main__":
    import pickle
    # methods,genes = bfs_crossing('roses', 4)
    # pickle.dump((methods,genes),open('gen.pkl','wb'))

    methods, genes = pickle.load(open('gen.pkl','rb'))
    # Blue_gene= 252
    Blue_gene= 252
    print('-'*20)
    
    # print_parents('',4, methods,genes,3)
    # print_parents('',Blue_gene, methods,genes)

    parents = [ v for v in methods[Blue_gene] if v[2]==6 ]
    parents.sort(key = lambda x:x[2])
    for pa,pb,prob,gen in parents:
        print("Blue(%d) %.1f%%= "%(Blue_gene, 2**(prob-8)*100),  genes[pa]+"(%d)"%pa,genes[pb]+"(%d)"%pb)
        print_parents('',pa, methods,genes,gen)
        print_parents('',pb, methods,genes,gen)
  