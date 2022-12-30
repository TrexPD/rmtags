from re import compile, findall


def removedor_tags_html(html: str, strip: bool = True, save_file: bool = False) -> str:
    """
    REMOVE TODAS AS TAGS HTML É PRESERVA APENAS O TEXTO!

    html: str = Recebe o HTML no formato de strings!
    strip: bool = Remove todos os espaços antes e depois dos caracteres! (por padrão "True")
    save_file: bool = Cria um arquivo de texto com o resultado final! (por padrão "True")
    """
    lista_entidades: list = [{'&lt;': '<'},{'&gt;': '>'},{'&amp;': '&'},{'&quot;': '"'},
    {'&apos;': "'"},{'&cent;': '\xa2'},{'&pound;': '\xa3'},{'&yen;': '\xa5'},
    {'&euro;': '\u20ac'},{'&copy;': '\xa9\ufe0f'},{'&reg;': '\xae'}]
    
    for dicios in lista_entidades:
        for key, value in dicios.items():
            if findall(f'{key}', html):
                html: str = html.replace(f'{key}', f'{value}')
    
    string = compile(r"<[^<>]*>").sub("", html)
    if strip:
        string = string.strip()
    if save_file:
        with open('sem_tags.txt', 'wt', encoding='UTF-8') as arquivo:
            arquivo.write(string)
    return string
     


