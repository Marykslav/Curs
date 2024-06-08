from graphviz import Digraph

# Create a new directed graph
dot = Digraph()

# Define nodes
dot.node('async_session', 'async_session\n<<class>>')
dot.node('User', 'User\n<<class>>\n- tg_id: int')
dot.node('Category', 'Category\n<<class>>')
dot.node('Item', 'Item\n<<class>>\n- category: int\n- id: int')
dot.node('Novelty', 'Novelty\n<<class>>')
dot.node('Item1', 'Item1\n<<class>>\n- novelty: int\n- id: int')
dot.node('Manga', 'Manga\n<<class>>')
dot.node('Item2', 'Item2\n<<class>>\n- manga: int\n- id: int')
dot.node('Functions', '''Functions
+ set_user(tg_id: int): None
+ get_categories(): Category
+ get_category_item(category_id): Item
+ get_item(item_id): Item
+ get_novelties(): Novelty
+ get_novelty_item1(novelty_id): Item1
+ get_item1(item1_id): Item1
+ get_mangs(): Manga
+ get_manga_item2(manga_id): Item2
+ get_item2(item2_id): Item2
''')

# Define edges
dot.edge('Functions', 'async_session', label='uses')
dot.edge('Functions', 'User', label='uses')
dot.edge('Functions', 'Category', label='uses')
dot.edge('Functions', 'Item', label='uses')
dot.edge('Functions', 'Novelty', label='uses')
dot.edge('Functions', 'Item1', label='uses')
dot.edge('Functions', 'Manga', label='uses')
dot.edge('Functions', 'Item2', label='uses')

# Render the diagram to a file
dot.render('C:\Users\Myroslav\.vscode\B', format='png')

'C:\Users\Myroslav\.vscode\B.png'
