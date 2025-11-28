#include <stdio.h>
#include <stdlib.h>

FILE *arq;


struct livraria {
    char livro[50];
    char autor[50];
    float preco;
    int quantidade;
};



int main() {

    struct livraria produto;
    int opcao;

    do {
        printf("\n--- MENU ---\n");
        printf("1 - Inserir informacoes\n");
        printf("2 - Listar livros\n");
        printf("3 - Pesquisar livro\n");
        printf("4 - Pesquisar autor\n");
        printf("5 - Pesquisar pela faixa do preco\n");
        printf("6 - Alterar quantidade\n");
        printf("7 - Alterar o preco do livro\n");
        printf("8 - Alterar todas as informacoes\n");
        printf("9 - Excluir registro\n");
        printf("10 - Sair\n");
        printf("Escolha uma opcao: ");
        scanf("%d", &opcao);
        getchar();

        switch (opcao) {
            case 1: informacoes(&produto); break;
            case 2: ImprimirDados(&produto); break;
            case 3: pesquisa_livro(&produto); break;
            case 4: pesquisa_autor(&produto); break;
            case 5: pesquisa_preco(&produto);break;
            case 6: altera_quantidade(&produto);break;
            case 7: altera_preco(&produto);break;
            case 8: altera_dados(&produto);break;
            case 9: exclui(&produto);break;
            case 10:printf("Saindo do programa.\n");break;
            default: printf("Opcao invalida. Tente novamente.\n");
        }
    } while (opcao != 10);
    return 0;
}


void informacoes(struct livraria *p){

int rep;

do{
    printf("Fale o nome do livro: ");
    scanf(" %50[^\n]", p->livro);
    printf("Fale o nome do autor: ");
    scanf(" %50[^\n]", p->autor);
    printf("Fale o preco: ");
    scanf("%f", &p->preco);
    printf("Fale a quantidade: ");
    scanf("%d", &p->quantidade);

     rep = repetido(p->livro);

    if (rep == 1){
        printf("repetido");
        printf("\ndigite novamente.\n");
    }
    if (rep== 0)
        printf("registrado");

    }while(rep == 1);
    arq = fopen("arq", "ab");

    fwrite(p, sizeof(*p),1, arq);

    fclose(arq);
}

void ImprimirDados(struct livraria *p){

arq = fopen("arq", "rb");

while(fread(p,sizeof(*p),1,arq) > 0){
    if(p->livro[0] != '*'){
        printf("\nLivro: %s\n", p->livro);
        printf("Autor: %s\n", p->autor);
        printf("Preco: %.2f\n", p->preco);
        printf("Quantidade: %d\n", p->quantidade);
                         }
}
fclose(arq);
}

int pesquisa_livro(struct livraria *p){

    arq = fopen("arq", "rb");
    int posicao = 0;

    char leitura;
    char pesquisa[50];

    printf("\ndigite o nome completo do livro que deseja pesquisar: ");
    scanf(" %50[^\n]", pesquisa);

    while(fread(p, sizeof(*p), 1, arq) == 1){
            int igual = 1;
            int i = 0;
            while (pesquisa[i] != '\0' && p->livro[i] != '\0') {
                if (pesquisa[i] != p->livro[i]) {
                    igual = 0;
                    break;
                }
                i++;
            }

    if (igual == 1) {
        printf("\nO produto foi encontrado\n");
        printf("\nLivro: %s\n", p->livro);
        printf("Autor: %s\n", p->autor);
        printf("Preco: %f\n", p->preco);
        printf("Quantidade: %d\n", p->quantidade);
        fclose(arq);
        return posicao;
    }
        posicao++;
    }
    fclose(arq);
    printf("\nO produto nao foi encontrado\n");
    return -1;
}

void pesquisa_autor(struct livraria *p){

char letra;

printf("\ndigite uma letra para usar de filtro na busca de autores.");
printf("\nletra digitada: ");
scanf("%c", &letra);

arq = fopen("arq", "rb");

while(fread(p, sizeof(*p), 1, arq) == 1){
    if(letra == p->autor[0]) {
        printf("\nAutor: %s\n", p->autor);
        printf("Livro: %s\n", p->livro);
        printf("Preco: %f\n", p->preco);
        printf("Quantidade: %d\n", p->quantidade);
                             }
                                        }
}

