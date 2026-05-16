# Fix 1: product_list.html - add data-cart-count to fcb-count span
f1 = '/app/templates/catalog/product_list.html'
c = open(f1, encoding='utf-8').read()
old = '<span id="fcb-count">{{ cart_total_items }}</span>'
new = '<span id="fcb-count" data-cart-count>{{ cart_total_items }}</span>'
if old in c:
    c = c.replace(old, new, 1)
    open(f1, 'w', encoding='utf-8').write(c)
    print('product_list: OK')
else:
    print('product_list: NOT FOUND')

# Fix 2: product_detail.html - add data-cart-count to fcb-count-detail span
f2 = '/app/templates/catalog/product_detail.html'
c = open(f2, encoding='utf-8').read()
old2 = '<span id="fcb-count-detail">{{ cart_total_items }}</span>'
new2 = '<span id="fcb-count-detail" data-cart-count>{{ cart_total_items }}</span>'
if old2 in c:
    c = c.replace(old2, new2, 1)
    open(f2, 'w', encoding='utf-8').write(c)
    print('product_detail: OK')
else:
    print('product_detail: NOT FOUND - searching...')
    idx = c.find('fcb-count-detail')
    print(repr(c[idx:idx+80]))
