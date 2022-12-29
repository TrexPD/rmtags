# rmtags: REMOVEDOR DE TAGS HTML

##### Script feito com **python** para remover todas as tags HTML, deixando apenas o texto puro. Com suporte parcial a entidades do html, podendo ainda salvar o conteúdo final em um arquivo de texto!

### Bibliotecas usadas:

```re```

### Uso na prática:

#### Parametros:

- **html:** str = recebe o HTML no formato de **strings**!
- **strip:** bool = remove todos os espaços antes e depois dos caracteres! (por padrão "True")
- **save_file:** bool = Cria um arquivo de texto com o resultado final! (por padrão "False")

#### Entrada dos dados e chamando a função!
```
html = """<p>&gt;&gt;&gt;O <b>sistema circulatório</b> é o conjunto de órgãos responsáveis pela distribuição
de nutrientes para as <a href="/wiki/C%C3%A9lula" title="Célula">células</a> e coleta de
suas excretas metabólicas para serem eliminadas por órgãos excretores. Os órgãos que fazem
parte do sistema circulatório são:</p>"""

print(removedor_tags_html(html))
```

#### Ouput:
```
>>> O sistema circulatório é o conjunto de órgãos responsáveis pela distribuição de nutrientes para as células e coleta de suas excretas metabólicas para serem eliminadas por órgãos excretores. Os órgãos que fazem parte do sistema circulatório são:
```


<h2 align="center">
    <strong>🌟
        Favorite este repositório 
    </strong>🌟
</h2>


<p align="center">
    Criado com ❤️ e python por
        <a href="https://github.com/TrexPD">
            Paulo Daniel (TrexPD)!
        </a>
</p> 