void pesquisa_preco(struct livraria *p){

float min, max;

printf("Fale o valor minimo do livro: \n");
scanf("%f", &min);
printf("Fale o valor maximo do livro: \n");
scanf("%f", &max);

arq = fopen("arq", "rb");

while(fread(p, sizeof(*p), 1, arq) == 1){
if(p->preco >= min && p->preco <= max){
        printf("\nLivro: %s\n", p->livro);
        printf("Autor: %s\n", p->autor);
        printf("Preco: %f\n", p->preco);
        printf("Quantidade: %d\n", p->quantidade);
                                      }
                                        }
fclose(arq);
}


void altera_quantidade(struct livraria *p){

int indice;
long pos;

indice = pesquisa_livro(p);

arq = fopen("arq", "r+b");

pos = indice * sizeof(*p);

fseek(arq,pos,SEEK_SET);
fread(p, sizeof(*p), 1, arq);

if(indice >= 0){
printf("\ndigite a nova quantidade do produto que deseja altear: ");
scanf(" %d", &p->quantidade);
               }

fseek(arq,pos,SEEK_SET);
fwrite(p, sizeof(*p),1, arq);

fclose(arq);

if(indice >= 0){
    printf("quantidade alterada!");
    }
}

void altera_preco(struct livraria *p){

int indice;
long pos;

indice = pesquisa_livro(p);

arq = fopen("arq", "r+b");

pos = indice * sizeof(*p);

fseek(arq,pos,SEEK_SET);
fread(p, sizeof(*p), 1, arq);

if(indice >= 0){
printf("\ndigite o novo preco: ");
scanf(" %f", &p->preco);
               }

fseek(arq,pos,SEEK_SET);
fwrite(p, sizeof(*p),1, arq);

fclose(arq);

if(indice >= 0){
    printf("preco alterada!");
    }
}

void altera_dados(struct livraria *p){

int indice;
long pos;

indice = pesquisa_livro(p);

arq = fopen("arq", "r+b");

pos = indice * sizeof(*p);

fseek(arq,pos,SEEK_SET);
fread(p, sizeof(*p), 1, arq);

if(indice >= 0){
    printf("Fale o nome do livro: ");
    scanf(" %50[^\n]", p->livro);
    printf("Fale o nome do autor: ");
    scanf(" %50[^\n]", p->autor);
    printf("Fale o preco: ");
    scanf("%f", &p->preco);
    printf("Fale a quantidade: ");
    scanf("%d", &p->quantidade);
               }

fseek(arq,pos,SEEK_SET);
fwrite(p, sizeof(*p),1, arq);

fclose(arq);

if(indice >= 0){
    printf("quantidade alterada!");
    }

}

void exclui(struct livraria *p){

int indice;
long pos;

indice = pesquisa_livro(p);

arq = fopen("arq", "r+b");

pos = indice * sizeof(*p);

fseek(arq,pos,0);
fread(p, sizeof(*p), 1, arq);
p->livro[0] = '*';
fseek(arq,pos,0);
fwrite(p, sizeof(*p),1, arq);

fclose(arq);

if(indice >= 0){
    printf("livro exluido!\n");
               }
}



int repetido (char *palavra){
struct livraria p;

arq = fopen("arq", "rb");;
int posicao = 0;

char leitura;

    while(fread(&p, sizeof(p), 1, arq) == 1){
            int igual = 1;
            int i = 0;
            while (palavra[i] != '\0' && p.livro[i] != '\0') {
                if (palavra[i] != p.livro[i]) {
                    igual = 0;
                    break;
                }
                i++;
            }
    if (palavra[i] != p.livro[i])
            igual = 0;

    if (igual == 1) {
        return 1;
    }
    }

    fclose(arq);
    return 0;
}





