if __name__ == "__main__":
    html = '''<div class="section" id="advanced-usage">
<h1>Advanced Usage<a class="headerlink" href="#advanced-usage" title="Permalink to this headline">¶</a></h1>
<div class="section" id="remarks-on-storage">
<h2>Remarks on Storage<a class="headerlink" href="#remarks-on-storage" title="Permalink to this headline">¶</a></h2>
<p>Before we dive deeper into the usage of TinyDB, we should stop for a moment
and discuss how TinyDB stores data.</p>
<p>To convert your data to a format that is writable to disk TinyDB uses the
<a class="reference external" href="http://docs.python.org/2/library/json.html">Python JSON</a> module by default.
It’s great when only simple data types are involved but it cannot handle more
complex data types like custom classes. On Python 2 it also converts strings to
Unicode strings upon reading
(described <a class="reference external" href="http://stackoverflow.com/q/956867/997063">here</a>).</p>
<p>If that causes problems, you can write
<a class="reference internal" href="extend.html"><span class="doc">your own storage</span></a>, that uses a more powerful (but also slower)
library like <a class="reference external" href="http://docs.python.org/library/pickle.html">pickle</a> or
<a class="reference external" href="http://pyyaml.org/">PyYAML</a>.</p>
<div class="admonition hint">
<p class="first admonition-title">Hint</p>
<p class="last">Opening multiple TinyDB instances on the same data (e.g. with the
<code class="docutils literal notranslate"><span class="pre">JSONStorage</span></code>) may result in unexpected behavior due to query caching.
See <a class="reference internal" href="#query-caching">query_caching</a> on how to disable the query cache.</p>
</div>
</div>
<div class="section" id="queries">
<h2>Queries<a class="headerlink" href="#queries" title="Permalink to this headline">¶</a></h2>
<p>With that out of the way, let’s start with TinyDB’s rich set of queries.
There are two main ways to construct queries. The first one resembles the
syntax of popular ORM tools:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="kn">from</span> <span class="nn">tinydb</span> <span class="kn">import</span> <span class="n">Query</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">User</span> <span class="o">=</span> <span class="n">Query</span><span class="p">()</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">User</span><span class="o">.</span><span class="n">name</span> <span class="o">==</span> <span class="s1">'John'</span><span class="p">)</span>
</pre></div>
</div>
<p>As you can see, we first create a new Query object and then use it to specify
which fields to check. Searching for nested fields is just as easy:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">User</span><span class="o">.</span><span class="n">birthday</span><span class="o">.</span><span class="n">year</span> <span class="o">==</span> <span class="mi">1990</span><span class="p">)</span>
</pre></div>
</div>
<p>Not all fields can be accessed this way if the field name is not a valid Python
identifier. In this case, you can switch to dict access notation:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="c1"># This would be invalid Python syntax:</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">User</span><span class="o">.</span><span class="n">country</span><span class="o">-</span><span class="n">code</span> <span class="o">==</span> <span class="s1">'foo'</span><span class="p">)</span>
<span class="gp">&gt;&gt;&gt; </span><span class="c1"># Use this instead:</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">User</span><span class="p">[</span><span class="s1">'country-code'</span><span class="p">]</span> <span class="o">==</span> <span class="s1">'foo'</span><span class="p">)</span>
</pre></div>
</div>
<p>In addition, you can use arbitrary transform function where a field would be,
for example:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="kn">from</span> <span class="nn">unidecode</span> <span class="kn">import</span> <span class="n">unidecode</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">User</span><span class="o">.</span><span class="n">name</span><span class="o">.</span><span class="n">map</span><span class="p">(</span><span class="n">unidecode</span><span class="p">)</span> <span class="o">==</span> <span class="s1">'Jose'</span><span class="p">)</span>
<span class="gp">&gt;&gt;&gt; </span><span class="c1"># will match 'José' etc.</span>
</pre></div>
</div>
<p>The second, traditional way of constructing queries is as follows:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="kn">from</span> <span class="nn">tinydb</span> <span class="kn">import</span> <span class="n">where</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">where</span><span class="p">(</span><span class="s1">'field'</span><span class="p">)</span> <span class="o">==</span> <span class="s1">'value'</span><span class="p">)</span>
</pre></div>
</div>
<p>Using <code class="docutils literal notranslate"><span class="pre">where('field')</span></code> is a shorthand for the following code:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">Query</span><span class="p">()[</span><span class="s1">'field'</span><span class="p">]</span> <span class="o">==</span> <span class="s1">'value'</span><span class="p">)</span>
</pre></div>
</div>
<p>Accessing nested fields with this syntax can be achieved like this:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">where</span><span class="p">(</span><span class="s1">'birthday'</span><span class="p">)</span><span class="o">.</span><span class="n">year</span> <span class="o">==</span> <span class="mi">1900</span><span class="p">)</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">where</span><span class="p">(</span><span class="s1">'birthday'</span><span class="p">)[</span><span class="s1">'year'</span><span class="p">]</span> <span class="o">==</span> <span class="mi">1900</span><span class="p">)</span>
</pre></div>
</div>
<div class="section" id="advanced-queries">
<h3>Advanced queries<a class="headerlink" href="#advanced-queries" title="Permalink to this headline">¶</a></h3>
<p>In the <a class="reference internal" href="getting-started.html"><span class="doc">Getting Started</span></a> you’ve learned about the basic comparisons
(<code class="docutils literal notranslate"><span class="pre">==</span></code>, <code class="docutils literal notranslate"><span class="pre">&lt;</span></code>, <code class="docutils literal notranslate"><span class="pre">&gt;</span></code>, …). In addition to these TinyDB supports the following
queries:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="c1"># Existence of a field:</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">User</span><span class="o">.</span><span class="n">name</span><span class="o">.</span><span class="n">exists</span><span class="p">())</span>
</pre></div>
</div>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="c1"># Regex:</span>
<span class="gp">&gt;&gt;&gt; </span><span class="c1"># Full item has to match the regex:</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">User</span><span class="o">.</span><span class="n">name</span><span class="o">.</span><span class="n">matches</span><span class="p">(</span><span class="s1">'[aZ]*'</span><span class="p">))</span>
<span class="gp">&gt;&gt;&gt; </span><span class="c1"># Case insensitive search for 'John':</span>
<span class="gp">&gt;&gt;&gt; </span><span class="kn">import</span> <span class="nn">re</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">User</span><span class="o">.</span><span class="n">name</span><span class="o">.</span><span class="n">matches</span><span class="p">(</span><span class="s1">'John'</span><span class="p">,</span> <span class="n">flags</span><span class="o">=</span><span class="n">re</span><span class="o">.</span><span class="n">IGNORECASE</span><span class="p">))</span>
<span class="gp">&gt;&gt;&gt; </span><span class="c1"># Any part of the item has to match the regex:</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">User</span><span class="o">.</span><span class="n">name</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="s1">'b+'</span><span class="p">))</span>
</pre></div>
</div>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="c1"># Custom test:</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">test_func</span> <span class="o">=</span> <span class="k">lambda</span> <span class="n">s</span><span class="p">:</span> <span class="n">s</span> <span class="o">==</span> <span class="s1">'John'</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">User</span><span class="o">.</span><span class="n">name</span><span class="o">.</span><span class="n">test</span><span class="p">(</span><span class="n">test_func</span><span class="p">))</span>
</pre></div>
</div>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="c1"># Custom test with parameters:</span>
<span class="gp">&gt;&gt;&gt; </span><span class="k">def</span> <span class="nf">test_func</span><span class="p">(</span><span class="n">val</span><span class="p">,</span> <span class="n">m</span><span class="p">,</span> <span class="n">n</span><span class="p">):</span>
<span class="gp">&gt;&gt;&gt; </span>    <span class="k">return</span> <span class="n">m</span> <span class="o">&lt;=</span> <span class="n">val</span> <span class="o">&lt;=</span> <span class="n">n</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">User</span><span class="o">.</span><span class="n">age</span><span class="o">.</span><span class="n">test</span><span class="p">(</span><span class="n">test_func</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="mi">21</span><span class="p">))</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">User</span><span class="o">.</span><span class="n">age</span><span class="o">.</span><span class="n">test</span><span class="p">(</span><span class="n">test_func</span><span class="p">,</span> <span class="mi">21</span><span class="p">,</span> <span class="mi">99</span><span class="p">))</span>
</pre></div>
</div>
<p>Another case is if you have a <code class="docutils literal notranslate"><span class="pre">dict</span></code> where you want to find all documents
that match this <code class="docutils literal notranslate"><span class="pre">dict</span></code>. We call this searching for a fragment:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">Query</span><span class="p">()</span><span class="o">.</span><span class="n">fragment</span><span class="p">({</span><span class="s1">'foo'</span><span class="p">:</span> <span class="kc">True</span><span class="p">,</span> <span class="s1">'bar'</span><span class="p">:</span> <span class="kc">False</span><span class="p">}))</span>
<span class="go">[{'foo': True, 'bar': False, 'foobar: 'yes!'}]</span>
</pre></div>
</div>
<p>You also can search for documents where a specific field matches the fragment:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">Query</span><span class="p">()</span><span class="o">.</span><span class="n">field</span><span class="o">.</span><span class="n">fragment</span><span class="p">({</span><span class="s1">'foo'</span><span class="p">:</span> <span class="kc">True</span><span class="p">,</span> <span class="s1">'bar'</span><span class="p">:</span> <span class="kc">False</span><span class="p">}))</span>
<span class="go">[{'field': {'foo': True, 'bar': False, 'foobar: 'yes!'}]</span>
</pre></div>
</div>
<p>When a field contains a list, you also can use the <code class="docutils literal notranslate"><span class="pre">any</span></code> and <code class="docutils literal notranslate"><span class="pre">all</span></code> methods.
There are two ways to use them: with lists of values and with nested queries.
Let’s start with the first one. Assuming we have a user object with a groups list
like this:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">insert</span><span class="p">({</span><span class="s1">'name'</span><span class="p">:</span> <span class="s1">'user1'</span><span class="p">,</span> <span class="s1">'groups'</span><span class="p">:</span> <span class="p">[</span><span class="s1">'user'</span><span class="p">]})</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">insert</span><span class="p">({</span><span class="s1">'name'</span><span class="p">:</span> <span class="s1">'user2'</span><span class="p">,</span> <span class="s1">'groups'</span><span class="p">:</span> <span class="p">[</span><span class="s1">'admin'</span><span class="p">,</span> <span class="s1">'user'</span><span class="p">]})</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">insert</span><span class="p">({</span><span class="s1">'name'</span><span class="p">:</span> <span class="s1">'user3'</span><span class="p">,</span> <span class="s1">'groups'</span><span class="p">:</span> <span class="p">[</span><span class="s1">'sudo'</span><span class="p">,</span> <span class="s1">'user'</span><span class="p">]})</span>
</pre></div>
</div>
<p>Now we can use the following queries:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="c1"># User's groups include at least one value from ['admin', 'sudo']</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">User</span><span class="o">.</span><span class="n">groups</span><span class="o">.</span><span class="n">any</span><span class="p">([</span><span class="s1">'admin'</span><span class="p">,</span> <span class="s1">'sudo'</span><span class="p">]))</span>
<span class="go">[{'name': 'user2', 'groups': ['admin', 'user']},</span>
<span class="go"> {'name': 'user3', 'groups': ['sudo', 'user']}]</span>
<span class="go">&gt;&gt;&gt;</span>
<span class="gp">&gt;&gt;&gt; </span><span class="c1"># User's groups include all values from ['admin', 'user']</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">User</span><span class="o">.</span><span class="n">groups</span><span class="o">.</span><span class="n">all</span><span class="p">([</span><span class="s1">'admin'</span><span class="p">,</span> <span class="s1">'user'</span><span class="p">]))</span>
<span class="go">[{'name': 'user2', 'groups': ['admin', 'user']}]</span>
</pre></div>
</div>
<p>In some cases you may want to have more complex <code class="docutils literal notranslate"><span class="pre">any</span></code>/<code class="docutils literal notranslate"><span class="pre">all</span></code> queries.
This is where nested queries come in as helpful. Let’s set up a table like this:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">Group</span> <span class="o">=</span> <span class="n">Query</span><span class="p">()</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">Permission</span> <span class="o">=</span> <span class="n">Query</span><span class="p">()</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">groups</span> <span class="o">=</span> <span class="n">db</span><span class="o">.</span><span class="n">table</span><span class="p">(</span><span class="s1">'groups'</span><span class="p">)</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">groups</span><span class="o">.</span><span class="n">insert</span><span class="p">({</span>
<span class="go">        'name': 'user',</span>
<span class="go">        'permissions': [{'type': 'read'}]})</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">groups</span><span class="o">.</span><span class="n">insert</span><span class="p">({</span>
<span class="go">        'name': 'sudo',</span>
<span class="go">        'permissions': [{'type': 'read'}, {'type': 'sudo'}]})</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">groups</span><span class="o">.</span><span class="n">insert</span><span class="p">({</span>
<span class="go">        'name': 'admin',</span>
<span class="go">        'permissions': [{'type': 'read'}, {'type': 'write'}, {'type': 'sudo'}]})</span>
</pre></div>
</div>
<p>Now let’s search this table using nested <code class="docutils literal notranslate"><span class="pre">any</span></code>/<code class="docutils literal notranslate"><span class="pre">all</span></code> queries:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="c1"># Group has a permission with type 'read'</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">groups</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">Group</span><span class="o">.</span><span class="n">permissions</span><span class="o">.</span><span class="n">any</span><span class="p">(</span><span class="n">Permission</span><span class="o">.</span><span class="n">type</span> <span class="o">==</span> <span class="s1">'read'</span><span class="p">))</span>
<span class="go">[{'name': 'user', 'permissions': [{'type': 'read'}]},</span>
<span class="go"> {'name': 'sudo', 'permissions': [{'type': 'read'}, {'type': 'sudo'}]},</span>
<span class="go"> {'name': 'admin', 'permissions':</span>
<span class="go">        [{'type': 'read'}, {'type': 'write'}, {'type': 'sudo'}]}]</span>
<span class="gp">&gt;&gt;&gt; </span><span class="c1"># Group has ONLY permission 'read'</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">groups</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">Group</span><span class="o">.</span><span class="n">permissions</span><span class="o">.</span><span class="n">all</span><span class="p">(</span><span class="n">Permission</span><span class="o">.</span><span class="n">type</span> <span class="o">==</span> <span class="s1">'read'</span><span class="p">))</span>
<span class="go">[{'name': 'user', 'permissions': [{'type': 'read'}]}]</span>
</pre></div>
</div>
<p>As you can see, <code class="docutils literal notranslate"><span class="pre">any</span></code> tests if there is <em>at least one</em> document matching
the query while <code class="docutils literal notranslate"><span class="pre">all</span></code> ensures <em>all</em> documents match the query.</p>
<p>The opposite operation, checking if a single item is contained in a list,
is also possible using <code class="docutils literal notranslate"><span class="pre">one_of</span></code>:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">User</span><span class="o">.</span><span class="n">name</span><span class="o">.</span><span class="n">one_of</span><span class="p">([</span><span class="s1">'jane'</span><span class="p">,</span> <span class="s1">'john'</span><span class="p">]))</span>
</pre></div>
</div>
</div>
<div class="section" id="query-modifiers">
<h3>Query modifiers<a class="headerlink" href="#query-modifiers" title="Permalink to this headline">¶</a></h3>
<p>TinyDB also allows you to use logical operations to modify and combine
queries:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="c1"># Negate a query:</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="o">~</span> <span class="p">(</span><span class="n">User</span><span class="o">.</span><span class="n">name</span> <span class="o">==</span> <span class="s1">'John'</span><span class="p">))</span>
</pre></div>
</div>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="c1"># Logical AND:</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">search</span><span class="p">((</span><span class="n">User</span><span class="o">.</span><span class="n">name</span> <span class="o">==</span> <span class="s1">'John'</span><span class="p">)</span> <span class="o">&amp;</span> <span class="p">(</span><span class="n">User</span><span class="o">.</span><span class="n">age</span> <span class="o">&lt;=</span> <span class="mi">30</span><span class="p">))</span>
</pre></div>
</div>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="c1"># Logical OR:</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">search</span><span class="p">((</span><span class="n">User</span><span class="o">.</span><span class="n">name</span> <span class="o">==</span> <span class="s1">'John'</span><span class="p">)</span> <span class="o">|</span> <span class="p">(</span><span class="n">User</span><span class="o">.</span><span class="n">name</span> <span class="o">==</span> <span class="s1">'Bob'</span><span class="p">))</span>
</pre></div>
</div>
<div class="admonition note">
<p class="first admonition-title">Note</p>
<p>When using <code class="docutils literal notranslate"><span class="pre">&amp;</span></code> or <code class="docutils literal notranslate"><span class="pre">|</span></code>, make sure you wrap the conditions on both sides
with parentheses or Python will mess up the comparison.</p>
<p>Also, when using negation (<code class="docutils literal notranslate"><span class="pre">~</span></code>) you’ll have to wrap the query you want
to negate in parentheses.</p>
<p class="last">The reason for these requirements is that Python’s binary operators that are
used for query modifiers have a higher operator precedence than comparison
operators. Simply put, <code class="docutils literal notranslate"><span class="pre">~</span> <span class="pre">User.name</span> <span class="pre">==</span> <span class="pre">'John'</span></code> is parsed by Python as
<code class="docutils literal notranslate"><span class="pre">(~User.name)</span> <span class="pre">==</span> <span class="pre">'John'</span></code> instead of <code class="docutils literal notranslate"><span class="pre">~(User.name</span> <span class="pre">==</span> <span class="pre">'John')</span></code>. See also the
Python <a class="reference external" href="https://docs.python.org/3/reference/expressions.html#operator-precedence">docs on operator precedence</a>
for details.</p>
</div>
</div>
<div class="section" id="recap">
<h3>Recap<a class="headerlink" href="#recap" title="Permalink to this headline">¶</a></h3>
<p>Let’s review the query operations we’ve learned:</p>
<div class="wy-table-responsive"><table border="1" class="docutils">
<colgroup>
<col width="38%">
<col width="62%">
</colgroup>
<tbody valign="top">
<tr class="row-odd"><td colspan="2"><strong>Queries</strong></td>
</tr>
<tr class="row-even"><td><code class="docutils literal notranslate"><span class="pre">Query().field.exists()</span></code></td>
<td>Match any document where a field called <code class="docutils literal notranslate"><span class="pre">field</span></code> exists</td>
</tr>
<tr class="row-odd"><td><code class="docutils literal notranslate"><span class="pre">Query().field.matches(regex)</span></code></td>
<td>Match any document with the whole field matching the
regular expression</td>
</tr>
<tr class="row-even"><td><code class="docutils literal notranslate"><span class="pre">Query().field.search(regex)</span></code></td>
<td>Match any document with a substring of the field matching
the regular expression</td>
</tr>
<tr class="row-odd"><td><code class="docutils literal notranslate"><span class="pre">Query().field.test(func,</span> <span class="pre">*args)</span></code></td>
<td>Matches any document for which the function returns
<code class="docutils literal notranslate"><span class="pre">True</span></code></td>
</tr>
<tr class="row-even"><td><code class="docutils literal notranslate"><span class="pre">Query().field.all(query</span> <span class="pre">|</span> <span class="pre">list)</span></code></td>
<td>If given a query, matches all documents where all documents
in the list <code class="docutils literal notranslate"><span class="pre">field</span></code> match the query.
If given a list, matches all documents where all documents
in the list <code class="docutils literal notranslate"><span class="pre">field</span></code> are a member of the given list</td>
</tr>
<tr class="row-odd"><td><code class="docutils literal notranslate"><span class="pre">Query().field.any(query</span> <span class="pre">|</span> <span class="pre">list)</span></code></td>
<td>If given a query, matches all documents where at least one
document in the list <code class="docutils literal notranslate"><span class="pre">field</span></code> match the query.
If given a list, matches all documents where at least one
documents in the list <code class="docutils literal notranslate"><span class="pre">field</span></code> are a member of the given
list</td>
</tr>
<tr class="row-even"><td><code class="docutils literal notranslate"><span class="pre">Query().field.one_of(list)</span></code></td>
<td>Match if the field is contained in the list</td>
</tr>
<tr class="row-odd"><td colspan="2"><strong>Logical operations on queries</strong></td>
</tr>
<tr class="row-even"><td><code class="docutils literal notranslate"><span class="pre">~</span> <span class="pre">(query)</span></code></td>
<td>Match documents that don’t match the query</td>
</tr>
<tr class="row-odd"><td><code class="docutils literal notranslate"><span class="pre">(query1)</span> <span class="pre">&amp;</span> <span class="pre">(query2)</span></code></td>
<td>Match documents that match both queries</td>
</tr>
<tr class="row-even"><td><code class="docutils literal notranslate"><span class="pre">(query1)</span> <span class="pre">|</span> <span class="pre">(query2)</span></code></td>
<td>Match documents that match at least one of the queries</td>
</tr>
</tbody>
</table></div>
</div>
</div>
<div class="section" id="handling-data">
<h2>Handling Data<a class="headerlink" href="#handling-data" title="Permalink to this headline">¶</a></h2>
<p>Next, let’s look at some more ways to insert, update and retrieve data from
your database.</p>
<div class="section" id="inserting-data">
<h3>Inserting data<a class="headerlink" href="#inserting-data" title="Permalink to this headline">¶</a></h3>
<p>As already described you can insert a document using <code class="docutils literal notranslate"><span class="pre">db.insert(...)</span></code>.
In case you want to insert multiple documents, you can use <code class="docutils literal notranslate"><span class="pre">db.insert_multiple(...)</span></code>:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">insert_multiple</span><span class="p">([</span>
<span class="go">        {'name': 'John', 'age': 22},</span>
<span class="go">        {'name': 'John', 'age': 37}])</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">insert_multiple</span><span class="p">({</span><span class="s1">'int'</span><span class="p">:</span> <span class="mi">1</span><span class="p">,</span> <span class="s1">'value'</span><span class="p">:</span> <span class="n">i</span><span class="p">}</span> <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">2</span><span class="p">))</span>
</pre></div>
</div>
<p>Also in some cases it may be useful to specify the document ID yourself when
inserting data. You can do that by using the <a class="reference internal" href="api.html#tinydb.table.Document" title="tinydb.table.Document"><code class="xref py py-class docutils literal notranslate"><span class="pre">Document</span></code></a>
class:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">insert</span><span class="p">(</span><span class="n">Document</span><span class="p">({</span><span class="s1">'name'</span><span class="p">:</span> <span class="s1">'John'</span><span class="p">,</span> <span class="s1">'age'</span><span class="p">:</span> <span class="mi">22</span><span class="p">},</span> <span class="n">doc_id</span><span class="o">=</span><span class="mi">12</span><span class="p">))</span>
<span class="go">12</span>
</pre></div>
</div>
<p>The same is possible when using <code class="docutils literal notranslate"><span class="pre">db.insert_multiple(...)</span></code>:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">insert_multiple</span><span class="p">([</span>
<span class="go">    Document({'name': 'John', 'age': 22}, doc_id=12),</span>
<span class="go">    Document({'name': 'Jane', 'age': 24}, doc_id=14),</span>
<span class="go">])</span>
<span class="go">[12, 14]</span>
</pre></div>
</div>
<div class="admonition note">
<p class="first admonition-title">Note</p>
<p class="last">Inserting a <code class="docutils literal notranslate"><span class="pre">Document</span></code> with an ID that already exists will result
in a <code class="docutils literal notranslate"><span class="pre">ValueError</span></code> being raised.</p>
</div>
</div>
<div class="section" id="updating-data">
<h3>Updating data<a class="headerlink" href="#updating-data" title="Permalink to this headline">¶</a></h3>
<p>Sometimes you want to update all documents in your database. In this case, you
can leave out the <code class="docutils literal notranslate"><span class="pre">query</span></code> argument:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">update</span><span class="p">({</span><span class="s1">'foo'</span><span class="p">:</span> <span class="s1">'bar'</span><span class="p">})</span>
</pre></div>
</div>
<p>When passing a dict to <code class="docutils literal notranslate"><span class="pre">db.update(fields,</span> <span class="pre">query)</span></code>, it only allows you to
update a document by adding or overwriting its values. But sometimes you may
need to e.g. remove one field or increment its value. In that case you can
pass a function instead of <code class="docutils literal notranslate"><span class="pre">fields</span></code>:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="kn">from</span> <span class="nn">tinydb.operations</span> <span class="kn">import</span> <span class="n">delete</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">update</span><span class="p">(</span><span class="n">delete</span><span class="p">(</span><span class="s1">'key1'</span><span class="p">),</span> <span class="n">User</span><span class="o">.</span><span class="n">name</span> <span class="o">==</span> <span class="s1">'John'</span><span class="p">)</span>
</pre></div>
</div>
<p>This will remove the key <code class="docutils literal notranslate"><span class="pre">key1</span></code> from all matching documents. TinyDB comes
with these operations:</p>
<ul class="simple">
<li><code class="docutils literal notranslate"><span class="pre">delete(key)</span></code>: delete a key from the document</li>
<li><code class="docutils literal notranslate"><span class="pre">increment(key)</span></code>: increment the value of a key</li>
<li><code class="docutils literal notranslate"><span class="pre">decrement(key)</span></code>: decrement the value of a key</li>
<li><code class="docutils literal notranslate"><span class="pre">add(key,</span> <span class="pre">value)</span></code>: add <code class="docutils literal notranslate"><span class="pre">value</span></code> to the value of a key (also works for strings)</li>
<li><code class="docutils literal notranslate"><span class="pre">subtract(key,</span> <span class="pre">value)</span></code>: subtract <code class="docutils literal notranslate"><span class="pre">value</span></code> from the value of a key</li>
<li><code class="docutils literal notranslate"><span class="pre">set(key,</span> <span class="pre">value)</span></code>: set <code class="docutils literal notranslate"><span class="pre">key</span></code> to <code class="docutils literal notranslate"><span class="pre">value</span></code></li>
</ul>
<p>Of course you also can write your own operations:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="k">def</span> <span class="nf">your_operation</span><span class="p">(</span><span class="n">your_arguments</span><span class="p">):</span>
<span class="gp">... </span>    <span class="k">def</span> <span class="nf">transform</span><span class="p">(</span><span class="n">doc</span><span class="p">):</span>
<span class="gp">... </span>        <span class="c1"># do something with the document</span>
<span class="gp">... </span>        <span class="c1"># ...</span>
<span class="gp">... </span>    <span class="k">return</span> <span class="n">transform</span>
<span class="gp">...</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">update</span><span class="p">(</span><span class="n">your_operation</span><span class="p">(</span><span class="n">arguments</span><span class="p">),</span> <span class="n">query</span><span class="p">)</span>
</pre></div>
</div>
<p>In order to perform multiple update operations at once, you can use the
<code class="docutils literal notranslate"><span class="pre">update_multiple</span></code> method like this:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">update_multiple</span><span class="p">([</span>
<span class="gp">... </span>    <span class="p">({</span><span class="s1">'int'</span><span class="p">:</span> <span class="mi">2</span><span class="p">},</span> <span class="n">where</span><span class="p">(</span><span class="s1">'char'</span><span class="p">)</span> <span class="o">==</span> <span class="s1">'a'</span><span class="p">),</span>
<span class="gp">... </span>    <span class="p">({</span><span class="s1">'int'</span><span class="p">:</span> <span class="mi">4</span><span class="p">},</span> <span class="n">where</span><span class="p">(</span><span class="s1">'char'</span><span class="p">)</span> <span class="o">==</span> <span class="s1">'b'</span><span class="p">),</span>
<span class="gp">... </span><span class="p">])</span>
</pre></div>
</div>
<p>You also can use mix normal updates with update operations:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">update_multiple</span><span class="p">([</span>
<span class="gp">... </span>    <span class="p">({</span><span class="s1">'int'</span><span class="p">:</span> <span class="mi">2</span><span class="p">},</span> <span class="n">where</span><span class="p">(</span><span class="s1">'char'</span><span class="p">)</span> <span class="o">==</span> <span class="s1">'a'</span><span class="p">),</span>
<span class="gp">... </span>    <span class="p">({</span><span class="n">delete</span><span class="p">(</span><span class="s1">'int'</span><span class="p">),</span> <span class="n">where</span><span class="p">(</span><span class="s1">'char'</span><span class="p">)</span> <span class="o">==</span> <span class="s1">'b'</span><span class="p">),</span>
<span class="gp">... </span><span class="p">])</span>
</pre></div>
</div>
</div>
</div>
<div class="section" id="data-access-and-modification">
<h2>Data access and modification<a class="headerlink" href="#data-access-and-modification" title="Permalink to this headline">¶</a></h2>
<div class="section" id="upserting-data">
<h3>Upserting data<a class="headerlink" href="#upserting-data" title="Permalink to this headline">¶</a></h3>
<p>In some cases you’ll need a mix of both <code class="docutils literal notranslate"><span class="pre">update</span></code> and <code class="docutils literal notranslate"><span class="pre">insert</span></code>: <code class="docutils literal notranslate"><span class="pre">upsert</span></code>.
This operation is provided a document and a query. If it finds any documents
matching the query, they will be updated with the data from the provided document.
On the other hand, if no matching document is found, it inserts the provided
document into the table:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">upsert</span><span class="p">({</span><span class="s1">'name'</span><span class="p">:</span> <span class="s1">'John'</span><span class="p">,</span> <span class="s1">'logged-in'</span><span class="p">:</span> <span class="kc">True</span><span class="p">},</span> <span class="n">User</span><span class="o">.</span><span class="n">name</span> <span class="o">==</span> <span class="s1">'John'</span><span class="p">)</span>
</pre></div>
</div>
<p>This will update all users with the name John to have <code class="docutils literal notranslate"><span class="pre">logged-in</span></code> set to <code class="docutils literal notranslate"><span class="pre">True</span></code>.
If no matching user is found, a new document is inserted with both the name set
and the <code class="docutils literal notranslate"><span class="pre">logged-in</span></code> flag.</p>
<p>To use the ID of the document as matching criterion a <a class="reference internal" href="api.html#tinydb.table.Document" title="tinydb.table.Document"><code class="xref py py-class docutils literal notranslate"><span class="pre">Document</span></code></a>
with <code class="docutils literal notranslate"><span class="pre">doc_id</span></code> is passed instead of a query:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">upsert</span><span class="p">(</span><span class="n">Document</span><span class="p">({</span><span class="s1">'name'</span><span class="p">:</span> <span class="s1">'John'</span><span class="p">,</span> <span class="s1">'logged-in'</span><span class="p">:</span> <span class="kc">True</span><span class="p">},</span> <span class="n">doc_id</span><span class="o">=</span><span class="mi">12</span><span class="p">))</span>
</pre></div>
</div>
</div>
<div class="section" id="retrieving-data">
<h3>Retrieving data<a class="headerlink" href="#retrieving-data" title="Permalink to this headline">¶</a></h3>
<p>There are several ways to retrieve data from your database. For instance you
can get the number of stored documents:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="nb">len</span><span class="p">(</span><span class="n">db</span><span class="p">)</span>
<span class="go">3</span>
</pre></div>
</div>
<div class="admonition hint">
<p class="first admonition-title">Hint</p>
<p class="last">This will return the number of documents in the default table
(see the notes on the <a class="reference internal" href="#default-table"><span class="std std-ref">default table</span></a>).</p>
</div>
<p>Then of course you can use <code class="docutils literal notranslate"><span class="pre">db.search(...)</span></code> as described in the <a class="reference internal" href="getting-started.html"><span class="doc">Getting Started</span></a>
section. But sometimes you want to get only one matching document. Instead of using</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="k">try</span><span class="p">:</span>
<span class="gp">... </span>    <span class="n">result</span> <span class="o">=</span> <span class="n">db</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">User</span><span class="o">.</span><span class="n">name</span> <span class="o">==</span> <span class="s1">'John'</span><span class="p">)[</span><span class="mi">0</span><span class="p">]</span>
<span class="gp">... </span><span class="k">except</span> <span class="ne">IndexError</span><span class="p">:</span>
<span class="gp">... </span>    <span class="k">pass</span>
</pre></div>
</div>
<p>you can use <code class="docutils literal notranslate"><span class="pre">db.get(...)</span></code>:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="n">User</span><span class="o">.</span><span class="n">name</span> <span class="o">==</span> <span class="s1">'John'</span><span class="p">)</span>
<span class="go">{'name': 'John', 'age': 22}</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="n">User</span><span class="o">.</span><span class="n">name</span> <span class="o">==</span> <span class="s1">'Bobby'</span><span class="p">)</span>
<span class="go">None</span>
</pre></div>
</div>
<div class="admonition caution">
<p class="first admonition-title">Caution</p>
<p class="last">If multiple documents match the query, probably a random one of them will
be returned!</p>
</div>
<p>Often you don’t want to search for documents but only know whether they are
stored in the database. In this case <code class="docutils literal notranslate"><span class="pre">db.contains(...)</span></code> is your friend:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">contains</span><span class="p">(</span><span class="n">User</span><span class="o">.</span><span class="n">name</span> <span class="o">==</span> <span class="s1">'John'</span><span class="p">)</span>
</pre></div>
</div>
<p>In a similar manner you can look up the number of documents matching a query:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">count</span><span class="p">(</span><span class="n">User</span><span class="o">.</span><span class="n">name</span> <span class="o">==</span> <span class="s1">'John'</span><span class="p">)</span>
<span class="go">2</span>
</pre></div>
</div>
<div class="section" id="id1">
<h4>Recap<a class="headerlink" href="#id1" title="Permalink to this headline">¶</a></h4>
<p>Let’s summarize the ways to handle data:</p>
<div class="wy-table-responsive"><table border="1" class="docutils">
<colgroup>
<col width="33%">
<col width="67%">
</colgroup>
<tbody valign="top">
<tr class="row-odd"><td colspan="2"><strong>Inserting data</strong></td>
</tr>
<tr class="row-even"><td><code class="docutils literal notranslate"><span class="pre">db.insert_multiple(...)</span></code></td>
<td>Insert multiple documents</td>
</tr>
<tr class="row-odd"><td colspan="2"><strong>Updating data</strong></td>
</tr>
<tr class="row-even"><td><code class="docutils literal notranslate"><span class="pre">db.update(operation,</span> <span class="pre">...)</span></code></td>
<td>Update all matching documents with a special operation</td>
</tr>
<tr class="row-odd"><td colspan="2"><strong>Retrieving data</strong></td>
</tr>
<tr class="row-even"><td><code class="docutils literal notranslate"><span class="pre">len(db)</span></code></td>
<td>Get the number of documents in the database</td>
</tr>
<tr class="row-odd"><td><code class="docutils literal notranslate"><span class="pre">db.get(query)</span></code></td>
<td>Get one document matching the query</td>
</tr>
<tr class="row-even"><td><code class="docutils literal notranslate"><span class="pre">db.contains(query)</span></code></td>
<td>Check if the database contains a matching document</td>
</tr>
<tr class="row-odd"><td><code class="docutils literal notranslate"><span class="pre">db.count(query)</span></code></td>
<td>Get the number of matching documents</td>
</tr>
</tbody>
</table></div>
<div class="admonition note">
<p class="first admonition-title">Note</p>
<p class="last">This was a new feature in v3.6.0</p>
</div>
</div>
</div>
</div>
<div class="section" id="using-document-ids">
<span id="document-ids"></span><h2>Using Document IDs<a class="headerlink" href="#using-document-ids" title="Permalink to this headline">¶</a></h2>
<p>Internally TinyDB associates an ID with every document you insert. It’s returned
after inserting a document:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">insert</span><span class="p">({</span><span class="s1">'name'</span><span class="p">:</span> <span class="s1">'John'</span><span class="p">,</span> <span class="s1">'age'</span><span class="p">:</span> <span class="mi">22</span><span class="p">})</span>
<span class="go">3</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">insert_multiple</span><span class="p">([{</span><span class="o">...</span><span class="p">},</span> <span class="p">{</span><span class="o">...</span><span class="p">},</span> <span class="p">{</span><span class="o">...</span><span class="p">}])</span>
<span class="go">[4, 5, 6]</span>
</pre></div>
</div>
<p>In addition you can get the ID of already inserted documents using
<code class="docutils literal notranslate"><span class="pre">document.doc_id</span></code>. This works both with <code class="docutils literal notranslate"><span class="pre">get</span></code> and <code class="docutils literal notranslate"><span class="pre">all</span></code>:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">el</span> <span class="o">=</span> <span class="n">db</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="n">User</span><span class="o">.</span><span class="n">name</span> <span class="o">==</span> <span class="s1">'John'</span><span class="p">)</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">el</span><span class="o">.</span><span class="n">doc_id</span>
<span class="go">3</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">el</span> <span class="o">=</span> <span class="n">db</span><span class="o">.</span><span class="n">all</span><span class="p">()[</span><span class="mi">0</span><span class="p">]</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">el</span><span class="o">.</span><span class="n">doc_id</span>
<span class="go">1</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">el</span> <span class="o">=</span> <span class="n">db</span><span class="o">.</span><span class="n">all</span><span class="p">()[</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">el</span><span class="o">.</span><span class="n">doc_id</span>
<span class="go">12</span>
</pre></div>
</div>
<p>Different TinyDB methods also work with IDs, namely: <code class="docutils literal notranslate"><span class="pre">update</span></code>, <code class="docutils literal notranslate"><span class="pre">remove</span></code>,
<code class="docutils literal notranslate"><span class="pre">contains</span></code> and <code class="docutils literal notranslate"><span class="pre">get</span></code>. The first two also return a list of affected IDs.</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">update</span><span class="p">({</span><span class="s1">'value'</span><span class="p">:</span> <span class="mi">2</span><span class="p">},</span> <span class="n">doc_ids</span><span class="o">=</span><span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">])</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">contains</span><span class="p">(</span><span class="n">doc_id</span><span class="o">=</span><span class="mi">1</span><span class="p">)</span>
<span class="go">True</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">remove</span><span class="p">(</span><span class="n">doc_ids</span><span class="o">=</span><span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">])</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="n">doc_id</span><span class="o">=</span><span class="mi">3</span><span class="p">)</span>
<span class="go">{...}</span>
</pre></div>
</div>
<p>Using <code class="docutils literal notranslate"><span class="pre">doc_id</span></code> instead of <code class="docutils literal notranslate"><span class="pre">Query()</span></code> again is slightly faster in operation.</p>
<div class="section" id="id2">
<h3>Recap<a class="headerlink" href="#id2" title="Permalink to this headline">¶</a></h3>
<p>Let’s sum up the way TinyDB supports working with IDs:</p>
<div class="wy-table-responsive"><table border="1" class="docutils">
<colgroup>
<col width="38%">
<col width="62%">
</colgroup>
<tbody valign="top">
<tr class="row-odd"><td colspan="2"><strong>Getting a document’s ID</strong></td>
</tr>
<tr class="row-even"><td><code class="docutils literal notranslate"><span class="pre">db.insert(...)</span></code></td>
<td>Returns the inserted document’s ID</td>
</tr>
<tr class="row-odd"><td><code class="docutils literal notranslate"><span class="pre">db.insert_multiple(...)</span></code></td>
<td>Returns the inserted documents’ ID</td>
</tr>
<tr class="row-even"><td><code class="docutils literal notranslate"><span class="pre">document.doc_id</span></code></td>
<td>Get the ID of a document fetched from the db</td>
</tr>
<tr class="row-odd"><td colspan="2"><strong>Working with IDs</strong></td>
</tr>
<tr class="row-even"><td><code class="docutils literal notranslate"><span class="pre">db.get(doc_id=...)</span></code></td>
<td>Get the document with the given ID</td>
</tr>
<tr class="row-odd"><td><code class="docutils literal notranslate"><span class="pre">db.contains(doc_id=...)</span></code></td>
<td>Check if the db contains a document with the given
IDs</td>
</tr>
<tr class="row-even"><td><code class="docutils literal notranslate"><span class="pre">db.update({...},</span> <span class="pre">doc_ids=[...])</span></code></td>
<td>Update all documents with the given IDs</td>
</tr>
<tr class="row-odd"><td><code class="docutils literal notranslate"><span class="pre">db.remove(doc_ids=[...])</span></code></td>
<td>Remove all documents with the given IDs</td>
</tr>
</tbody>
</table></div>
</div>
</div>
<div class="section" id="tables">
<h2>Tables<a class="headerlink" href="#tables" title="Permalink to this headline">¶</a></h2>
<p>TinyDB supports working with multiple tables. They behave just the same as
the <code class="docutils literal notranslate"><span class="pre">TinyDB</span></code> class. To create and use a table, use <code class="docutils literal notranslate"><span class="pre">db.table(name)</span></code>.</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">table</span> <span class="o">=</span> <span class="n">db</span><span class="o">.</span><span class="n">table</span><span class="p">(</span><span class="s1">'table_name'</span><span class="p">)</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">table</span><span class="o">.</span><span class="n">insert</span><span class="p">({</span><span class="s1">'value'</span><span class="p">:</span> <span class="kc">True</span><span class="p">})</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">table</span><span class="o">.</span><span class="n">all</span><span class="p">()</span>
<span class="go">[{'value': True}]</span>
<span class="gp">&gt;&gt;&gt; </span><span class="k">for</span> <span class="n">row</span> <span class="ow">in</span> <span class="n">table</span><span class="p">:</span>
<span class="gp">&gt;&gt;&gt; </span>    <span class="nb">print</span><span class="p">(</span><span class="n">row</span><span class="p">)</span>
<span class="go">{'value': True}</span>
</pre></div>
</div>
<p>To remove a table from a database, use:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">drop_table</span><span class="p">(</span><span class="s1">'table_name'</span><span class="p">)</span>
</pre></div>
</div>
<p>If on the other hand you want to remove all tables, use the counterpart:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">drop_tables</span><span class="p">()</span>
</pre></div>
</div>
<p>Finally, you can get a list with the names of all tables in your database:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">tables</span><span class="p">()</span>
<span class="go">{'_default', 'table_name'}</span>
</pre></div>
</div>
<div class="section" id="default-table">
<span id="id3"></span><h3>Default Table<a class="headerlink" href="#default-table" title="Permalink to this headline">¶</a></h3>
<p>TinyDB uses a table named <code class="docutils literal notranslate"><span class="pre">_default</span></code> as the default table. All operations
on the database object (like <code class="docutils literal notranslate"><span class="pre">db.insert(...)</span></code>) operate on this table.
The name of this table can be modified by setting the <code class="docutils literal notranslate"><span class="pre">default_table_name</span></code>
class variable to modify the default table name for all instances:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="c1">#1: for a single instance only</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span> <span class="o">=</span> <span class="n">TinyDB</span><span class="p">(</span><span class="n">storage</span><span class="o">=</span><span class="n">SomeStorage</span><span class="p">)</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">default_table_name</span> <span class="o">=</span> <span class="s1">'my-default'</span>
<span class="gp">&gt;&gt;&gt; </span><span class="c1">#2: for all instances</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">TinyDB</span><span class="o">.</span><span class="n">default_table_name</span> <span class="o">=</span> <span class="s1">'my-default'</span>
</pre></div>
</div>
</div>
<div class="section" id="query-caching">
<span id="id4"></span><h3>Query Caching<a class="headerlink" href="#query-caching" title="Permalink to this headline">¶</a></h3>
<p>TinyDB caches query result for performance. That way re-running a query won’t
have to read the data from the storage as long as the database hasn’t been
modified. You can optimize the query cache size by passing the <code class="docutils literal notranslate"><span class="pre">cache_size</span></code>
to the <code class="docutils literal notranslate"><span class="pre">table(...)</span></code> function:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">table</span> <span class="o">=</span> <span class="n">db</span><span class="o">.</span><span class="n">table</span><span class="p">(</span><span class="s1">'table_name'</span><span class="p">,</span> <span class="n">cache_size</span><span class="o">=</span><span class="mi">30</span><span class="p">)</span>
</pre></div>
</div>
<div class="admonition hint">
<p class="first admonition-title">Hint</p>
<p class="last">You can set <code class="docutils literal notranslate"><span class="pre">cache_size</span></code> to <code class="docutils literal notranslate"><span class="pre">None</span></code> to make the cache unlimited in
size. Also, you can set <code class="docutils literal notranslate"><span class="pre">cache_size</span></code> to 0 to disable it.</p>
</div>
<div class="admonition hint">
<p class="first admonition-title">Hint</p>
<p class="last">It’s not possible to open the same table multiple times with different
settings. After the first invocation, all the subsequent calls will return
the same table with the same settings as the first one.</p>
</div>
<div class="admonition hint">
<p class="first admonition-title">Hint</p>
<p class="last">The TinyDB query cache doesn’t check if the underlying storage
that the database uses has been modified by an external process. In this
case the query cache may return outdated results. To clear the cache and
read data from the storage again you can use <code class="docutils literal notranslate"><span class="pre">db.clear_cache()</span></code>.</p>
</div>
<div class="admonition hint">
<p class="first admonition-title">Hint</p>
<p class="last">When using an unlimited cache size and <code class="docutils literal notranslate"><span class="pre">test()</span></code> queries, TinyDB
will store a reference to the test function. As a result of that behavior
long-running applications that use <code class="docutils literal notranslate"><span class="pre">lambda</span></code> functions as a test function
may experience memory leaks.</p>
</div>
</div>
</div>
<div class="section" id="storage-middleware">
<h2>Storage &amp; Middleware<a class="headerlink" href="#storage-middleware" title="Permalink to this headline">¶</a></h2>
<div class="section" id="storage-types">
<h3>Storage Types<a class="headerlink" href="#storage-types" title="Permalink to this headline">¶</a></h3>
<p>TinyDB comes with two storage types: JSON and in-memory. By
default TinyDB stores its data in JSON files so you have to specify the path
where to store it:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="kn">from</span> <span class="nn">tinydb</span> <span class="kn">import</span> <span class="n">TinyDB</span><span class="p">,</span> <span class="n">where</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span> <span class="o">=</span> <span class="n">TinyDB</span><span class="p">(</span><span class="s1">'path/to/db.json'</span><span class="p">)</span>
</pre></div>
</div>
<p>To use the in-memory storage, use:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="kn">from</span> <span class="nn">tinydb.storages</span> <span class="kn">import</span> <span class="n">MemoryStorage</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span> <span class="o">=</span> <span class="n">TinyDB</span><span class="p">(</span><span class="n">storage</span><span class="o">=</span><span class="n">MemoryStorage</span><span class="p">)</span>
</pre></div>
</div>
<div class="admonition hint">
<p class="first admonition-title">Hint</p>
<p>All arguments except for the <code class="docutils literal notranslate"><span class="pre">storage</span></code> argument are forwarded to the
underlying storage. For the JSON storage you can use this to pass
additional keyword arguments to Python’s
<a class="reference external" href="https://docs.python.org/2/library/json.html#json.dump">json.dump(…)</a>
method. For example, you can set it to create prettified JSON files like
this:</p>
<div class="last highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">db</span> <span class="o">=</span> <span class="n">TinyDB</span><span class="p">(</span><span class="s1">'db.json'</span><span class="p">,</span> <span class="n">sort_keys</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">indent</span><span class="o">=</span><span class="mi">4</span><span class="p">,</span> <span class="n">separators</span><span class="o">=</span><span class="p">(</span><span class="s1">','</span><span class="p">,</span> <span class="s1">': '</span><span class="p">))</span>
</pre></div>
</div>
</div>
<p>To modify the default storage for all <code class="docutils literal notranslate"><span class="pre">TinyDB</span></code> instances, set the
<code class="docutils literal notranslate"><span class="pre">default_storage_class</span></code> class variable:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">TinyDB</span><span class="o">.</span><span class="n">default_storage_class</span> <span class="o">=</span> <span class="n">MemoryStorage</span>
</pre></div>
</div>
<p>In case you need to access the storage instance directly, you can use the
<code class="docutils literal notranslate"><span class="pre">storage</span></code> property of your TinyDB instance. This may be useful to call
method directly on the storage or middleware:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">db</span> <span class="o">=</span> <span class="n">TinyDB</span><span class="p">(</span><span class="n">storage</span><span class="o">=</span><span class="n">CachingMiddleware</span><span class="p">(</span><span class="n">MemoryStorage</span><span class="p">))</span>
<span class="go">&lt;tinydb.middlewares.CachingMiddleware at 0x10991def0&gt;</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span><span class="o">.</span><span class="n">storage</span><span class="o">.</span><span class="n">flush</span><span class="p">()</span>
</pre></div>
</div>
</div>
<div class="section" id="middleware">
<h3>Middleware<a class="headerlink" href="#middleware" title="Permalink to this headline">¶</a></h3>
<p>Middleware wraps around existing storage allowing you to customize their
behaviour.</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="kn">from</span> <span class="nn">tinydb.storages</span> <span class="kn">import</span> <span class="n">JSONStorage</span>
<span class="gp">&gt;&gt;&gt; </span><span class="kn">from</span> <span class="nn">tinydb.middlewares</span> <span class="kn">import</span> <span class="n">CachingMiddleware</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">db</span> <span class="o">=</span> <span class="n">TinyDB</span><span class="p">(</span><span class="s1">'/path/to/db.json'</span><span class="p">,</span> <span class="n">storage</span><span class="o">=</span><span class="n">CachingMiddleware</span><span class="p">(</span><span class="n">JSONStorage</span><span class="p">))</span>
</pre></div>
</div>
<div class="admonition hint">
<p class="first admonition-title">Hint</p>
<p>You can nest middleware:</p>
<div class="last highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">db</span> <span class="o">=</span> <span class="n">TinyDB</span><span class="p">(</span><span class="s1">'/path/to/db.json'</span><span class="p">,</span>
<span class="go">                storage=FirstMiddleware(SecondMiddleware(JSONStorage)))</span>
</pre></div>
</div>
</div>
<div class="section" id="cachingmiddleware">
<h4>CachingMiddleware<a class="headerlink" href="#cachingmiddleware" title="Permalink to this headline">¶</a></h4>
<p>The <code class="docutils literal notranslate"><span class="pre">CachingMiddleware</span></code> improves speed by reducing disk I/O. It caches all
read operations and writes data to disk after a configured number of
write operations.</p>
<p>To make sure that all data is safely written when closing the table, use one
of these ways:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="c1"># Using a context manager:</span>
<span class="k">with</span> <span class="n">database</span> <span class="k">as</span> <span class="n">db</span><span class="p">:</span>
    <span class="c1"># Your operations</span>
</pre></div>
</div>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="c1"># Using the close function</span>
<span class="n">db</span><span class="o">.</span><span class="n">close</span><span class="p">()</span>
</pre></div>
</div>
</div>
</div>
</div>
<div class="section" id="mypy-type-checking">
<span id="id5"></span><h2>MyPy Type Checking<a class="headerlink" href="#mypy-type-checking" title="Permalink to this headline">¶</a></h2>
<p>TinyDB comes with type annotations that MyPy can use to make sure you’re using
the API correctly. Unfortunately, MyPy doesn’t understand all code patterns
that TinyDB uses. For that reason TinyDB ships a MyPy plugin that helps
correctly type checking code that uses TinyDB. To use it, add it to the
plugins list in the <a class="reference external" href="https://mypy.readthedocs.io/en/latest/config_file.html">MyPy configuration file</a>
(typically located in <code class="docutils literal notranslate"><span class="pre">setup.cfg</span></code> or <code class="docutils literal notranslate"><span class="pre">mypy.ini</span></code>):</p>
<div class="highlight-ini notranslate"><div class="highlight"><pre><span></span><span class="k">[mypy]</span><span class="w"></span>
<span class="na">plugins</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="s">tinydb.mypy_plugin</span><span class="w"></span>
</pre></div>
</div>
</div>
<div class="section" id="what-s-next">
<h2>What’s next<a class="headerlink" href="#what-s-next" title="Permalink to this headline">¶</a></h2>
<p>Congratulations, you’ve made through the user guide! Now go and build something
awesome or dive deeper into TinyDB with these resources:</p>
<ul class="simple">
<li>Want to learn how to customize TinyDB (storages, middlewares) and what
extensions exist? Check out <a class="reference internal" href="extend.html"><span class="doc">How to Extend TinyDB</span></a> and <a class="reference internal" href="extensions.html"><span class="doc">Extensions</span></a>.</li>
<li>Want to study the API in detail? Read <a class="reference internal" href="api.html"><span class="doc">API Documentation</span></a>.</li>
<li>Interested in contributing to the TinyDB development guide? Go on to the
<a class="reference internal" href="contribute.html"><span class="doc">Contribution Guidelines</span></a>.</li>

&gt;&gt;&gt; &cent; &euro; &copy; &reg; &amp;
</ul> 
</div>
</div>'''


    print(removedor_tags_html(html=html, save_file=True))