from re import compile

def removedor_tags_html(html: str, strip: bool = True) -> str:
    """
    Remove todas as tags HTML é preserva apenas o texto!

    html: str = recebe o HTML no formato de strings!
    strip: bool = remove todos os espaços antes e depois dos caracteres! (por padrão "True")
    """
    string = compile(r"<[^<>]*>").sub("", html)
    if strip:
        string = string.strip()
    
    return string
     


if __name__ == "__main__":
    html = '''<p>O <b>Segway PT</b> é um <a href="/wiki/Diciclo" title="Diciclo">diciclo</a> (<a href="/wiki/Transporte" title="Transporte">meio de transporte</a> de duas <a href="/wiki/Roda" title="Roda">rodas</a> lado a lado) inventado por <a href="/wiki/Dean_Kamen" title="Dean Kamen">Dean Kamen</a> e revelado em Dezembro de <a href="/wiki/2001" title="2001">2001</a>, que funciona a partir do equilíbrio do indivíduo que o utiliza. A <a href="/wiki/Tecnologia" title="Tecnologia">tecnologia</a> existente nos Segway PT, consiste numa inteligente rede de <a href="/wiki/Sensores" class="mw-redirect" title="Sensores">sensores</a>, mecanismos e sistemas de controlo, que permite ao Segway PT o auto-equilíbrio e a deslocação em duas <a href="/wiki/Rodas" class="mw-redirect" title="Rodas">rodas</a>. 
Quando se desloca, 5 micro-giroscópios e 2 acelerómetros estudam as mudanças no terreno e a posição do corpo do condutor, a uma <a href="/wiki/Velocidade" title="Velocidade">velocidade</a> de 100 vezes por segundo. Para que o Segway PT avance, o indivíduo só precisa de se inclinar para a frente e para que recue é necessária a inclinação para trás. Para virar, basta oscilar o braço central para o lado pretendido.<span id="refbALTITUDE"><a href="#refALTITUDE">(Altitude, 2006)</a> Esta <a href="/wiki/Tecnologia" title="Tecnologia">tecnologia</a> é denominada de <i>LeanSteer</i>. É eléctrico, e utiliza duas baterias Li-ion, que lhe permitem uma autonomia de cerca de 35 <a href="/wiki/Quil%C3%B3metro" class="mw-redirect" title="Quilómetro">quilómetros</a> e uma <a href="/wiki/Velocidade" title="Velocidade">velocidade</a> máxima de 20 km/h. A carga total é de 8-10h e representa apenas um <a href="/wiki/Quilowatt" title="Quilowatt">quilowatt</a>. A sua utilização é vocacionada para a mobilidade urbana, onde poderá representar uma redução de entre 71 a 93% de emissões de <a href="/wiki/G%C3%A1s_carb%C3%B4nico" class="mw-redirect" title="Gás carbônico">gás carbônico</a> em comparação a qualquer veículo motorizado, ou <a href="/wiki/H%C3%ADbrido" class="mw-disambig" title="Híbrido">híbrido</a>. O seu custo inicial será amortizado pela sua utilização como substituto do automóvel. O nome <i>Segway PT</i> é propriedade de Segway Inc.<span id="refbBYNATURE"><a href="#refBYNATURE">(Bynature, 2008)</a>
</span></span></p>'''

    print(removedor_tags_html(html=html))
